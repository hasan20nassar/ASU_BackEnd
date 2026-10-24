from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field
import re
import uuid
from django.utils.text import slugify
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

User = get_user_model()


def sanitize_slug(slug_val, name_en="", name_ar="", default_prefix="item"):
    """
    Sanitizes a slug by removing leading/trailing slashes and whitespace,
    and converting non-alphanumeric characters to hyphens.
    Falls back to slugified English name, Arabic name, or a unique ID.
    """
    if slug_val and isinstance(slug_val, str):
        cleaned = slug_val.strip("/ \t\r\n")
        cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", cleaned).strip("-_").lower()
        if cleaned:
            return cleaned

    if name_en and isinstance(name_en, str):
        cleaned = slugify(name_en)
        if cleaned:
            return cleaned

    if name_ar and isinstance(name_ar, str):
        cleaned = slugify(name_ar)
        if cleaned:
            return cleaned

    return f"{default_prefix}-{uuid.uuid4().hex[:6]}"


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source="id", read_only=True)
    nameAr = serializers.CharField(source="name_ar")
    nameEn = serializers.CharField(
        source="name_en", required=False, allow_blank=True, default=""
    )
    assignedFaculty = serializers.PrimaryKeyRelatedField(
        source="assigned_faculty",
        queryset=Faculty.objects.all(),
        required=False,
        allow_null=True,
    )
    assignedFacultyName = serializers.CharField(
        source="assigned_faculty.name_ar", read_only=True
    )
    assignedFaculties = serializers.PrimaryKeyRelatedField(
        source="assigned_faculties",
        queryset=Faculty.objects.all(),
        many=True,
        required=False,
    )
    birthDate = serializers.DateField(
        source="birth_date", required=False, allow_null=True
    )
    bio = serializers.CharField(required=False, allow_blank=True, default="")
    password = serializers.CharField(
        write_only=True, required=False, allow_blank=True, default=""
    )
    isActive = serializers.BooleanField(
        source="is_active", required=False, default=True
    )
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user",
            "nameAr",
            "nameEn",
            "email",
            "password",
            "birthDate",
            "bio",
            "role",
            "assignedFaculty",
            "assignedFacultyName",
            "assignedFaculties",
            "phone",
            "avatar",
            "isActive",
            "createdAt",
        ]


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="email", read_only=True)
    first_name = serializers.CharField(source="name_ar", read_only=True)
    last_name = serializers.CharField(source="name_en", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "pk",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "role",
            "avatar",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "username", "email", "name_ar", "name_en", "role"]


class CourseSerializer(serializers.ModelSerializer):
    nameAr = serializers.CharField(source="name_ar")
    nameEn = serializers.CharField(source="name_en")
    program = serializers.PrimaryKeyRelatedField(
        queryset=Program.objects.all(), required=False, allow_null=True
    )
    programNameAr = serializers.CharField(source="program.name_ar", read_only=True)
    programNameEn = serializers.CharField(source="program.name_en", read_only=True)
    descriptionAr = serializers.CharField(
        source="description_ar", required=False, allow_blank=True, default=""
    )
    descriptionEn = serializers.CharField(
        source="description_en", required=False, allow_blank=True, default=""
    )
    prerequisitesText = serializers.CharField(
        source="prerequisites_text", required=False, allow_blank=True, default=""
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "code",
            "nameAr",
            "nameEn",
            "credits",
            "program",
            "programNameAr",
            "programNameEn",
            "year",
            "semester",
            "descriptionAr",
            "descriptionEn",
            "prerequisitesText",
        ]


class ProgramSerializer(serializers.ModelSerializer):
    facultySlug = serializers.CharField(source="faculty.slug", read_only=True)
    facultyNameAr = serializers.CharField(source="faculty.name_ar", read_only=True)
    facultyNameEn = serializers.CharField(source="faculty.name_en", read_only=True)
    nameAr = serializers.CharField(source="name_ar")
    nameEn = serializers.CharField(
        source="name_en", required=False, allow_blank=True, default=""
    )
    descriptionAr = serializers.CharField(
        source="description_ar", required=False, allow_blank=True, default=""
    )
    descriptionEn = serializers.CharField(
        source="description_en", required=False, allow_blank=True, default=""
    )
    creditHours = serializers.IntegerField(
        source="credit_hours", required=False, default=160
    )
    minScorePercent = serializers.IntegerField(
        source="min_score_percent", required=False, default=60
    )
    minScorePoints = serializers.IntegerField(
        source="min_score_points", required=False, default=120
    )
    tuitionSyrian = serializers.IntegerField(
        source="tuition_syrian", required=False, default=0
    )
    tuitionNonResident = serializers.IntegerField(
        source="tuition_non_resident", required=False, default=1500
    )
    tuitionCurrency = serializers.SerializerMethodField(read_only=True)
    head = serializers.PrimaryKeyRelatedField(
        queryset=FacultyMember.objects.all(), required=False, allow_null=True
    )
    headDetail = serializers.SerializerMethodField(read_only=True)
    teachersCount = serializers.SerializerMethodField(read_only=True)
    totalStudents = serializers.SerializerMethodField(read_only=True)
    courses = CourseSerializer(many=True, read_only=True)

    mottoAr = serializers.CharField(
        source="motto_ar",
        required=False,
        allow_blank=True,
        default="نحو التميز الأكاديمي والمهني",
    )
    mottoEn = serializers.CharField(
        source="motto_en",
        required=False,
        allow_blank=True,
        default="Towards Academic & Professional Excellence",
    )
    primaryColor = serializers.CharField(
        source="primary_color", required=False, default="#1E3A8A"
    )
    accentColor = serializers.CharField(
        source="accent_color", required=False, default="#F59E0B"
    )
    heroBanner = serializers.CharField(
        source="hero_banner", required=False, allow_blank=True, default=""
    )
    logoUrl = serializers.CharField(
        source="logo_url", required=False, allow_blank=True, default=""
    )
    headNameAr = serializers.CharField(
        source="head_name_ar", required=False, allow_blank=True, default=""
    )
    headNameEn = serializers.CharField(
        source="head_name_en", required=False, allow_blank=True, default=""
    )
    headMessageAr = serializers.CharField(
        source="head_message_ar", required=False, allow_blank=True, default=""
    )
    headMessageEn = serializers.CharField(
        source="head_message_en", required=False, allow_blank=True, default=""
    )
    headPhoto = serializers.CharField(
        source="head_photo", required=False, allow_blank=True, default=""
    )
    establishedYear = serializers.IntegerField(
        source="established_year", required=False, default=2005
    )
    studentsCount = serializers.IntegerField(
        source="students_count", required=False, default=350
    )
    labsCount = serializers.IntegerField(
        source="labs_count", required=False, default=6
    )
    researchPapersCount = serializers.IntegerField(
        source="research_papers_count", required=False, default=80
    )
    employmentRate = serializers.IntegerField(
        source="employment_rate", required=False, default=90
    )
    facilities = serializers.JSONField(required=False)
    careerPaths = serializers.CharField(
        source="career_paths", required=False, allow_blank=True, default=""
    )
    guideDocumentUrl = serializers.CharField(
        source="guide_document_url", required=False, allow_blank=True, default=""
    )
    layoutConfig = serializers.JSONField(
        source="layout_config", required=False
    )

    class Meta:
        model = Program
        fields = [
            "id",
            "slug",
            "faculty",
            "facultySlug",
            "facultyNameAr",
            "facultyNameEn",
            "nameAr",
            "nameEn",
            "descriptionAr",
            "descriptionEn",
            "mottoAr",
            "mottoEn",
            "primaryColor",
            "accentColor",
            "heroBanner",
            "logoUrl",
            "creditHours",
            "minScorePercent",
            "minScorePoints",
            "tuitionSyrian",
            "tuitionNonResident",
            "tuitionCurrency",
            "branch",
            "duration",
            "head",
            "headDetail",
            "headNameAr",
            "headNameEn",
            "headMessageAr",
            "headMessageEn",
            "headPhoto",
            "establishedYear",
            "studentsCount",
            "labsCount",
            "researchPapersCount",
            "employmentRate",
            "facilities",
            "careerPaths",
            "guideDocumentUrl",
            "layoutConfig",
            "teachersCount",
            "totalStudents",
            "courses",
        ]

    @extend_schema_field(serializers.DictField(child=serializers.CharField()))
    def get_tuitionCurrency(self, obj):
        return {"syrian": "SYP", "nonResident": "USD"}

    @extend_schema_field(serializers.DictField())
    def get_headDetail(self, obj):
        if obj.head:
            return {
                "id": obj.head.id,
                "nameAr": obj.head.name_ar,
                "nameEn": obj.head.name_en,
                "email": obj.head.email,
            }
        return None

    @extend_schema_field(serializers.IntegerField())
    def get_teachersCount(self, obj):
        if hasattr(obj, "teachers_count"):
            return obj.teachers_count
        return obj.teachers.count()

    @extend_schema_field(serializers.IntegerField())
    def get_totalStudents(self, obj):
        if hasattr(obj, "total_students"):
            return obj.total_students
        return obj.students.count()

    def to_internal_value(self, data):
        ret_data = data.copy() if hasattr(data, "copy") else dict(data)
        slug_val = ret_data.get("slug")
        name_en = ret_data.get("nameEn") or ret_data.get("name_en") or ""
        name_ar = ret_data.get("nameAr") or ret_data.get("name_ar") or ""
        ret_data["slug"] = sanitize_slug(
            slug_val, name_en=name_en, name_ar=name_ar, default_prefix="program"
        )
        if not ret_data.get("nameEn") and not ret_data.get("name_en"):
            ret_data["nameEn"] = name_ar
        desc_ar = ret_data.get("descriptionAr") or ret_data.get("description_ar") or ""
        desc_en = ret_data.get("descriptionEn") or ret_data.get("description_en") or ""
        if not desc_ar:
            ret_data["descriptionAr"] = f"قسم {name_ar}" if name_ar else "قسم أكاديمي"
        if not desc_en:
            ret_data["descriptionEn"] = (
                f"Department of {name_en or name_ar}"
                if (name_en or name_ar)
                else "Academic Department"
            )
        return super().to_internal_value(ret_data)


class FacultyLaboratorySerializer(serializers.ModelSerializer):
    nameAr = serializers.CharField(source="name_ar")
    nameEn = serializers.CharField(
        source="name_en", required=False, allow_blank=True, default=""
    )
    descriptionAr = serializers.CharField(
        source="description_ar", required=False, allow_blank=True, default=""
    )
    descriptionEn = serializers.CharField(
        source="description_en", required=False, allow_blank=True, default=""
    )
    equipmentAr = serializers.CharField(
        source="equipment_ar", required=False, allow_blank=True, default=""
    )
    equipmentEn = serializers.CharField(
        source="equipment_en", required=False, allow_blank=True, default=""
    )
    locationAr = serializers.CharField(
        source="location_ar", required=False, allow_blank=True, default=""
    )
    locationEn = serializers.CharField(
        source="location_en", required=False, allow_blank=True, default=""
    )
    supervisorNameAr = serializers.CharField(
        source="supervisor_name_ar", required=False, allow_blank=True, default=""
    )
    supervisorNameEn = serializers.CharField(
        source="supervisor_name_en", required=False, allow_blank=True, default=""
    )
    isActive = serializers.BooleanField(source="is_active", required=False, default=True)

    class Meta:
        model = FacultyLaboratory
        fields = [
            "id",
            "faculty",
            "nameAr",
            "nameEn",
            "descriptionAr",
            "descriptionEn",
            "equipmentAr",
            "equipmentEn",
            "image",
            "locationAr",
            "locationEn",
            "capacity",
            "supervisorNameAr",
            "supervisorNameEn",
            "order",
            "isActive",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class FacultySerializer(serializers.ModelSerializer):
    nameAr = serializers.CharField(source="name_ar")
    nameEn = serializers.CharField(
        source="name_en", required=False, allow_blank=True, default=""
    )
    descriptionAr = serializers.CharField(
        source="description_ar", required=False, allow_blank=True, default=""
    )
    descriptionEn = serializers.CharField(
        source="description_en", required=False, allow_blank=True, default=""
    )
    mottoAr = serializers.CharField(
        source="motto_ar",
        required=False,
        allow_blank=True,
        default="الصرح الأكاديمي والبحثي الرائد",
    )
    mottoEn = serializers.CharField(
        source="motto_en",
        required=False,
        allow_blank=True,
        default="Pioneering Academic & Research Excellence",
    )
    primaryColor = serializers.CharField(
        source="primary_color", required=False, default="#800000"
    )
    accentColor = serializers.CharField(
        source="accent_color", required=False, default="#D4AF37"
    )
    heroBanner = serializers.CharField(
        source="hero_banner", required=False, allow_blank=True, default=""
    )
    logoUrl = serializers.CharField(
        source="logo_url", required=False, allow_blank=True, default=""
    )
    deanNameAr = serializers.CharField(
        source="dean_name_ar", required=False, allow_blank=True, default=""
    )
    deanNameEn = serializers.CharField(
        source="dean_name_en", required=False, allow_blank=True, default=""
    )
    deanMessageAr = serializers.CharField(
        source="dean_message_ar", required=False, allow_blank=True, default=""
    )
    deanMessageEn = serializers.CharField(
        source="dean_message_en", required=False, allow_blank=True, default=""
    )
    deanPhoto = serializers.CharField(
        source="dean_photo", required=False, allow_blank=True, default=""
    )
    establishedYear = serializers.IntegerField(
        source="established_year", required=False, default=2005
    )
    studentsCount = serializers.IntegerField(
        source="students_count", required=False, default=1200
    )
    labsCount = serializers.IntegerField(
        source="labs_count", required=False, default=12
    )
    researchPapersCount = serializers.IntegerField(
        source="research_papers_count", required=False, default=250
    )
    employmentRate = serializers.IntegerField(
        source="employment_rate", required=False, default=92
    )
    guideDocumentUrl = serializers.CharField(
        source="guide_document_url", required=False, allow_blank=True, default=""
    )
    layoutConfig = serializers.JSONField(
        source="layout_config", required=False
    )
    programs = ProgramSerializer(many=True, read_only=True)
    laboratories = FacultyLaboratorySerializer(many=True, read_only=True)
    facilities = serializers.SerializerMethodField()
    dean = serializers.PrimaryKeyRelatedField(
        queryset=FacultyMember.objects.all(), required=False, allow_null=True
    )
    deanDetail = serializers.SerializerMethodField(read_only=True)
    totalPrograms = serializers.SerializerMethodField(read_only=True)
    totalTeachers = serializers.SerializerMethodField(read_only=True)
    totalStudents = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Faculty
        fields = [
            "id",
            "slug",
            "nameAr",
            "nameEn",
            "descriptionAr",
            "descriptionEn",
            "icon",
            "color",
            "image",
            "mottoAr",
            "mottoEn",
            "primaryColor",
            "accentColor",
            "heroBanner",
            "logoUrl",
            "dean",
            "deanDetail",
            "deanNameAr",
            "deanNameEn",
            "deanMessageAr",
            "deanMessageEn",
            "deanPhoto",
            "establishedYear",
            "studentsCount",
            "labsCount",
            "researchPapersCount",
            "employmentRate",
            "facilities",
            "laboratories",
            "guideDocumentUrl",
            "layoutConfig",
            "programs",
            "totalPrograms",
            "totalTeachers",
            "totalStudents",
        ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_facilities(self, obj):
        labs = obj.laboratories.filter(is_active=True).order_by("order", "id")
        if labs.exists():
            return [
                {
                    "id": lab.id,
                    "nameAr": lab.name_ar,
                    "nameEn": lab.name_en or lab.name_ar,
                    "descriptionAr": lab.description_ar,
                    "descriptionEn": lab.description_en or lab.description_ar,
                    "equipmentAr": lab.equipment_ar,
                    "equipmentEn": lab.equipment_en,
                    "locationAr": lab.location_ar,
                    "locationEn": lab.location_en,
                    "capacity": lab.capacity,
                    "supervisorNameAr": lab.supervisor_name_ar,
                    "supervisorNameEn": lab.supervisor_name_en,
                    "image": lab.image,
                }
                for lab in labs
            ]
        return obj.facilities or []

    @extend_schema_field(serializers.DictField())
    def get_deanDetail(self, obj):
        if obj.dean:
            return {
                "id": obj.dean.id,
                "nameAr": obj.dean.name_ar,
                "nameEn": obj.dean.name_en,
                "email": obj.dean.email,
            }
        if obj.dean_name_ar or obj.dean_name_en:
            return {
                "id": 0,
                "nameAr": obj.dean_name_ar,
                "nameEn": obj.dean_name_en,
                "email": "",
            }
        return None

    @extend_schema_field(serializers.IntegerField())
    def get_totalPrograms(self, obj):
        if hasattr(obj, "total_programs"):
            return obj.total_programs
        return obj.programs.count()

    @extend_schema_field(serializers.IntegerField())
    def get_totalTeachers(self, obj):
        if hasattr(obj, "total_teachers"):
            return obj.total_teachers
        return obj.members.count()

    @extend_schema_field(serializers.IntegerField())
    def get_totalStudents(self, obj):
        if hasattr(obj, "total_students"):
            return obj.total_students
        return obj.students.count()

    def to_internal_value(self, data):
        ret_data = data.copy() if hasattr(data, "copy") else dict(data)
        if "layoutConfig" in ret_data:
            ret_data["layout_config"] = ret_data["layoutConfig"]
        slug_val = ret_data.get("slug")
        name_en = ret_data.get("nameEn") or ret_data.get("name_en") or ""
        name_ar = ret_data.get("nameAr") or ret_data.get("name_ar") or ""
        ret_data["slug"] = sanitize_slug(
            slug_val, name_en=name_en, name_ar=name_ar, default_prefix="faculty"
        )
        if not ret_data.get("nameEn") and not ret_data.get("name_en"):
            ret_data["nameEn"] = name_ar
        desc_ar = ret_data.get("descriptionAr") or ret_data.get("description_ar") or ""
        desc_en = ret_data.get("descriptionEn") or ret_data.get("description_en") or ""
        if not desc_ar:
            ret_data["descriptionAr"] = (
                f"كلية {name_ar}" if name_ar else "كلية أكاديمية"
            )
        if not desc_en:
            ret_data["descriptionEn"] = (
                f"Faculty of {name_en or name_ar}"
                if (name_en or name_ar)
                else "Academic Faculty"
            )
        return super().to_internal_value(ret_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if request and "facilities" in request.data:
            raw_facilities = request.data.get("facilities")
            if isinstance(raw_facilities, list):
                instance.facilities = raw_facilities
                # Sync directly to FacultyLaboratory database rows
                FacultyLaboratory.objects.filter(faculty=instance).delete()
                for idx, item in enumerate(raw_facilities):
                    if isinstance(item, dict) and (item.get("nameAr") or item.get("name_ar")):
                        FacultyLaboratory.objects.create(
                            faculty=instance,
                            name_ar=item.get("nameAr") or item.get("name_ar") or "",
                            name_en=item.get("nameEn") or item.get("name_en") or "",
                            description_ar=item.get("descriptionAr") or item.get("description_ar") or "",
                            description_en=item.get("descriptionEn") or item.get("description_en") or "",
                            equipment_ar=item.get("equipmentAr") or item.get("equipment_ar") or "",
                            equipment_en=item.get("equipmentEn") or item.get("equipment_en") or "",
                            image=item.get("image") or "",
                            order=idx,
                        )
                validated_data["labs_count"] = len(raw_facilities)
        return super().update(instance, validated_data)


class FacultyMemberSerializer(serializers.ModelSerializer):
    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), required=False, allow_null=True
    )
    facultySlug = serializers.CharField(source="faculty.slug", read_only=True)
    facultyNameAr = serializers.CharField(source="faculty.name_ar", read_only=True)
    facultyNameEn = serializers.CharField(source="faculty.name_en", read_only=True)
    department = serializers.PrimaryKeyRelatedField(
        queryset=Program.objects.all(), required=False, allow_null=True
    )
    departmentNameAr = serializers.CharField(
        source="department.name_ar", read_only=True
    )
    departmentNameEn = serializers.CharField(
        source="department.name_en", read_only=True
    )
    departmentDetail = serializers.SerializerMethodField(read_only=True)
    nameAr = serializers.CharField(source="name_ar")
    nameEn = serializers.CharField(source="name_en")
    titleAr = serializers.CharField(source="title_ar")
    titleEn = serializers.CharField(source="title_en")
    departmentAr = serializers.CharField(
        source="department_ar", required=False, allow_blank=True
    )
    departmentEn = serializers.CharField(
        source="department_en", required=False, allow_blank=True
    )
    descriptionAr = serializers.CharField(
        source="description_ar", required=False, allow_blank=True, default=""
    )
    descriptionEn = serializers.CharField(
        source="description_en", required=False, allow_blank=True, default=""
    )
    officeHours = serializers.CharField(
        source="office_hours", required=False, allow_blank=True, default=""
    )
    locationAr = serializers.CharField(
        source="location_ar", required=False, allow_blank=True, default=""
    )
    locationEn = serializers.CharField(
        source="location_en", required=False, allow_blank=True, default=""
    )
    image = serializers.CharField(required=False, allow_blank=True, default="/user.png")
    isHead = serializers.BooleanField(source="is_head", required=False, default=False)
    bioAr = serializers.CharField(
        source="bio_ar", required=False, allow_blank=True, default=""
    )
    bioEn = serializers.CharField(
        source="bio_en", required=False, allow_blank=True, default=""
    )
    educationAr = serializers.JSONField(
        source="education_ar", required=False, default=list
    )
    educationEn = serializers.JSONField(
        source="education_en", required=False, default=list
    )
    researchAr = serializers.CharField(
        source="research_ar", required=False, allow_blank=True, default=""
    )
    researchEn = serializers.CharField(
        source="research_en", required=False, allow_blank=True, default=""
    )
    publications = serializers.JSONField(required=False, default=list)
    officeHourSlots = serializers.JSONField(
        source="office_hour_slots", required=False, default=list
    )
    appointmentLocation = serializers.CharField(
        source="appointment_location", required=False, allow_blank=True, default=""
    )

    class Meta:
        model = FacultyMember
        fields = [
            "id",
            "faculty",
            "facultySlug",
            "facultyNameAr",
            "facultyNameEn",
            "department",
            "departmentNameAr",
            "departmentNameEn",
            "departmentDetail",
            "nameAr",
            "nameEn",
            "titleAr",
            "titleEn",
            "departmentAr",
            "departmentEn",
            "descriptionAr",
            "descriptionEn",
            "email",
            "officeHours",
            "locationAr",
            "locationEn",
            "image",
            "isHead",
            "bioAr",
            "bioEn",
            "educationAr",
            "educationEn",
            "researchAr",
            "researchEn",
            "publications",
            "officeHourSlots",
            "appointmentLocation",
        ]

    @extend_schema_field(serializers.DictField())
    def get_departmentDetail(self, obj):
        if obj.department:
            return {
                "id": obj.department.id,
                "nameAr": obj.department.name_ar,
                "nameEn": obj.department.name_en,
                "slug": obj.department.slug,
            }
        return None

    def validate(self, attrs):
        department = attrs.get("department") or (
            self.instance.department if self.instance else None
        )
        faculty = attrs.get("faculty") or (
            self.instance.faculty if self.instance else None
        )

        if department and department.faculty:
            # Auto-derive faculty from department
            attrs["faculty"] = department.faculty
            # Auto-sync text fields for backward compatibility
            attrs["department_ar"] = department.name_ar
            attrs["department_en"] = department.name_en
        elif faculty and department and department.faculty_id != faculty.id:
            raise serializers.ValidationError(
                {"department": "القسم المختار لا ينتمي إلى الكلية المحددة للمدرس."}
            )
        return attrs

    def create(self, validated_data):
        # Fallback to finding faculty if not directly provided
        if not validated_data.get("faculty"):
            if (
                validated_data.get("department")
                and validated_data["department"].faculty
            ):
                validated_data["faculty"] = validated_data["department"].faculty
            else:
                faculty_slug = self.initial_data.get("facultySlug")
                if faculty_slug:
                    faculty_obj = Faculty.objects.filter(slug=faculty_slug).first()
                    if faculty_obj:
                        validated_data["faculty"] = faculty_obj
                if not validated_data.get("faculty"):
                    # Default to first faculty if available
                    first_fac = Faculty.objects.first()
                    if first_fac:
                        validated_data["faculty"] = first_fac
        return super().create(validated_data)


class FacultyAppointmentSerializer(serializers.ModelSerializer):
    facultyMember = serializers.PrimaryKeyRelatedField(
        source="faculty_member", queryset=FacultyMember.objects.all()
    )
    facultyMemberNameAr = serializers.CharField(
        source="faculty_member.name_ar", read_only=True
    )
    facultyMemberNameEn = serializers.CharField(
        source="faculty_member.name_en", read_only=True
    )
    studentName = serializers.CharField(source="student_name")
    studentEmail = serializers.CharField(source="student_email")
    studentId = serializers.CharField(
        source="student_id", required=False, allow_blank=True, default=""
    )
    dayAr = serializers.CharField(source="day_ar")
    dayEn = serializers.CharField(source="day_en")
    timeSlot = serializers.CharField(source="time_slot")
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = FacultyAppointment
        fields = [
            "id",
            "facultyMember",
            "facultyMemberNameAr",
            "facultyMemberNameEn",
            "studentName",
            "studentEmail",
            "studentId",
            "dayAr",
            "dayEn",
            "timeSlot",
            "reason",
            "status",
            "createdAt",
        ]


class AlumniStorySerializer(serializers.ModelSerializer):
    facultySlug = serializers.CharField(source="faculty.slug", read_only=True)
    nameAr = serializers.CharField(source="name_ar")
    nameEn = serializers.CharField(source="name_en")
    graduationYear = serializers.IntegerField(source="graduation_year")
    programAr = serializers.CharField(source="program_ar")
    programEn = serializers.CharField(source="program_en")
    currentRoleAr = serializers.CharField(source="current_role_ar")
    currentRoleEn = serializers.CharField(source="current_role_en")
    companyAr = serializers.CharField(source="company_ar")
    companyEn = serializers.CharField(source="company_en")
    storyAr = serializers.CharField(source="story_ar")
    storyEn = serializers.CharField(source="story_en")

    class Meta:
        model = AlumniStory
        fields = [
            "id",
            "faculty",
            "facultySlug",
            "nameAr",
            "nameEn",
            "graduationYear",
            "programAr",
            "programEn",
            "currentRoleAr",
            "currentRoleEn",
            "companyAr",
            "companyEn",
            "storyAr",
            "storyEn",
            "image",
        ]


class ScheduleItemSerializer(serializers.ModelSerializer):
    courseCode = serializers.CharField(source="course.code", read_only=True)
    courseNameAr = serializers.CharField(source="course.name_ar", read_only=True)
    courseNameEn = serializers.CharField(source="course.name_en", read_only=True)
    dayAr = serializers.CharField(source="day_ar")
    dayEn = serializers.CharField(source="day_en")
    instructorEn = serializers.CharField(source="instructor_en")

    class Meta:
        model = ScheduleItem
        fields = [
            "id",
            "course",
            "courseCode",
            "courseNameAr",
            "courseNameEn",
            "day",
            "dayAr",
            "dayEn",
            "time",
            "room",
            "instructor",
            "instructorEn",
        ]


class StudentGradeSerializer(serializers.ModelSerializer):
    courseCode = serializers.CharField(source="course.code", read_only=True)
    courseNameAr = serializers.CharField(source="course.name_ar", read_only=True)
    courseNameEn = serializers.CharField(source="course.name_en", read_only=True)

    class Meta:
        model = StudentGrade
        fields = [
            "id",
            "course",
            "courseCode",
            "courseNameAr",
            "courseNameEn",
            "grade",
            "points",
        ]


class StudentSerializer(serializers.ModelSerializer):
    studentId = serializers.CharField(source="student_id")
    nameAr = serializers.CharField(source="name_ar")
    nameEn = serializers.CharField(source="name_en")
    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), required=False, allow_null=True
    )
    facultySlug = serializers.CharField(source="faculty.slug", read_only=True)
    facultyNameAr = serializers.CharField(source="faculty.name_ar", read_only=True)
    facultyNameEn = serializers.CharField(source="faculty.name_en", read_only=True)
    programSlug = serializers.CharField(source="program.slug", read_only=True)
    programNameAr = serializers.CharField(source="program.name_ar", read_only=True)
    programNameEn = serializers.CharField(source="program.name_en", read_only=True)
    programDetail = serializers.SerializerMethodField(read_only=True)
    totalCredits = serializers.IntegerField(source="total_credits")
    completedCredits = serializers.IntegerField(source="completed_credits")
    isTop = serializers.BooleanField(source="is_top")
    schedule = ScheduleItemSerializer(
        source="schedule_items", many=True, read_only=True
    )
    grades = StudentGradeSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "studentId",
            "nameAr",
            "nameEn",
            "email",
            "faculty",
            "facultySlug",
            "facultyNameAr",
            "facultyNameEn",
            "program",
            "programSlug",
            "programNameAr",
            "programNameEn",
            "programDetail",
            "year",
            "gpa",
            "totalCredits",
            "completedCredits",
            "image",
            "isTop",
            "rank",
            "schedule",
            "grades",
        ]

    @extend_schema_field(serializers.DictField())
    def get_programDetail(self, obj):
        if obj.program:
            return {
                "id": obj.program.id,
                "nameAr": obj.program.name_ar,
                "nameEn": obj.program.name_en,
                "slug": obj.program.slug,
            }
        return None

    def validate(self, attrs):
        program = attrs.get("program") or (
            self.instance.program if self.instance else None
        )
        faculty = attrs.get("faculty") or (
            self.instance.faculty if self.instance else None
        )
        if program and program.faculty:
            attrs["faculty"] = program.faculty
        elif faculty and program and program.faculty_id != faculty.id:
            raise serializers.ValidationError(
                {"program": "التخصص/القسم المختار لا ينتمي إلى الكلية المحددة للطالب."}
            )
        return attrs

    def create(self, validated_data):
        if not validated_data.get("faculty") and validated_data.get("program"):
            validated_data["faculty"] = validated_data["program"].faculty
        return super().create(validated_data)


class NewsArticleSerializer(serializers.ModelSerializer):
    titleAr = serializers.CharField(source="title_ar")
    titleEn = serializers.CharField(source="title_en")
    excerptAr = serializers.CharField(source="excerpt_ar")
    excerptEn = serializers.CharField(source="excerpt_en")
    contentAr = serializers.CharField(source="content_ar")
    contentEn = serializers.CharField(source="content_en")
    scope = serializers.CharField(required=False, default="university")
    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), required=False, allow_null=True
    )
    facultyNameAr = serializers.CharField(source="faculty.name_ar", read_only=True)
    facultySlug = serializers.CharField(source="faculty.slug", read_only=True)
    program = serializers.PrimaryKeyRelatedField(
        queryset=Program.objects.all(), required=False, allow_null=True
    )
    programNameAr = serializers.CharField(source="program.name_ar", read_only=True)
    programSlug = serializers.CharField(source="program.slug", read_only=True)

    imageCaptionAr = serializers.CharField(
        source="image_caption_ar", required=False, allow_blank=True, default=""
    )
    imageCaptionEn = serializers.CharField(
        source="image_caption_en", required=False, allow_blank=True, default=""
    )
    authorNameAr = serializers.CharField(
        source="author_name_ar", required=False, allow_blank=True, default=""
    )
    authorNameEn = serializers.CharField(
        source="author_name_en", required=False, allow_blank=True, default=""
    )
    authorTitleAr = serializers.CharField(
        source="author_title_ar", required=False, allow_blank=True, default=""
    )
    authorTitleEn = serializers.CharField(
        source="author_title_en", required=False, allow_blank=True, default=""
    )
    readingTime = serializers.IntegerField(
        source="reading_time", required=False, default=3
    )
    viewsCount = serializers.IntegerField(source="views_count", read_only=True)
    status = serializers.CharField(required=False, default="published")
    galleryImages = serializers.JSONField(
        source="gallery_images", required=False, default=list
    )
    attachments = serializers.JSONField(
        required=False, default=list
    )
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "slug",
            "titleAr",
            "titleEn",
            "excerptAr",
            "excerptEn",
            "contentAr",
            "contentEn",
            "image",
            "imageCaptionAr",
            "imageCaptionEn",
            "category",
            "scope",
            "faculty",
            "facultyNameAr",
            "facultySlug",
            "program",
            "programNameAr",
            "programSlug",
            "authorNameAr",
            "authorNameEn",
            "authorTitleAr",
            "authorTitleEn",
            "readingTime",
            "viewsCount",
            "status",
            "galleryImages",
            "attachments",
            "date",
            "featured",
            "createdAt",
            "updatedAt",
        ]

    def to_internal_value(self, data):
        ret_data = data.copy() if hasattr(data, "copy") else dict(data)
        slug_val = ret_data.get("slug")
        title_en = ret_data.get("titleEn") or ret_data.get("title_en") or ""
        title_ar = ret_data.get("titleAr") or ret_data.get("title_ar") or ""
        ret_data["slug"] = sanitize_slug(
            slug_val, name_en=title_en, name_ar=title_ar, default_prefix="news"
        )
        return super().to_internal_value(ret_data)


class EventSerializer(serializers.ModelSerializer):
    titleAr = serializers.CharField(source="title_ar")
    titleEn = serializers.CharField(source="title_en")
    descriptionAr = serializers.CharField(source="description_ar")
    descriptionEn = serializers.CharField(source="description_en")
    location = serializers.SerializerMethodField(read_only=True)
    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), required=False, allow_null=True
    )
    facultyNameAr = serializers.CharField(source="faculty.name_ar", read_only=True)
    facultySlug = serializers.CharField(source="faculty.slug", read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "titleAr",
            "titleEn",
            "descriptionAr",
            "descriptionEn",
            "date",
            "time",
            "location",
            "type",
            "faculty",
            "facultyNameAr",
            "facultySlug",
        ]

    @extend_schema_field(serializers.DictField(child=serializers.CharField()))
    def get_location(self, obj):
        return {"ar": obj.location_ar, "en": obj.location_en}

    def to_internal_value(self, data):
        # Support writing location as nested {"ar": "...", "en": "..."}
        location = data.get("location")
        return super().to_internal_value(data)


class AcademicCalendarEventSerializer(serializers.ModelSerializer):
    eventAr = serializers.CharField(source="event_ar")
    eventEn = serializers.CharField(source="event_en")
    dateAr = serializers.CharField(source="date_ar")
    dateEn = serializers.CharField(source="date_en")
    order = serializers.IntegerField(required=False, default=0)

    class Meta:
        model = AcademicCalendarEvent
        fields = ["id", "eventAr", "eventEn", "dateAr", "dateEn", "order", "created_at"]


class JobApplicationSerializer(serializers.ModelSerializer):
    applicantName = serializers.CharField(source="applicant_name")
    coverLetter = serializers.CharField(
        source="cover_letter", required=False, allow_blank=True, default=""
    )
    resumeUrl = serializers.CharField(
        source="resume_url", required=False, allow_blank=True, default=""
    )
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            "id",
            "job",
            "applicantName",
            "email",
            "phone",
            "coverLetter",
            "resumeUrl",
            "status",
            "createdAt",
        ]


class JobOfferSerializer(serializers.ModelSerializer):
    titleAr = serializers.CharField(source="title_ar")
    titleEn = serializers.CharField(source="title_en")
    departmentAr = serializers.CharField(source="department_ar")
    departmentEn = serializers.CharField(source="department_en")
    locationAr = serializers.CharField(
        source="location_ar", required=False, default="حرم معرة صيدنايا"
    )
    locationEn = serializers.CharField(
        source="location_en", required=False, default="Maarat Saidnaya Campus"
    )
    requirementsAr = serializers.CharField(source="requirements_ar")
    requirementsEn = serializers.CharField(source="requirements_en")
    isActive = serializers.BooleanField(
        source="is_active", required=False, default=True
    )
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    applications = JobApplicationSerializer(many=True, read_only=True)

    class Meta:
        model = JobOffer
        fields = [
            "id",
            "titleAr",
            "titleEn",
            "departmentAr",
            "departmentEn",
            "type",
            "locationAr",
            "locationEn",
            "deadline",
            "requirementsAr",
            "requirementsEn",
            "isActive",
            "createdAt",
            "applications",
        ]


class AdmissionApplicationSerializer(serializers.ModelSerializer):
    fullNameAr = serializers.CharField(source="full_name_ar")
    fullNameEn = serializers.CharField(source="full_name_en")
    highSchoolBranch = serializers.CharField(source="high_school_branch")
    highSchoolScore = serializers.DecimalField(
        source="high_school_score", max_digits=5, decimal_places=2
    )
    desiredFaculty = serializers.PrimaryKeyRelatedField(
        source="desired_faculty",
        queryset=Faculty.objects.all(),
        required=False,
        allow_null=True,
    )
    desiredProgram = serializers.PrimaryKeyRelatedField(
        source="desired_program",
        queryset=Program.objects.all(),
        required=False,
        allow_null=True,
    )
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = AdmissionApplication
        fields = [
            "id",
            "fullNameAr",
            "fullNameEn",
            "email",
            "phone",
            "highSchoolBranch",
            "highSchoolScore",
            "desiredFaculty",
            "desiredProgram",
            "status",
            "createdAt",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    titleAr = serializers.CharField(source="title_ar")
    titleEn = serializers.CharField(source="title_en")
    messageAr = serializers.CharField(source="message_ar")
    messageEn = serializers.CharField(source="message_en")
    isRead = serializers.BooleanField(source="is_read", required=False, default=False)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "user",
            "titleAr",
            "titleEn",
            "messageAr",
            "messageEn",
            "type",
            "link",
            "isRead",
            "createdAt",
        ]


class ActivityLogSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source="user_name")
    userNameEn = serializers.CharField(
        source="user_name_en", required=False, allow_blank=True, default=""
    )
    actionAr = serializers.CharField(source="action_ar")
    actionEn = serializers.CharField(source="action_en")
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "userName",
            "userNameEn",
            "actionAr",
            "actionEn",
            "status",
            "createdAt",
        ]


class UserNotificationPreferenceSerializer(serializers.ModelSerializer):
    muteMessages = serializers.BooleanField(
        source="mute_messages", required=False, default=False
    )
    muteResults = serializers.BooleanField(
        source="mute_results", required=False, default=False
    )
    muteInfo = serializers.BooleanField(
        source="mute_info", required=False, default=False
    )
    muteWarning = serializers.BooleanField(
        source="mute_warning", required=False, default=False
    )
    muteUrgent = serializers.BooleanField(
        source="mute_urgent", required=False, default=False
    )

    class Meta:
        model = UserNotificationPreference
        fields = [
            "id",
            "user",
            "muteMessages",
            "muteResults",
            "muteInfo",
            "muteWarning",
            "muteUrgent",
        ]


class SiteSettingSerializer(serializers.ModelSerializer):
    addressEn = serializers.CharField(
        source="address_en", required=False, allow_blank=True, default=""
    )
    officeAddress = serializers.CharField(
        source="office_address", required=False, allow_blank=True, default=""
    )
    officeAddressEn = serializers.CharField(
        source="office_address_en", required=False, allow_blank=True, default=""
    )
    workingHours = serializers.CharField(
        source="working_hours", required=False, allow_blank=True, default=""
    )
    workingHoursEn = serializers.CharField(
        source="working_hours_en", required=False, allow_blank=True, default=""
    )
    contactFields = serializers.JSONField(
        source="contact_fields", required=False, default=dict
    )
    registrationOpen = serializers.BooleanField(
        source="registration_open", required=False, default=True
    )
    maintenanceMode = serializers.BooleanField(
        source="maintenance_mode", required=False, default=False
    )
    showResults = serializers.BooleanField(
        source="show_results", required=False, default=True
    )
    socialLinks = serializers.JSONField(
        source="social_links", required=False, default=dict
    )
    publishedPages = serializers.JSONField(
        source="published_pages", required=False, default=dict
    )
    homePageConfig = serializers.JSONField(
        source="home_page_config", required=False, default=dict
    )
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = SiteSetting
        fields = [
            "id",
            "email",
            "phone",
            "address",
            "addressEn",
            "officeAddress",
            "officeAddressEn",
            "workingHours",
            "workingHoursEn",
            "contactFields",
            "registrationOpen",
            "maintenanceMode",
            "showResults",
            "socialLinks",
            "publishedPages",
            "homePageConfig",
            "updatedAt",
        ]


class BookSerializer(serializers.ModelSerializer):
    titleAr = serializers.CharField(source="title_ar")
    titleEn = serializers.CharField(source="title_en")
    authorAr = serializers.CharField(source="author_ar")
    authorEn = serializers.CharField(source="author_en")
    isbn = serializers.CharField(required=False, allow_blank=True, default="")

    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), required=False, allow_null=True
    )
    facultyNameAr = serializers.CharField(source="faculty.name_ar", read_only=True)
    facultyNameEn = serializers.CharField(source="faculty.name_en", read_only=True)

    category = serializers.CharField(required=False, default="engineering")
    categoryNameAr = serializers.CharField(
        source="category_name_ar", required=False, allow_blank=True, default=""
    )
    categoryNameEn = serializers.CharField(
        source="category_name_en", required=False, allow_blank=True, default=""
    )

    year = serializers.IntegerField(
        source="publication_year", required=False, default=2024
    )
    edition = serializers.CharField(required=False, allow_blank=True, default="")
    pages = serializers.IntegerField(source="pages_count", required=False, default=0)
    language = serializers.CharField(required=False, default="العربية")

    descriptionAr = serializers.CharField(
        source="description_ar", required=False, allow_blank=True, default=""
    )
    descriptionEn = serializers.CharField(
        source="description_en", required=False, allow_blank=True, default=""
    )

    coverImage = serializers.CharField(
        source="cover_image", required=False, allow_blank=True, default=""
    )
    coverColor = serializers.CharField(
        source="cover_color", required=False, default="from-blue-600 to-indigo-950"
    )

    pdfFile = serializers.CharField(
        source="pdf_file", required=False, allow_blank=True, default=""
    )
    pdfFileSize = serializers.IntegerField(
        source="pdf_file_size", required=False, default=0
    )
    pdfFileSizeFormatted = serializers.CharField(
        source="pdf_file_size_formatted", required=False, allow_blank=True, default=""
    )
    allowDownload = serializers.BooleanField(
        source="allow_download", required=False, default=True
    )

    totalCopies = serializers.IntegerField(
        source="total_copies", required=False, default=1
    )
    availableCopies = serializers.IntegerField(
        source="available_copies", required=False, default=1
    )
    shelfLocation = serializers.CharField(
        source="shelf_location", required=False, allow_blank=True, default=""
    )
    available = serializers.BooleanField(
        source="is_available", required=False, default=True
    )

    viewsCount = serializers.IntegerField(source="views_count", read_only=True)
    downloadsCount = serializers.IntegerField(
        source="downloads_count", read_only=True
    )
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "titleAr",
            "titleEn",
            "authorAr",
            "authorEn",
            "isbn",
            "faculty",
            "facultyNameAr",
            "facultyNameEn",
            "category",
            "categoryNameAr",
            "categoryNameEn",
            "year",
            "edition",
            "pages",
            "language",
            "descriptionAr",
            "descriptionEn",
            "coverImage",
            "coverColor",
            "pdfFile",
            "pdfFileSize",
            "pdfFileSizeFormatted",
            "allowDownload",
            "totalCopies",
            "availableCopies",
            "shelfLocation",
            "available",
            "viewsCount",
            "downloadsCount",
            "createdAt",
            "updatedAt",
        ]


class BookReservationSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    bookTitleAr = serializers.CharField(source="book.title_ar", read_only=True)
    bookTitleEn = serializers.CharField(source="book.title_en", read_only=True)
    bookCoverImage = serializers.CharField(source="book.cover_image", read_only=True)

    studentName = serializers.CharField(source="student_name")
    studentId = serializers.CharField(source="student_id")
    studentMajor = serializers.CharField(
        source="student_major", required=False, allow_blank=True, default=""
    )
    studentEmail = serializers.EmailField(
        source="student_email", required=False, allow_blank=True, default=""
    )
    studentPhone = serializers.CharField(
        source="student_phone", required=False, allow_blank=True, default=""
    )

    status = serializers.CharField(required=False, default="pending")
    reservedAt = serializers.DateTimeField(source="reserved_at", read_only=True)
    expiresAt = serializers.DateTimeField(
        source="expires_at", required=False, allow_null=True
    )
    returnedAt = serializers.DateTimeField(
        source="returned_at", required=False, allow_null=True
    )

    notes = serializers.CharField(required=False, allow_blank=True, default="")
    adminNotes = serializers.CharField(
        source="admin_notes", required=False, allow_blank=True, default=""
    )

    class Meta:
        model = BookReservation
        fields = [
            "id",
            "book",
            "bookTitleAr",
            "bookTitleEn",
            "bookCoverImage",
            "studentName",
            "studentId",
            "studentMajor",
            "studentEmail",
            "studentPhone",
            "status",
            "reservedAt",
            "expiresAt",
            "returnedAt",
            "notes",
            "adminNotes",
        ]


class ResearchCenterSerializer(serializers.ModelSerializer):
    titleAr = serializers.CharField(source="title_ar")
    titleEn = serializers.CharField(source="title_en")
    descriptionAr = serializers.CharField(source="description_ar")
    descriptionEn = serializers.CharField(source="description_en")
    icon = serializers.CharField(required=False, default="Microscope")
    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), required=False, allow_null=True
    )
    facultyNameAr = serializers.CharField(source="faculty.name_ar", read_only=True)
    facultyNameEn = serializers.CharField(source="faculty.name_en", read_only=True)
    directorNameAr = serializers.CharField(
        source="director_name_ar", required=False, allow_blank=True, default=""
    )
    directorNameEn = serializers.CharField(
        source="director_name_en", required=False, allow_blank=True, default=""
    )
    location = serializers.CharField(
        required=False, allow_blank=True, default=""
    )
    contactEmail = serializers.EmailField(
        source="contact_email", required=False, allow_blank=True, default=""
    )
    isActive = serializers.BooleanField(source="is_active", required=False, default=True)
    order = serializers.IntegerField(required=False, default=0)
    publicationsCount = serializers.SerializerMethodField(read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    @extend_schema_field(serializers.IntegerField)
    def get_publicationsCount(self, obj):
        return obj.publications.filter(is_active=True).count()

    class Meta:
        model = ResearchCenter
        fields = [
            "id",
            "titleAr",
            "titleEn",
            "descriptionAr",
            "descriptionEn",
            "icon",
            "faculty",
            "facultyNameAr",
            "facultyNameEn",
            "directorNameAr",
            "directorNameEn",
            "location",
            "contactEmail",
            "isActive",
            "order",
            "publicationsCount",
            "createdAt",
        ]


class ResearchAreaSerializer(serializers.ModelSerializer):
    nameAr = serializers.CharField(source="name_ar")
    nameEn = serializers.CharField(source="name_en")
    descriptionAr = serializers.CharField(
        source="description_ar", required=False, allow_blank=True, default=""
    )
    descriptionEn = serializers.CharField(
        source="description_en", required=False, allow_blank=True, default=""
    )
    isActive = serializers.BooleanField(source="is_active", required=False, default=True)
    order = serializers.IntegerField(required=False, default=0)
    publicationsCount = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(serializers.IntegerField)
    def get_publicationsCount(self, obj):
        return obj.publications.filter(is_active=True).count()

    class Meta:
        model = ResearchArea
        fields = [
            "id",
            "nameAr",
            "nameEn",
            "descriptionAr",
            "descriptionEn",
            "isActive",
            "order",
            "publicationsCount",
        ]


class ResearchPublicationSerializer(serializers.ModelSerializer):
    titleAr = serializers.CharField(source="title_ar")
    titleEn = serializers.CharField(source="title_en")
    authorsAr = serializers.CharField(source="authors_ar")
    authorsEn = serializers.CharField(source="authors_en")
    journalAr = serializers.CharField(source="journal_ar")
    journalEn = serializers.CharField(source="journal_en")
    publicationYear = serializers.IntegerField(
        source="publication_year", required=False, default=2024
    )

    researchArea = serializers.PrimaryKeyRelatedField(
        queryset=ResearchArea.objects.all(),
        source="research_area",
        required=False,
        allow_null=True,
    )
    researchAreaNameAr = serializers.CharField(
        source="research_area.name_ar", read_only=True
    )
    researchAreaNameEn = serializers.CharField(
        source="research_area.name_en", read_only=True
    )

    center = serializers.PrimaryKeyRelatedField(
        queryset=ResearchCenter.objects.all(),
        required=False,
        allow_null=True,
    )
    centerTitleAr = serializers.CharField(source="center.title_ar", read_only=True)
    centerTitleEn = serializers.CharField(source="center.title_en", read_only=True)

    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(),
        required=False,
        allow_null=True,
    )
    facultyNameAr = serializers.CharField(source="faculty.name_ar", read_only=True)
    facultyNameEn = serializers.CharField(source="faculty.name_en", read_only=True)

    abstractAr = serializers.CharField(
        source="abstract_ar", required=False, allow_blank=True, default=""
    )
    abstractEn = serializers.CharField(
        source="abstract_en", required=False, allow_blank=True, default=""
    )

    doiUrl = serializers.URLField(
        source="doi_url", required=False, allow_blank=True, default=""
    )
    pdfFile = serializers.CharField(
        source="pdf_file", required=False, allow_blank=True, default=""
    )
    pdfFileSize = serializers.IntegerField(
        source="pdf_file_size", required=False, default=0
    )
    pdfFileSizeFormatted = serializers.CharField(
        source="pdf_file_size_formatted", required=False, allow_blank=True, default=""
    )

    viewsCount = serializers.IntegerField(source="views_count", read_only=True)
    downloadsCount = serializers.IntegerField(source="downloads_count", read_only=True)

    isFeatured = serializers.BooleanField(
        source="is_featured", required=False, default=False
    )
    isActive = serializers.BooleanField(source="is_active", required=False, default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = ResearchPublication
        fields = [
            "id",
            "titleAr",
            "titleEn",
            "authorsAr",
            "authorsEn",
            "journalAr",
            "journalEn",
            "publicationYear",
            "researchArea",
            "researchAreaNameAr",
            "researchAreaNameEn",
            "center",
            "centerTitleAr",
            "centerTitleEn",
            "faculty",
            "facultyNameAr",
            "facultyNameEn",
            "abstractAr",
            "abstractEn",
            "doiUrl",
            "pdfFile",
            "pdfFileSize",
            "pdfFileSizeFormatted",
            "viewsCount",
            "downloadsCount",
            "isFeatured",
            "isActive",
            "createdAt",
            "updatedAt",
        ]


class HousingFeatureSerializer(serializers.ModelSerializer):
    titleAr = serializers.CharField(source="title_ar")
    titleEn = serializers.CharField(source="title_en", required=False, allow_blank=True, default="")
    descriptionAr = serializers.CharField(source="description_ar")
    descriptionEn = serializers.CharField(source="description_en", required=False, allow_blank=True, default="")
    icon = serializers.CharField(required=False, default="Bed")
    order = serializers.IntegerField(required=False, default=0)
    isActive = serializers.BooleanField(source="is_active", required=False, default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = HousingFeature
        fields = [
            "id",
            "titleAr",
            "titleEn",
            "descriptionAr",
            "descriptionEn",
            "icon",
            "order",
            "isActive",
            "createdAt",
            "updatedAt",
        ]


class StudentClubSerializer(serializers.ModelSerializer):
    nameAr = serializers.CharField(source="name_ar")
    nameEn = serializers.CharField(source="name_en", required=False, allow_blank=True, default="")
    descriptionAr = serializers.CharField(source="description_ar")
    descriptionEn = serializers.CharField(source="description_en", required=False, allow_blank=True, default="")
    icon = serializers.CharField(required=False, default="Users")
    category = serializers.CharField(required=False, allow_blank=True, default="عام")
    supervisor = serializers.CharField(required=False, allow_blank=True, default="")
    order = serializers.IntegerField(required=False, default=0)
    isActive = serializers.BooleanField(source="is_active", required=False, default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = StudentClub
        fields = [
            "id",
            "nameAr",
            "nameEn",
            "descriptionAr",
            "descriptionEn",
            "icon",
            "category",
            "supervisor",
            "order",
            "isActive",
            "createdAt",
            "updatedAt",
        ]


class SportActivitySerializer(serializers.ModelSerializer):
    nameAr = serializers.CharField(source="name_ar")
    nameEn = serializers.CharField(source="name_en", required=False, allow_blank=True, default="")
    descriptionAr = serializers.CharField(source="description_ar", required=False, allow_blank=True, default="")
    descriptionEn = serializers.CharField(source="description_en", required=False, allow_blank=True, default="")
    icon = serializers.CharField(required=False, default="Dumbbell")
    order = serializers.IntegerField(required=False, default=0)
    isActive = serializers.BooleanField(source="is_active", required=False, default=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = SportActivity
        fields = [
            "id",
            "nameAr",
            "nameEn",
            "descriptionAr",
            "descriptionEn",
            "icon",
            "order",
            "isActive",
            "createdAt",
            "updatedAt",
        ]


class CampusLifeOverviewSerializer(serializers.ModelSerializer):
    housingTitleAr = serializers.CharField(source="housing_title_ar", required=False, default="السكن الجامعي")
    housingTitleEn = serializers.CharField(source="housing_title_en", required=False, allow_blank=True, default="Student Housing")
    housingDescAr = serializers.CharField(source="housing_desc_ar", required=False, default="")
    housingDescEn = serializers.CharField(source="housing_desc_en", required=False, allow_blank=True, default="")
    housingImage = serializers.CharField(source="housing_image", required=False, allow_blank=True, default="")
    housingContactNoteAr = serializers.CharField(source="housing_contact_note_ar", required=False, allow_blank=True, default="")
    housingContactNoteEn = serializers.CharField(source="housing_contact_note_en", required=False, allow_blank=True, default="")

    sportsTitleAr = serializers.CharField(source="sports_title_ar", required=False, default="الأنشطة الرياضية")
    sportsTitleEn = serializers.CharField(source="sports_title_en", required=False, allow_blank=True, default="Sports Activities")
    sportsDescAr = serializers.CharField(source="sports_desc_ar", required=False, default="")
    sportsDescEn = serializers.CharField(source="sports_desc_en", required=False, allow_blank=True, default="")
    sportsImage = serializers.CharField(source="sports_image", required=False, allow_blank=True, default="")
    championshipsTitleAr = serializers.CharField(source="championships_title_ar", required=False, allow_blank=True, default="البطولات السنوية")
    championshipsTitleEn = serializers.CharField(source="championships_title_en", required=False, allow_blank=True, default="Annual Championships")
    championshipsDescAr = serializers.CharField(source="championships_desc_ar", required=False, allow_blank=True, default="")
    championshipsDescEn = serializers.CharField(source="championships_desc_en", required=False, allow_blank=True, default="")
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = CampusLifeOverview
        fields = [
            "id",
            "housingTitleAr",
            "housingTitleEn",
            "housingDescAr",
            "housingDescEn",
            "housingImage",
            "housingContactNoteAr",
            "housingContactNoteEn",
            "sportsTitleAr",
            "sportsTitleEn",
            "sportsDescAr",
            "sportsDescEn",
            "sportsImage",
            "championshipsTitleAr",
            "championshipsTitleEn",
            "championshipsDescAr",
            "championshipsDescEn",
            "updatedAt",
        ]


