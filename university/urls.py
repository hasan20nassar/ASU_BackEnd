from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FacultyViewSet,
    ProgramViewSet,
    FacultyMemberViewSet,
    FacultyAppointmentViewSet,
    UserProfileViewSet,
    AlumniStoryViewSet,
    CourseViewSet,
    StudentViewSet,
    ScheduleItemViewSet,
    StudentGradeViewSet,
    NewsArticleViewSet,
    EventViewSet,
    AcademicCalendarEventViewSet,
    JobOfferViewSet,
    JobApplicationViewSet,
    AdmissionApplicationViewSet,
    NotificationViewSet,
    ActivityLogViewSet,
    SiteSettingViewSet,
    MediaUploadView,
    BookViewSet,
    BookReservationViewSet,
    BookPdfUploadView,
    BookCoverUploadView,
    ResearchCenterViewSet,
    ResearchAreaViewSet,
    ResearchPublicationViewSet,
    ResearchPdfUploadView,
    HousingFeatureViewSet,
    StudentClubViewSet,
    SportActivityViewSet,
    CampusLifeOverviewViewSet,
    FacultyLaboratoryViewSet,
)

router = DefaultRouter()
router.register(r"users", UserProfileViewSet, basename="user-profile")
router.register(r"site-settings", SiteSettingViewSet, basename="site-setting")
router.register(r"faculties", FacultyViewSet, basename="faculty")
router.register(r"faculty-laboratories", FacultyLaboratoryViewSet, basename="faculty-laboratory")
router.register(r"laboratories", FacultyLaboratoryViewSet, basename="laboratory")

router.register(r"programs", ProgramViewSet, basename="program")
router.register(r"faculty-members", FacultyMemberViewSet, basename="faculty-member")
router.register(r"faculty-appointments", FacultyAppointmentViewSet, basename="faculty-appointment")
router.register(r"alumni-stories", AlumniStoryViewSet, basename="alumni-story")

router.register(r"courses", CourseViewSet, basename="course")
router.register(r"students", StudentViewSet, basename="student")
router.register(r"schedule-items", ScheduleItemViewSet, basename="schedule-item")
router.register(r"student-grades", StudentGradeViewSet, basename="student-grade")
router.register(r"news-articles", NewsArticleViewSet, basename="news-article")
router.register(r"events", EventViewSet, basename="event")
router.register(r"academic-calendar", AcademicCalendarEventViewSet, basename="academic-calendar")
router.register(r"jobs", JobOfferViewSet, basename="job-offer")
router.register(r"job-applications", JobApplicationViewSet, basename="job-application")
router.register(r"admission-applications", AdmissionApplicationViewSet, basename="admission-application")
router.register(r"notifications", NotificationViewSet, basename="notification")
router.register(r"activity-logs", ActivityLogViewSet, basename="activity-log")
router.register(r"books", BookViewSet, basename="book")
router.register(r"book-reservations", BookReservationViewSet, basename="book-reservation")
router.register(r"research-centers", ResearchCenterViewSet, basename="research-center")
router.register(r"research-areas", ResearchAreaViewSet, basename="research-area")
router.register(r"research-publications", ResearchPublicationViewSet, basename="research-publication")
router.register(r"campus-life/housing-features", HousingFeatureViewSet, basename="housing-feature")
router.register(r"campus-life/student-clubs", StudentClubViewSet, basename="student-club")
router.register(r"campus-life/sport-activities", SportActivityViewSet, basename="sport-activity")
router.register(r"campus-life/overview", CampusLifeOverviewViewSet, basename="campus-life-overview")


urlpatterns = [
    path("upload/", MediaUploadView.as_view(), name="media-upload"),
    path("books/upload-pdf/", BookPdfUploadView.as_view(), name="book-pdf-upload"),
    path("books/upload-cover/", BookCoverUploadView.as_view(), name="book-cover-upload"),
    path("research/upload-pdf/", ResearchPdfUploadView.as_view(), name="research-pdf-upload"),
    path("", include(router.urls)),
]


