from django.contrib import admin
from .models import (
    Faculty,
    FacultyLaboratory,
    Program,
    FacultyMember,
    AlumniStory,
    Course,
    Student,
    ScheduleItem,
    StudentGrade,
    NewsArticle,
    Event,
    AcademicCalendarEvent,
    UserProfile,
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


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("email", "name_ar", "role", "is_staff", "is_superuser", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "name_ar", "name_en", "username")


class FacultyLaboratoryInline(admin.TabularInline):
    model = FacultyLaboratory
    extra = 1


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name_en", "slug", "icon", "color")
    search_fields = ("name_en", "name_ar", "slug")
    inlines = [FacultyLaboratoryInline]


@admin.register(FacultyLaboratory)
class FacultyLaboratoryAdmin(admin.ModelAdmin):
    list_display = ("name_ar", "name_en", "faculty", "location_ar", "capacity", "is_active", "order")
    list_filter = ("faculty", "is_active")
    search_fields = (
        "name_ar",
        "name_en",
        "description_ar",
        "description_en",
        "equipment_ar",
        "faculty__name_ar",
        "faculty__name_en",
    )


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name_en", "slug", "faculty", "credit_hours", "duration")
    list_filter = ("faculty", "branch")
    search_fields = ("name_en", "name_ar", "slug")


@admin.register(FacultyMember)
class FacultyMemberAdmin(admin.ModelAdmin):
    list_display = ("name_en", "faculty", "title_en", "email", "is_head")
    list_filter = ("faculty", "is_head")
    search_fields = ("name_en", "name_ar", "email")


@admin.register(AlumniStory)
class AlumniStoryAdmin(admin.ModelAdmin):
    list_display = ("name_en", "faculty", "graduation_year", "current_role_en")
    list_filter = ("faculty", "graduation_year")
    search_fields = ("name_en", "name_ar", "company_en")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name_en", "code", "credits")
    search_fields = ("name_en", "name_ar", "code")


class ScheduleItemInline(admin.TabularInline):
    model = ScheduleItem
    extra = 1


class StudentGradeInline(admin.TabularInline):
    model = StudentGrade
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "name_en", "email", "faculty", "program", "gpa", "is_top")
    list_filter = ("faculty", "program", "year", "is_top")
    search_fields = ("student_id", "name_en", "name_ar", "email")
    inlines = [ScheduleItemInline, StudentGradeInline]


@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "day_en", "time", "room")
    list_filter = ("day", "room")
    search_fields = ("student__name_en", "course__name_en")


@admin.register(StudentGrade)
class StudentGradeAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "grade", "points")
    list_filter = ("grade",)
    search_fields = ("student__name_en", "course__name_en")


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title_en", "category", "date", "featured")
    list_filter = ("category", "date", "featured")
    search_fields = ("title_en", "title_ar", "excerpt_en", "excerpt_ar")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title_en", "date", "time", "location_en", "type")
    list_filter = ("date", "type")
    search_fields = ("title_en", "title_ar", "location_en")


@admin.register(AcademicCalendarEvent)
class AcademicCalendarEventAdmin(admin.ModelAdmin):
    list_display = ("event_en", "event_ar", "date_en", "date_ar", "order")
    search_fields = ("event_en", "event_ar", "date_en", "date_ar")
    list_editable = ("order",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title_ar",
        "title_en",
        "author_ar",
        "category",
        "isbn",
        "publication_year",
        "available_copies",
        "total_copies",
        "is_available",
    )
    list_filter = ("category", "faculty", "is_available", "allow_download", "publication_year")
    search_fields = ("title_ar", "title_en", "author_ar", "author_en", "isbn")


@admin.register(BookReservation)
class BookReservationAdmin(admin.ModelAdmin):
    list_display = (
        "student_name",
        "student_id",
        "book",
        "status",
        "reserved_at",
        "expires_at",
    )
    list_filter = ("status", "reserved_at")
    search_fields = ("student_name", "student_id", "student_email", "book__title_ar")


@admin.register(ResearchCenter)
class ResearchCenterAdmin(admin.ModelAdmin):
    list_display = ("title_ar", "title_en", "faculty", "director_name_ar", "is_active", "order")
    list_filter = ("faculty", "is_active")
    search_fields = ("title_ar", "title_en", "director_name_ar")
    list_editable = ("order", "is_active")


@admin.register(ResearchArea)
class ResearchAreaAdmin(admin.ModelAdmin):
    list_display = ("name_ar", "name_en", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("name_ar", "name_en")
    list_editable = ("order", "is_active")


@admin.register(ResearchPublication)
class ResearchPublicationAdmin(admin.ModelAdmin):
    list_display = (
        "title_ar",
        "authors_ar",
        "journal_ar",
        "publication_year",
        "research_area",
        "center",
        "is_featured",
        "is_active",
        "views_count",
    )
    list_filter = ("publication_year", "research_area", "center", "faculty", "is_featured", "is_active")
    search_fields = ("title_ar", "title_en", "authors_ar", "authors_en", "journal_ar")
    list_editable = ("is_featured", "is_active")


@admin.register(HousingFeature)
class HousingFeatureAdmin(admin.ModelAdmin):
    list_display = ("title_ar", "title_en", "icon", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title_ar", "title_en", "description_ar")
    list_editable = ("order", "is_active")


@admin.register(StudentClub)
class StudentClubAdmin(admin.ModelAdmin):
    list_display = ("name_ar", "name_en", "category", "supervisor", "icon", "order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name_ar", "name_en", "description_ar", "supervisor")
    list_editable = ("order", "is_active")


@admin.register(SportActivity)
class SportActivityAdmin(admin.ModelAdmin):
    list_display = ("name_ar", "name_en", "icon", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name_ar", "name_en")
    list_editable = ("order", "is_active")


@admin.register(CampusLifeOverview)
class CampusLifeOverviewAdmin(admin.ModelAdmin):
    list_display = ("housing_title_ar", "sports_title_ar", "updated_at")



