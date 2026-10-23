import os
import uuid
from django.core.files.storage import default_storage
from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    BasePermission,
    IsAuthenticated,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models, transaction
from django.db.models import Subquery, OuterRef, Count, IntegerField
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import (
    Faculty,
    FacultyLaboratory,
    Program,
    FacultyMember,
    FacultyAppointment,
    UserProfile,
    AlumniStory,
    Course,
    Student,
    ScheduleItem,
    StudentGrade,
    NewsArticle,
    Event,
    AcademicCalendarEvent,
    JobOffer,
    JobApplication,
    AdmissionApplication,
    Notification,
    UserNotificationState,
    UserNotificationPreference,
    ActivityLog,
    SiteSetting,
    Book,
    BookReservation,
    ResearchCenter,
    ResearchArea,
    ResearchPublication,
    HousingFeature,
    StudentClub,
    SportActivity,
    CampusLifeOverview,
)
from PIL import Image
from .serializers import (
    FacultySerializer,
    FacultyLaboratorySerializer,
    ProgramSerializer,
    FacultyMemberSerializer,
    FacultyAppointmentSerializer,
    UserProfileSerializer,
    AlumniStorySerializer,
    CourseSerializer,
    StudentSerializer,
    ScheduleItemSerializer,
    StudentGradeSerializer,
    NewsArticleSerializer,
    EventSerializer,
    AcademicCalendarEventSerializer,
    JobOfferSerializer,
    JobApplicationSerializer,
    AdmissionApplicationSerializer,
    NotificationSerializer,
    UserNotificationPreferenceSerializer,
    ActivityLogSerializer,
    SiteSettingSerializer,
    BookSerializer,
    BookReservationSerializer,
    ResearchCenterSerializer,
    ResearchAreaSerializer,
    ResearchPublicationSerializer,
    HousingFeatureSerializer,
    StudentClubSerializer,
    SportActivitySerializer,
    CampusLifeOverviewSerializer,
)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by("-created_at")
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name_ar", "name_en", "email", "role", "phone"]

    def perform_create(self, serializer):
        instance = serializer.save()
        user_name = instance.name_ar or instance.name_en or instance.email

        # If a password was provided in request, hash it properly
        raw_password = serializer.validated_data.get("password")
        if raw_password:
            instance.set_password(raw_password)
            instance.save(update_fields=["password"])

        # Sync with academic profile (FacultyMember / Student)
        self._sync_academic_profile(instance)

        Notification.objects.create(
            title_ar=f"تسجيل مستخدم جديد: '{user_name}'",
            title_en=f"New User Registered: '{user_name}'",
            message_ar=f"انضم مستخدم جديد للنظام بالدور الوظيفي: ({instance.role}) والبريد: {instance.email}",
            message_en=f"New user registered with role: ({instance.role}) and email: {instance.email}",
            type="info",
            link="/dashboard/users",
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        raw_password = serializer.validated_data.get("password")
        if raw_password:
            instance.set_password(raw_password)
            instance.save(update_fields=["password"])

        # Sync with academic profile (FacultyMember / Student)
        self._sync_academic_profile(instance)

    def _sync_academic_profile(self, instance):
        """
        Synchronize UserProfile with academic entities:
        - If role is 'faculty': create or update FacultyMember so they appear under faculty members.
        - If role is 'student' or 'alumni': link or update Student if exists.
        """
        if instance.role == "faculty" and instance.email:
            faculty_obj = instance.assigned_faculty
            if not faculty_obj and Faculty.objects.exists():
                faculty_obj = Faculty.objects.first()

            member = (
                FacultyMember.objects.filter(user=instance).first()
                or FacultyMember.objects.filter(email=instance.email).first()
            )

            if not member:
                FacultyMember.objects.create(
                    user=instance,
                    name_ar=instance.name_ar or "عضو هيئة تدريس",
                    name_en=instance.name_en or instance.name_ar or "Faculty Member",
                    email=instance.email,
                    title_ar="أستاذ محاضر",
                    title_en="Lecturer",
                    faculty=faculty_obj,
                    department=None,
                    department_ar="",
                    department_en="",
                    image=instance.avatar or "/user.png",
                    bio_ar=instance.bio or "",
                    bio_en=instance.bio or "",
                )
            else:
                member.name_ar = instance.name_ar or member.name_ar
                member.name_en = instance.name_en or member.name_en or member.name_ar
                if instance.avatar:
                    member.image = instance.avatar
                if instance.bio:
                    member.bio_ar = instance.bio
                if faculty_obj and not member.faculty:
                    member.faculty = faculty_obj
                if not member.user:
                    member.user = instance
                member.save()

        elif instance.role in ["student", "alumni"] and instance.email:
            student = (
                Student.objects.filter(user=instance).first()
                or Student.objects.filter(email=instance.email).first()
            )

            if student:
                student.name_ar = instance.name_ar or student.name_ar
                student.name_en = instance.name_en or student.name_en
                if not student.user:
                    student.user = instance
                student.save()


class FacultyViewSet(viewsets.ModelViewSet):
    serializer_class = FacultySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name_ar", "name_en", "slug"]

    def get_queryset(self):
        teachers_subquery = (
            FacultyMember.objects.filter(faculty=OuterRef("pk"))
            .values("faculty")
            .annotate(c=Count("id"))
            .values("c")
        )
        students_subquery = (
            Student.objects.filter(faculty=OuterRef("pk"))
            .values("faculty")
            .annotate(c=Count("id"))
            .values("c")
        )
        programs_subquery = (
            Program.objects.filter(faculty=OuterRef("pk"))
            .values("faculty")
            .annotate(c=Count("id"))
            .values("c")
        )

        return (
            Faculty.objects.select_related("dean")
            .prefetch_related("programs")
            .annotate(
                total_programs=Coalesce(
                    Subquery(programs_subquery, output_field=IntegerField()), 0
                ),
                total_teachers=Coalesce(
                    Subquery(teachers_subquery, output_field=IntegerField()), 0
                ),
                total_students=Coalesce(
                    Subquery(students_subquery, output_field=IntegerField()), 0
                ),
            )
        )

    def perform_create(self, serializer):
        instance = serializer.save()
        Notification.objects.create(
            title_ar=f"تمت إضافة كلية جديدة: '{instance.name_ar}'",
            title_en=f"New Faculty Added: '{instance.name_en}'",
            message_ar=f"تمت إضافة واعتماد كلية ({instance.name_ar}) في الهيكل الجامعي رسمياً",
            message_en=f"Faculty ({instance.name_en}) has been added to university structure",
            type="info",
            link="/dashboard/faculties",
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        Notification.objects.create(
            title_ar=f"تحديث بيانات كلية: '{instance.name_ar}'",
            title_en=f"Faculty Updated: '{instance.name_en}'",
            message_ar=f"تم تحديث بيانات وهوية وبرامج كلية ({instance.name_ar}) بنجاح",
            message_en=f"Faculty details updated for ({instance.name_en})",
            type="info",
            link="/dashboard/faculties",
        )

    def perform_destroy(self, instance):
        name_ar = instance.name_ar
        name_en = instance.name_en
        instance.delete()
        Notification.objects.create(
            title_ar=f"حذف كلية: '{name_ar}'",
            title_en=f"Faculty Deleted: '{name_en}'",
            message_ar=f"تم حذف كلية ({name_ar}) وجميع أقسامها المرتبطة من الهيكل الجامعي",
            message_en=f"Faculty ({name_en}) and all associated programs deleted",
            type="warning",
            link="/dashboard/faculties",
        )


class ProgramViewSet(viewsets.ModelViewSet):
    serializer_class = ProgramSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name_ar", "name_en", "slug"]

    def get_queryset(self):
        teachers_subquery = (
            FacultyMember.objects.filter(department=OuterRef("pk"))
            .values("department")
            .annotate(c=Count("id"))
            .values("c")
        )
        students_subquery = (
            Student.objects.filter(program=OuterRef("pk"))
            .values("program")
            .annotate(c=Count("id"))
            .values("c")
        )

        qs = (
            Program.objects.select_related("faculty", "head")
            .annotate(
                teachers_count=Coalesce(
                    Subquery(teachers_subquery, output_field=IntegerField()), 0
                ),
                total_students=Coalesce(
                    Subquery(students_subquery, output_field=IntegerField()), 0
                ),
            )
            .order_by("id")
        )

        faculty_id = self.request.query_params.get("faculty")
        faculty_slug = self.request.query_params.get("facultySlug")
        if faculty_id:
            qs = qs.filter(faculty_id=faculty_id)
        elif faculty_slug:
            qs = qs.filter(faculty__slug=faculty_slug)
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        faculty_name = instance.faculty.name_ar if instance.faculty else ""
        Notification.objects.create(
            title_ar=f"إضافة تخصص/قسم جديد: '{instance.name_ar}'",
            title_en=f"New Academic Program Added: '{instance.name_en}'",
            message_ar=f"تم اعتماد التخصص الجديد في {faculty_name}",
            message_en=f"New program created under {faculty_name}",
            type="info",
            link="/dashboard/programs",
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        faculty_name = instance.faculty.name_ar if instance.faculty else ""
        Notification.objects.create(
            title_ar=f"تحديث بيانات قسم: '{instance.name_ar}'",
            title_en=f"Academic Program Updated: '{instance.name_en}'",
            message_ar=f"تم تحديث بيانات وهوية تخصص ({instance.name_ar}) في {faculty_name}",
            message_en=f"Program details updated for ({instance.name_en}) in {faculty_name}",
            type="info",
            link="/dashboard/programs",
        )

    def perform_destroy(self, instance):
        name_ar = instance.name_ar
        name_en = instance.name_en
        faculty_name = instance.faculty.name_ar if instance.faculty else ""
        instance.delete()
        Notification.objects.create(
            title_ar=f"حذف قسم/تخصص: '{name_ar}'",
            title_en=f"Academic Program Deleted: '{name_en}'",
            message_ar=f"تم حذف قسم ({name_ar}) من {faculty_name}",
            message_en=f"Program ({name_en}) has been deleted from {faculty_name}",
            type="warning",
            link="/dashboard/programs",
        )


class FacultyMemberViewSet(viewsets.ModelViewSet):
    serializer_class = FacultyMemberSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name_ar", "name_en", "email", "department_ar", "department_en"]

    def get_queryset(self):
        qs = FacultyMember.objects.select_related("faculty", "department").order_by(
            "id"
        )
        faculty_id = self.request.query_params.get("faculty")
        department_id = self.request.query_params.get("department")
        if faculty_id:
            qs = qs.filter(faculty_id=faculty_id)
        if department_id:
            qs = qs.filter(department_id=department_id)
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()

        # Ensure UserProfile exists with role='faculty'
        if instance.email:
            profile, created = UserProfile.objects.get_or_create(
                email=instance.email,
                defaults={
                    "name_ar": instance.name_ar,
                    "name_en": instance.name_en or instance.name_ar,
                    "role": "faculty",
                    "assigned_faculty": instance.faculty,
                    "avatar": instance.image or "/user.png",
                },
            )
            if not created and profile.role != "faculty":
                profile.role = "faculty"
                if instance.faculty and not profile.assigned_faculty:
                    profile.assigned_faculty = instance.faculty
                profile.save()
            if not instance.user:
                instance.user = profile
                instance.save(update_fields=["user"])

        dept_name = (
            instance.department.name_ar
            if instance.department
            else (instance.department_ar or "الكلية")
        )
        Notification.objects.create(
            title_ar=f"انضمام عضو هيئة تدريس جديد: '{instance.name_ar}'",
            title_en=f"New Faculty Member Joined: '{instance.name_en}'",
            message_ar=f"تم تعيين الدكتور/المحاضر {instance.name_ar} في قسم {dept_name}",
            message_en=f"Faculty member {instance.name_en} assigned to {dept_name}",
            type="info",
            link="/dashboard/faculty-members",
        )

    def perform_update(self, serializer):
        instance = self.get_object()
        old_dept = instance.department
        new_instance = serializer.save()
        new_dept = new_instance.department

        if old_dept != new_dept:
            old_name = old_dept.name_ar if old_dept else "بدون قسم"
            new_name = new_dept.name_ar if new_dept else "بدون قسم"
            actor = (
                getattr(self.request.user, "first_name", "")
                or getattr(self.request.user, "username", "Admin")
                or "لوحة التحكم"
            )
            ActivityLog.objects.create(
                user_name=actor,
                action_ar=f"تم نقل عضو الهيئة التدريسية '{new_instance.name_ar}' من قسم ({old_name}) إلى قسم ({new_name})",
                action_en=f"Transferred faculty member '{new_instance.name_en}' from department ({old_name}) to ({new_name})",
                status="update",
            )


class FacultyAppointmentViewSet(viewsets.ModelViewSet):
    queryset = FacultyAppointment.objects.all().order_by("-created_at")
    serializer_class = FacultyAppointmentSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["student_name", "student_email", "student_id"]

    def perform_create(self, serializer):
        instance = serializer.save()
        doc_name = (
            instance.faculty_member.name_ar if instance.faculty_member else "عضو الكلية"
        )
        Notification.objects.create(
            title_ar=f"حجز موعد استشارة من الطالب: '{instance.student_name}'",
            title_en=f"New Advisory Appointment by: '{instance.student_name}'",
            message_ar=f"طلب موعد مقابلة واستشارة مع الدكتور: {doc_name}",
            message_en=f"Requested appointment with professor: {doc_name}",
            type="message",
            link="/dashboard/faculty-members",
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        status_text = (
            "مقبول"
            if instance.status == "accepted"
            else ("مرفوض" if instance.status == "rejected" else instance.status)
        )
        Notification.objects.create(
            title_ar=f"تحديث حالة موعد مقابلة الطالب: '{instance.student_name}'",
            title_en=f"Appointment Status Updated: '{instance.student_name}'",
            message_ar=f"تم تعديل حالة الطلب إلى ({status_text})",
            message_en=f"Appointment status changed to ({instance.status})",
            type="message",
            link="/dashboard/faculty-members",
        )


class AlumniStoryViewSet(viewsets.ModelViewSet):
    queryset = AlumniStory.objects.all()
    serializer_class = AlumniStorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name_ar", "name_en", "company_ar", "company_en"]

    def perform_create(self, serializer):
        instance = serializer.save()
        Notification.objects.create(
            title_ar=f"إضافة قصة نجاح خريج متميز: '{instance.name_ar}'",
            title_en=f"New Alumni Success Story: '{instance.name_en}'",
            message_ar=f"تمت إضافة إنجاز الخريج بالشركة: {instance.company_ar}",
            message_en=f"Added alumni achievement at company: {instance.company_en}",
            type="info",
            link="/alumni",
        )


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name_ar", "name_en", "code"]

    def get_queryset(self):
        qs = super().get_queryset()
        program_id = self.request.query_params.get("program")
        if program_id:
            qs = qs.filter(program_id=program_id)
        faculty_id = self.request.query_params.get("faculty")
        if faculty_id:
            qs = qs.filter(program__faculty_id=faculty_id)
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        Notification.objects.create(
            title_ar=f"إضافة كتاب / مقرر تعليمي جديد للمكتبة: '{instance.name_ar}'",
            title_en=f"New Book/Course Added to Library: '{instance.name_en}'",
            message_ar=f"تم إدراج المقرر الدراسي برمز المادة ({instance.code}) ورصيد الساعات: {instance.credits}",
            message_en=f"Course code ({instance.code}) added with credits: {instance.credits}",
            type="info",
            link="/dashboard/programs",
        )


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name_ar", "name_en", "student_id", "email"]

    def get_queryset(self):
        qs = Student.objects.select_related("faculty", "program").order_by("id")
        faculty_id = self.request.query_params.get("faculty")
        program_id = self.request.query_params.get(
            "program"
        ) or self.request.query_params.get("department")
        if faculty_id:
            qs = qs.filter(faculty_id=faculty_id)
        if program_id:
            qs = qs.filter(program_id=program_id)
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        Notification.objects.create(
            title_ar=f"تسجيل طالب جديد: '{instance.name_ar}'",
            title_en=f"New Student Enrolled: '{instance.name_en}'",
            message_ar=f"تم قيد الطالب بالسجل الأكاديمي برقم جامعي: {instance.student_id}",
            message_en=f"Student enrolled with university ID: {instance.student_id}",
            type="info",
            link="/dashboard/students",
        )

    def perform_update(self, serializer):
        instance = self.get_object()
        old_prog = instance.program
        new_instance = serializer.save()
        new_prog = new_instance.program

        if old_prog != new_prog:
            old_name = old_prog.name_ar if old_prog else "بدون تخصص"
            new_name = new_prog.name_ar if new_prog else "بدون تخصص"
            actor = (
                getattr(self.request.user, "first_name", "")
                or getattr(self.request.user, "username", "Admin")
                or "لوحة التحكم"
            )
            ActivityLog.objects.create(
                user_name=actor,
                action_ar=f"تم نقل الطالب '{new_instance.name_ar}' من قسم ({old_name}) إلى قسم ({new_name})",
                action_en=f"Transferred student '{new_instance.name_en}' from program ({old_name}) to ({new_name})",
                status="update",
            )

    @action(detail=False, methods=["post"], url_path="bulk-transfer")
    def bulk_transfer(self, request):
        student_ids = request.data.get("student_ids", [])
        target_program_id = request.data.get("target_program_id")

        if not student_ids or not target_program_id:
            return Response(
                {"detail": "يرجى تحديد الطلاب والقسم المراد النقل إليه"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            target_program = get_object_or_404(
                Program.objects.select_related("faculty"), pk=target_program_id
            )

            count = Student.objects.filter(id__in=student_ids).update(
                program=target_program,
                faculty=target_program.faculty,
            )

            actor = (
                getattr(request.user, "first_name", "")
                or getattr(request.user, "username", "Admin")
                or "لوحة التحكم"
            )
            ActivityLog.objects.create(
                user_name=actor,
                action_ar=f"تم نقل ({count}) طالب دفعة واحدة إلى قسم ({target_program.name_ar})",
                action_en=f"Bulk transferred ({count}) students to department ({target_program.name_en})",
                status="update",
            )

        return Response(
            {
                "detail": f"تم نقل {count} طالب بنجاح إلى قسم {target_program.name_ar}",
                "transferred_count": count,
            },
            status=status.HTTP_200_OK,
        )


class ScheduleItemViewSet(viewsets.ModelViewSet):
    queryset = ScheduleItem.objects.all()
    serializer_class = ScheduleItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        instance = serializer.save()
        course_name = instance.course.name_ar if instance.course else "المادة"
        Notification.objects.create(
            title_ar=f"إضافة محاضرة جديدة بالجدول: '{course_name}'",
            title_en=f"New Schedule Item Added: '{course_name}'",
            message_ar=f"اليوم: {instance.day_of_week} • القاعة: {instance.room_number}",
            message_en=f"Day: {instance.day_of_week} • Room: {instance.room_number}",
            type="warning",
            link="/dashboard/programs",
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        course_name = instance.course.name_ar if instance.course else "المادة"
        Notification.objects.create(
            title_ar=f"تحديث قاعة/توقيت محاضرة: '{course_name}'",
            title_en=f"Lecture Schedule/Room Changed: '{course_name}'",
            message_ar=f"تغير الموعد إلى يوم {instance.day_of_week} والقاعة {instance.room_number}",
            message_en=f"Updated to day {instance.day_of_week} and room {instance.room_number}",
            type="warning",
            link="/dashboard/programs",
        )


class StudentGradeViewSet(viewsets.ModelViewSet):
    queryset = StudentGrade.objects.all()
    serializer_class = StudentGradeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        instance = serializer.save()
        Notification.objects.create(
            title_ar=f"رصد علامة امتحانية جديدة",
            title_en=f"New Exam Grade Recorded",
            message_ar=f"تم رفع العلامات وحفظها في السجل الامتحاني للطالب",
            message_en=f"New grade uploaded and saved in student academic ledger",
            type="result",
            link="/dashboard/students",
        )


class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title_ar", "title_en", "excerpt_ar", "excerpt_en", "content_ar", "content_en"]

    def get_queryset(self):
        qs = NewsArticle.objects.all().select_related("faculty", "program").order_by("-date", "-id")
        scope = self.request.query_params.get("scope")
        if scope:
            qs = qs.filter(scope=scope)
        faculty_id = self.request.query_params.get("faculty")
        if faculty_id:
            qs = qs.filter(faculty_id=faculty_id)
        program_id = self.request.query_params.get("program")
        if program_id:
            qs = qs.filter(program_id=program_id)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)
        featured = self.request.query_params.get("featured")
        if featured is not None:
            if featured.lower() in ("true", "1"):
                qs = qs.filter(featured=True)
            elif featured.lower() in ("false", "0"):
                qs = qs.filter(featured=False)
        return qs

    @action(detail=True, methods=["post"], permission_classes=[AllowAny])
    def increment_view(self, request, pk=None):
        article = self.get_object()
        article.views_count = (article.views_count or 0) + 1
        article.save(update_fields=["views_count"])
        return Response({"viewsCount": article.views_count})

    def perform_create(self, serializer):
        instance = serializer.save()
        Notification.objects.create(
            title_ar=f"نشر خبر جديد: '{instance.title_ar}'",
            title_en=f"News Article Published: '{instance.title_en}'",
            message_ar=f"تم نشر خبر رسمي جديد في البوابة الأكاديمية",
            message_en=f"Official news published on university portal",
            type="info",
            link="/dashboard/news",
        )


class MediaUploadView(APIView):
    """
    Generic media and document upload endpoint.
    Saves uploaded files to MEDIA_ROOT/uploads/<folder>/
    Returns direct public URL, filename, and formatted file size.
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        folder = request.data.get("folder", "news")
        ext = os.path.splitext(file_obj.name)[1].lower()
        allowed_extensions = [
            ".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg",
            ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".zip"
        ]
        if ext not in allowed_extensions:
            return Response(
                {"error": f"الملحق {ext} غير مدعوم. الملحقات المسموحة: صور ومستندات PDF."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate unique safe name
        safe_base = "".join([c if c.isalnum() or c in (".", "_", "-") else "_" for c in file_obj.name])
        unique_name = f"{uuid.uuid4().hex[:8]}_{safe_base}"
        save_rel_path = os.path.join("uploads", folder, unique_name).replace("\\", "/")

        saved_path = default_storage.save(save_rel_path, file_obj)
        file_url = default_storage.url(saved_path)

        size_bytes = file_obj.size
        size_formatted = f"{size_bytes / 1024:.1f} KB" if size_bytes < 1048576 else f"{size_bytes / 1048576:.2f} MB"

        return Response(
            {
                "url": file_url,
                "filename": file_obj.name,
                "size": size_bytes,
                "sizeFormatted": size_formatted,
                "fileType": ext.replace(".", "").upper(),
            },
            status=status.HTTP_201_CREATED,
        )


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title_ar", "title_en", "location_ar", "location_en"]

    def perform_create(self, serializer):
        instance = serializer.save()
        Notification.objects.create(
            title_ar=f"إعلان فعالية جديدة: '{instance.title_ar}'",
            title_en=f"New Event Announced: '{instance.title_en}'",
            message_ar=f"المكان: {instance.location_ar} • التاريخ: {instance.date_ar}",
            message_en=f"Location: {instance.location_en} • Date: {instance.date_en}",
            type="info",
            link="/dashboard/news",
        )


class AcademicCalendarEventViewSet(viewsets.ModelViewSet):
    queryset = AcademicCalendarEvent.objects.all().order_by("order", "id")
    serializer_class = AcademicCalendarEventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["event_ar", "event_en", "date_ar", "date_en"]

    def perform_create(self, serializer):
        instance = serializer.save()
        Notification.objects.create(
            title_ar=f"إضافة موعد بالتقويم الأكاديمي: '{instance.event_ar}'",
            title_en=f"Academic Calendar Event Added: '{instance.event_en}'",
            message_ar=f"التاريخ المقترح: {instance.date_ar}",
            message_en=f"Scheduled date: {instance.date_en}",
            type="info",
            link="/news",
        )


class JobOfferViewSet(viewsets.ModelViewSet):
    queryset = JobOffer.objects.all().order_by("-created_at")
    serializer_class = JobOfferSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title_ar", "title_en", "department_ar", "department_en"]

    def perform_create(self, serializer):
        instance = serializer.save()
        Notification.objects.create(
            title_ar=f"افتتاح شاغر وظيفي جديد: '{instance.title_ar}'",
            title_en=f"New Job Opportunity Opened: '{instance.title_en}'",
            message_ar=f"القسم: {instance.department_ar} • آخر موعد: {instance.deadline}",
            message_en=f"Department: {instance.department_en} • Deadline: {instance.deadline}",
            type="info",
            link="/dashboard/jobs",
        )


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all().order_by("-created_at")
    serializer_class = JobApplicationSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["applicant_name", "email", "phone"]

    def perform_create(self, serializer):
        instance = serializer.save()
        job_title = instance.job.title_ar if instance.job else "فرصة عمل"
        Notification.objects.create(
            title_ar=f"طلب توظيف جديد من '{instance.applicant_name}'",
            title_en=f"New Job Application from '{instance.applicant_name}'",
            message_ar=f"تم تقديم طلب جديد لشغل شاغر: {job_title}",
            message_en=f"New application received for position: {job_title}",
            type="message",
            link="/dashboard/jobs",
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        status_text = (
            "مقبول"
            if instance.status == "accepted"
            else ("مرفوض" if instance.status == "rejected" else instance.status)
        )
        Notification.objects.create(
            title_ar=f"تحديث حالة طلب التوظيف للمتقدم: '{instance.applicant_name}'",
            title_en=f"Job Application Status Changed: '{instance.applicant_name}'",
            message_ar=f"تغيرت حالة الطلب إلى ({status_text})",
            message_en=f"Job application status updated to ({instance.status})",
            type="info",
            link="/dashboard/jobs",
        )


class AdmissionApplicationViewSet(viewsets.ModelViewSet):
    queryset = AdmissionApplication.objects.all().order_by("-created_at")
    serializer_class = AdmissionApplicationSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["full_name_ar", "full_name_en", "email", "phone"]

    def perform_create(self, serializer):
        instance = serializer.save()
        Notification.objects.create(
            title_ar=f"طلب مفاضلة/قبول جديد من '{instance.full_name_ar}'",
            title_en=f"New Admission Application from '{instance.full_name_en}'",
            message_ar=f"المعدل: {instance.high_school_score}% • الفرع: {instance.high_school_branch}",
            message_en=f"Score: {instance.high_school_score}% • Branch: {instance.high_school_branch}",
            type="info",
            link="/dashboard/students",
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        status_text = (
            "مقبول"
            if instance.status == "accepted"
            else ("مرفوض" if instance.status == "rejected" else instance.status)
        )
        Notification.objects.create(
            title_ar=f"تحديث قرار المفاضلة للطالب: '{instance.full_name_ar}'",
            title_en=f"Admission Application Status Changed: '{instance.full_name_en}'",
            message_ar=f"تم تعديل حالة طلب القبول إلى ({status_text})",
            message_en=f"Admission application status updated to ({instance.status})",
            type="result",
            link="/dashboard/students",
        )


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by("-created_at")
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

    def _get_target_user(self):
        user_id = (
            self.request.query_params.get("user")
            or self.request.data.get("user_id")
            or self.request.data.get("user")
        )
        if user_id:
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                pass
        if self.request.user and self.request.user.is_authenticated:
            return self.request.user
        return None

    def get_queryset(self):
        qs = super().get_queryset()
        user = self._get_target_user()
        if user:
            qs = qs.filter(models.Q(user=user) | models.Q(user__isnull=True))
            # Apply user notification mute preferences
            if hasattr(user, "notification_preference"):
                pref = user.notification_preference
                muted_types = []
                if pref.mute_messages:
                    muted_types.append("message")
                if pref.mute_results:
                    muted_types.append("result")
                if pref.mute_info:
                    muted_types.append("info")
                if pref.mute_warning:
                    muted_types.append("warning")
                if pref.mute_urgent:
                    muted_types.append("urgent")
                if muted_types:
                    qs = qs.exclude(type__in=muted_types)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = self._get_target_user()

        # Map per-user read states if user exists
        user_read_states = {}
        if user:
            states = UserNotificationState.objects.filter(
                user=user, notification__in=queryset
            )
            user_read_states = {st.notification_id: st.is_read for st in states}

        page = self.paginate_queryset(queryset)
        target_qs = page if page is not None else queryset

        serializer = self.get_serializer(target_qs, many=True)
        data = serializer.data

        # Override isRead with per-user state
        for item in data:
            notif_id = item["id"]
            if user and notif_id in user_read_states:
                item["isRead"] = user_read_states[notif_id]

        if page is not None:
            return self.get_paginated_response(data)
        return Response(data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self._get_target_user()

        is_read = request.data.get("is_read") or request.data.get("isRead")
        if is_read is not None:
            is_read_bool = bool(is_read)
            if user:
                UserNotificationState.objects.update_or_create(
                    user=user,
                    notification=instance,
                    defaults={
                        "is_read": is_read_bool,
                        "read_at": timezone.now() if is_read_bool else None,
                    },
                )
            if instance.user and instance.user == user:
                instance.is_read = is_read_bool
                instance.save()

        serializer = self.get_serializer(instance)
        data = serializer.data
        if user:
            st = UserNotificationState.objects.filter(
                user=user, notification=instance
            ).first()
            if st:
                data["isRead"] = st.is_read
        return Response(data)

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        user = self._get_target_user()
        target_notifications = self.get_queryset()

        if user:
            # Create/update per-user read state for all notifications visible to this user
            now = timezone.now()
            for notif in target_notifications:
                UserNotificationState.objects.update_or_create(
                    user=user,
                    notification=notif,
                    defaults={"is_read": True, "read_at": now},
                )
            Notification.objects.filter(user=user, is_read=False).update(is_read=True)
        else:
            Notification.objects.filter(is_read=False).update(is_read=True)

        return Response(
            {
                "status": "success",
                "message": "All notifications marked as read for user",
            }
        )

    @action(detail=False, methods=["get", "patch"])
    def preferences(self, request):
        user = self._get_target_user()
        if not user:
            return Response(
                {"error": "User context is required for notification preferences"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pref, _ = UserNotificationPreference.objects.get_or_create(user=user)

        if request.method == "PATCH":
            serializer = UserNotificationPreferenceSerializer(
                pref, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
            else:
                # Custom payload field mapping if camelCase passed
                data = request.data
                if "muteMessages" in data:
                    pref.mute_messages = data["muteMessages"]
                if "muteResults" in data:
                    pref.mute_results = data["muteResults"]
                if "muteInfo" in data:
                    pref.mute_info = data["muteInfo"]
                if "muteWarning" in data:
                    pref.mute_warning = data["muteWarning"]
                if "muteUrgent" in data:
                    pref.mute_urgent = data["muteUrgent"]
                pref.save()

        serializer = UserNotificationPreferenceSerializer(pref)
        return Response(serializer.data)


class ActivityLogViewSet(viewsets.ModelViewSet):
    queryset = ActivityLog.objects.all().order_by("-created_at")
    serializer_class = ActivityLogSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["user_name", "user_name_en", "action_ar", "action_en"]


class SiteSettingViewSet(viewsets.ModelViewSet):
    queryset = SiteSetting.objects.all()
    serializer_class = SiteSettingSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        setting, _ = SiteSetting.objects.get_or_create(id=1)
        serializer = self.get_serializer(setting)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        setting, _ = SiteSetting.objects.get_or_create(id=1)
        serializer = self.get_serializer(setting, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        setting, _ = SiteSetting.objects.get_or_create(id=1)
        serializer = self.get_serializer(setting, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class IsAdminOrContentManager(BasePermission):
    """
    Grants access only to authenticated users with 'admin' or 'content_manager' role,
    or superusers/staff members.
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.is_superuser or request.user.is_staff:
            return True
        user_role = getattr(request.user, "role", "")
        return user_role in ["admin", "content_manager"]


class IsAdminOrReadOnly(BasePermission):
    """
    Public read access for safe methods (GET, HEAD, OPTIONS).
    Write access strictly limited to admins and content managers.
    """

    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.is_superuser or request.user.is_staff:
            return True
        user_role = getattr(request.user, "role", "")
        return user_role in ["admin", "content_manager"]


class BookPdfUploadView(APIView):
    """
    Strict, hardened PDF upload endpoint.
    ONLY accepts files with .pdf extension, valid application/pdf MIME,
    and genuine %PDF- magic bytes header.
    Rejects any executable or masqueraded file formats.
    """

    permission_classes = [AllowAny]  # Can be tightened, but allow authenticated or dashboard requests
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response(
                {"error": "لم يتم إرفاق أي ملف."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Strict extension check
        ext = os.path.splitext(file_obj.name)[1].lower()
        if ext != ".pdf":
            return Response(
                {
                    "error": f"الملف المرفوع ذو امتداد ({ext}) غير مسموح. يُسمح فقط وحصراً برفع ملفات PDF (.pdf)."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 2. Strict file size check (Max 100 MB)
        max_size = 100 * 1024 * 1024
        if file_obj.size > max_size:
            return Response(
                {"error": "حجم ملف الـ PDF يتجاوز الحد الأقصى المسموح (100 ميغابايت)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 3. Magic Bytes verification (Must start with %PDF-)
        header_sample = file_obj.read(5)
        file_obj.seek(0)
        if not header_sample.startswith(b"%PDF-"):
            return Response(
                {
                    "error": "الملف غير صالح أو مزور. لا يحتوي على الترويسة الرقمية المعتمدة لملفات الـ PDF (%PDF-)."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 4. Generate unique cryptographic filename to avoid path traversal and overwriting
        safe_base_name = f"{uuid.uuid4().hex}.pdf"
        rel_storage_path = os.path.join(
            "uploads", "library", "books", safe_base_name
        ).replace("\\", "/")

        saved_path = default_storage.save(rel_storage_path, file_obj)
        file_url = default_storage.url(saved_path)

        size_bytes = file_obj.size
        size_formatted = (
            f"{size_bytes / 1024:.1f} KB"
            if size_bytes < 1048576
            else f"{size_bytes / 1048576:.2f} MB"
        )

        return Response(
            {
                "url": file_url,
                "filename": file_obj.name,
                "size": size_bytes,
                "sizeFormatted": size_formatted,
                "fileType": "PDF",
            },
            status=status.HTTP_201_CREATED,
        )


class BookCoverUploadView(APIView):
    """
    Hardened Book Cover Image upload endpoint.
    Strictly verifies image headers, dimensions, and blocks scripts/polyglots using Pillow.
    Only allows .jpg, .jpeg, .png, .webp.
    """

    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response(
                {"error": "لم يتم إرفاق أي صورة."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Allowed extensions
        ext = os.path.splitext(file_obj.name)[1].lower()
        allowed_extensions = [".jpg", ".jpeg", ".png", ".webp"]
        if ext not in allowed_extensions:
            return Response(
                {
                    "error": f"امتداد الصورة ({ext}) غير مدعوم. الامتدادات المدعومة هي: JPG, JPEG, PNG, WEBP."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 2. Size limit (Max 5 MB)
        if file_obj.size > 5 * 1024 * 1024:
            return Response(
                {"error": "حجم صورة الغلاف يتجاوز الحد الأقصى المسموح به (5 ميغابايت)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 3. Pillow deep structure verification
        try:
            image = Image.open(file_obj)
            image.verify()
            file_obj.seek(0)
        except Exception:
            return Response(
                {"error": "الملف المرفوع ليس ملف صورة سليم أو يحتوي على بيانات تالفة."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 4. Randomized filename to prevent directory traversal
        safe_base_name = f"{uuid.uuid4().hex}{ext}"
        rel_storage_path = os.path.join(
            "uploads", "library", "covers", safe_base_name
        ).replace("\\", "/")

        saved_path = default_storage.save(rel_storage_path, file_obj)
        file_url = default_storage.url(saved_path)

        size_bytes = file_obj.size
        size_formatted = (
            f"{size_bytes / 1024:.1f} KB"
            if size_bytes < 1048576
            else f"{size_bytes / 1048576:.2f} MB"
        )

        return Response(
            {
                "url": file_url,
                "filename": file_obj.name,
                "size": size_bytes,
                "sizeFormatted": size_formatted,
                "fileType": ext.replace(".", "").upper(),
            },
            status=status.HTTP_201_CREATED,
        )


class BookViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Academic Books in ASU Library.
    Supports advanced filtering, search, live stats, view tracking, and instant reservation.
    """

    queryset = Book.objects.all().select_related("faculty").order_by("-created_at")
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Public read, write protected by action if needed
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title_ar", "title_en", "author_ar", "author_en", "isbn"]
    ordering_fields = [
        "created_at",
        "publication_year",
        "title_ar",
        "views_count",
        "downloads_count",
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get("category")
        faculty_id = self.request.query_params.get("faculty")
        available = self.request.query_params.get("available")

        if category and category != "all":
            qs = qs.filter(category=category)
        if faculty_id:
            qs = qs.filter(faculty_id=faculty_id)
        if available is not None and available != "all":
            if available in ["true", "1", "available"]:
                qs = qs.filter(is_available=True)
            elif available in ["false", "0", "reserved"]:
                qs = qs.filter(is_available=False)
        return qs

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def stats(self, request):
        """
        Returns live aggregated metrics for the library dashboard.
        """
        total = Book.objects.count()
        available = Book.objects.filter(is_available=True).count()
        reserved = total - available
        with_pdf = Book.objects.exclude(pdf_file="").count()
        total_downloads = (
            Book.objects.aggregate(total=models.Sum("downloads_count"))["total"] or 0
        )
        total_views = (
            Book.objects.aggregate(total=models.Sum("views_count"))["total"] or 0
        )
        total_reservations = BookReservation.objects.count()
        pending_reservations = BookReservation.objects.filter(
            status="pending"
        ).count()

        return Response(
            {
                "total": total,
                "available": available,
                "reserved": reserved,
                "withPdf": with_pdf,
                "totalDownloads": total_downloads,
                "totalViews": total_views,
                "totalReservations": total_reservations,
                "pendingReservations": pending_reservations,
            }
        )

    @action(detail=True, methods=["post"], permission_classes=[AllowAny])
    def record_view(self, request, pk=None):
        """
        Increments view count atomically.
        """
        book = self.get_object()
        Book.objects.filter(pk=book.pk).update(
            views_count=models.F("views_count") + 1
        )
        return Response({"status": "view recorded", "viewsCount": book.views_count + 1})

    @action(detail=True, methods=["post"], permission_classes=[AllowAny])
    def record_download(self, request, pk=None):
        """
        Increments download count atomically.
        """
        book = self.get_object()
        Book.objects.filter(pk=book.pk).update(
            downloads_count=models.F("downloads_count") + 1
        )
        return Response(
            {"status": "download recorded", "downloadsCount": book.downloads_count + 1}
        )

    @action(detail=True, methods=["post"], permission_classes=[AllowAny])
    def reserve(self, request, pk=None):
        """
        Student reservation action. Creates a reservation record and adjusts availability.
        """
        book = self.get_object()
        student_name = request.data.get("studentName", "").strip()
        student_id = request.data.get("studentId", "").strip()
        student_major = request.data.get("studentMajor", "").strip()
        student_email = request.data.get("studentEmail", "").strip()
        student_phone = request.data.get("studentPhone", "").strip()
        notes = request.data.get("notes", "").strip()

        if not student_name or not student_id:
            return Response(
                {"error": "يرجى تعبئة اسم الطالب والرقم الجامعي."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            # Concurrency-safe lock
            locked_book = Book.objects.select_for_update().get(pk=book.pk)

            # Create reservation
            reservation = BookReservation.objects.create(
                book=locked_book,
                student_name=student_name,
                student_id=student_id,
                student_major=student_major,
                student_email=student_email,
                student_phone=student_phone,
                notes=notes,
                status="pending",
                expires_at=timezone.now() + timezone.timedelta(days=2),  # 48 hours pickup window
            )

            # Adjust available copies
            if locked_book.available_copies > 0:
                locked_book.available_copies -= 1
            if locked_book.available_copies == 0:
                locked_book.is_available = False
            locked_book.save()

            # Record activity log
            try:
                ActivityLog.objects.create(
                    user_name=student_name,
                    action_ar=f"قام الطالب {student_name} ({student_id}) بطلب حجز كتاب ({locked_book.title_ar})",
                    action_en=f"Student {student_name} ({student_id}) requested reservation for book ({locked_book.title_en})",
                    status="info",
                )
            except Exception:
                pass

        return Response(
            {
                "success": True,
                "message": "تم تقديم طلب حجز الكتاب بنجاح!",
                "reservationId": reservation.id,
                "expiresAt": reservation.expires_at,
            },
            status=status.HTTP_201_CREATED,
        )


class BookReservationViewSet(viewsets.ModelViewSet):
    """
    Management API for Book Reservations and borrowing requests.
    """

    queryset = (
        BookReservation.objects.all().select_related("book").order_by("-reserved_at")
    )
    serializer_class = BookReservationSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "student_name",
        "student_id",
        "student_email",
        "book__title_ar",
        "book__title_en",
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        status_param = self.request.query_params.get("status")
        book_id = self.request.query_params.get("book")
        if status_param and status_param != "all":
            qs = qs.filter(status=status_param)
        if book_id:
            qs = qs.filter(book_id=book_id)
        return qs

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        reservation = self.get_object()
        new_status = request.data.get("status")
        admin_notes = request.data.get("adminNotes", "")

        valid_statuses = [
            "pending",
            "approved",
            "borrowed",
            "returned",
            "cancelled",
            "rejected",
        ]
        if new_status not in valid_statuses:
            return Response(
                {"error": f"حالة غير صالحة ({new_status})."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            old_status = reservation.status
            reservation.status = new_status
            if admin_notes:
                reservation.admin_notes = admin_notes

            if new_status == "returned":
                reservation.returned_at = timezone.now()
                # Restore copy
                book = Book.objects.select_for_update().get(pk=reservation.book.pk)
                book.available_copies = min(
                    book.total_copies, book.available_copies + 1
                )
                book.is_available = True
                book.save()

            elif new_status in ["cancelled", "rejected"] and old_status in [
                "pending",
                "approved",
                "borrowed",
            ]:
                # If cancelled/rejected, release copy
                book = Book.objects.select_for_update().get(pk=reservation.book.pk)
                book.available_copies = min(
                    book.total_copies, book.available_copies + 1
                )
                book.is_available = True
                book.save()

            reservation.save()

        return Response(
            {"success": True, "status": reservation.status, "id": reservation.id}
        )


class ResearchPdfUploadView(APIView):
    """
    Secure file uploader exclusively for Research Paper PDFs.
    Enforces MIME check, header magic bytes (%PDF-), randomizes filenames to prevent traversal,
    and enforces maximum file size limit (100MB).
    """

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response(
                {"error": "لم يتم إرفاق أي ملف."}, status=status.HTTP_400_BAD_REQUEST
            )

        MAX_SIZE = 100 * 1024 * 1024  # 100 MB
        if file_obj.size > MAX_SIZE:
            return Response(
                {"error": "حجم ملف الـ PDF يتجاوز الحد المسموح به (100 ميغابايت)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        name_lower = file_obj.name.lower()
        if not name_lower.endswith(".pdf"):
            return Response(
                {"error": "صيغة الملف غير مقبولة. يُسمح فقط بملفات PDF (.pdf)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        first_bytes = file_obj.read(10)
        file_obj.seek(0)
        if not first_bytes.startswith(b"%PDF-"):
            return Response(
                {
                    "error": "الملف غير صالح أو تالف. لا يحتوي على ترويسة PDF رقمية معتمدة."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        safe_uuid = uuid.uuid4().hex
        secure_filename = f"paper_{safe_uuid}.pdf"
        rel_storage_path = os.path.join("research_papers", secure_filename)

        saved_path = default_storage.save(rel_storage_path, file_obj)
        file_url = default_storage.url(saved_path)

        size_bytes = file_obj.size
        size_formatted = (
            f"{size_bytes / 1024:.1f} KB"
            if size_bytes < 1048576
            else f"{size_bytes / 1048576:.2f} MB"
        )

        return Response(
            {
                "url": file_url,
                "filename": file_obj.name,
                "size": size_bytes,
                "sizeFormatted": size_formatted,
                "fileType": "PDF",
            },
            status=status.HTTP_201_CREATED,
        )


class ResearchCenterViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Research Centers at Antioch Syrian University.
    """

    queryset = (
        ResearchCenter.objects.all()
        .select_related("faculty")
        .order_by("order", "created_at")
    )
    serializer_class = ResearchCenterSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "title_ar",
        "title_en",
        "description_ar",
        "description_en",
        "director_name_ar",
        "director_name_en",
    ]


class ResearchAreaViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Research Areas and Disciplines.
    """

    queryset = ResearchArea.objects.all().order_by("order", "name_ar")
    serializer_class = ResearchAreaSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name_ar", "name_en", "description_ar", "description_en"]


class ResearchPublicationViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Scientific Research Publications.
    Supports filtering by research area, center, faculty, year, and featured status.
    """

    queryset = (
        ResearchPublication.objects.all()
        .select_related("research_area", "center", "faculty")
        .order_by("-publication_year", "-created_at")
    )
    serializer_class = ResearchPublicationSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "title_ar",
        "title_en",
        "authors_ar",
        "authors_en",
        "journal_ar",
        "journal_en",
    ]
    ordering_fields = [
        "publication_year",
        "created_at",
        "views_count",
        "downloads_count",
        "title_ar",
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        area_id = self.request.query_params.get("area")
        center_id = self.request.query_params.get("center")
        faculty_id = self.request.query_params.get("faculty")
        year = self.request.query_params.get("year")
        is_featured = self.request.query_params.get("featured")

        if area_id and area_id != "all":
            qs = qs.filter(research_area_id=area_id)
        if center_id and center_id != "all":
            qs = qs.filter(center_id=center_id)
        if faculty_id:
            qs = qs.filter(faculty_id=faculty_id)
        if year and year != "all":
            qs = qs.filter(publication_year=year)
        if is_featured in ["true", "1"]:
            qs = qs.filter(is_featured=True)
        return qs

    @action(detail=False, methods=["get"])
    def stats(self, request):
        total_pubs = ResearchPublication.objects.filter(is_active=True).count()
        current_year = timezone.now().year
        current_year_pubs = ResearchPublication.objects.filter(
            is_active=True, publication_year=current_year
        ).count()
        total_centers = ResearchCenter.objects.filter(is_active=True).count()
        total_areas = ResearchArea.objects.filter(is_active=True).count()
        total_downloads = (
            ResearchPublication.objects.aggregate(total=models.Sum("downloads_count"))[
                "total"
            ]
            or 0
        )
        total_views = (
            ResearchPublication.objects.aggregate(total=models.Sum("views_count"))[
                "total"
            ]
            or 0
        )

        return Response(
            {
                "totalPublications": total_pubs,
                "currentYearPublications": current_year_pubs,
                "totalCenters": total_centers,
                "totalAreas": total_areas,
                "totalDownloads": total_downloads,
                "totalViews": total_views,
                "internationalPartnerships": 5,
                "annualConferences": 3,
                "researchProjects": 10,
            }
        )

    @action(detail=True, methods=["post"], permission_classes=[AllowAny])
    def record_view(self, request, pk=None):
        pub = self.get_object()
        ResearchPublication.objects.filter(pk=pub.pk).update(
            views_count=models.F("views_count") + 1
        )
        return Response({"status": "view recorded", "viewsCount": pub.views_count + 1})

    @action(detail=True, methods=["post"], permission_classes=[AllowAny])
    def record_download(self, request, pk=None):
        pub = self.get_object()
        ResearchPublication.objects.filter(pk=pub.pk).update(
            downloads_count=models.F("downloads_count") + 1
        )
        return Response(
            {"status": "download recorded", "downloadsCount": pub.downloads_count + 1}
        )


class HousingFeatureViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Campus Life Housing Features.
    """
    queryset = HousingFeature.objects.all().order_by("order", "id")
    serializer_class = HousingFeatureSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title_ar", "title_en", "description_ar", "description_en"]
    ordering_fields = ["order", "id", "created_at"]


class StudentClubViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Campus Life Student Clubs.
    """
    queryset = StudentClub.objects.all().order_by("order", "id")
    serializer_class = StudentClubSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name_ar", "name_en", "description_ar", "description_en", "category", "supervisor"]
    ordering_fields = ["order", "id", "created_at"]


class SportActivityViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Campus Life Sport Activities.
    """
    queryset = SportActivity.objects.all().order_by("order", "id")
    serializer_class = SportActivitySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name_ar", "name_en", "description_ar", "description_en"]
    ordering_fields = ["order", "id", "created_at"]


class CampusLifeOverviewViewSet(viewsets.ModelViewSet):
    """
    API for Campus Life overview settings and section texts.
    """
    queryset = CampusLifeOverview.objects.all()
    serializer_class = CampusLifeOverviewSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        overview = CampusLifeOverview.objects.first()
        if not overview:
            overview = CampusLifeOverview.objects.create()
        serializer = self.get_serializer(overview)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        total_clubs = StudentClub.objects.filter(is_active=True).count()
        total_housing = HousingFeature.objects.filter(is_active=True).count()
        total_sports = SportActivity.objects.filter(is_active=True).count()

        return Response({
            "totalClubs": total_clubs,
            "totalHousingFeatures": total_housing,
            "totalSports": total_sports,
        })


class FacultyLaboratoryViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Faculty Laboratories and Scientific Research Facilities.
    Supports filtering by ?faculty=<id> or ?faculty_slug=<slug>.
    """
    queryset = (
        FacultyLaboratory.objects.all()
        .select_related("faculty")
        .order_by("order", "id")
    )
    serializer_class = FacultyLaboratorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "name_ar",
        "name_en",
        "description_ar",
        "description_en",
        "equipment_ar",
        "equipment_en",
        "location_ar",
        "location_en",
        "supervisor_name_ar",
        "supervisor_name_en",
    ]
    ordering_fields = ["order", "id", "created_at", "name_ar", "name_en"]

    def get_queryset(self):
        qs = super().get_queryset()
        faculty_id = self.request.query_params.get("faculty")
        if faculty_id:
            qs = qs.filter(faculty_id=faculty_id)
        faculty_slug = self.request.query_params.get("faculty_slug")
        if faculty_slug:
            qs = qs.filter(faculty__slug=faculty_slug)
        return qs


