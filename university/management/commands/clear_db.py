from django.core.management.base import BaseCommand
from django.db import transaction
from university.models import (
    Faculty,
    FacultyLaboratory,
    FacultyMember,
    FacultyAppointment,
    Program,
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


class Command(BaseCommand):
    help = "Clears all university data from tables while keeping ALL UserProfile accounts (admins, faculty, students) completely intact."

    def handle(self, *args, **options):
        self.stdout.write("Clearing university data while preserving all user accounts...")

        with transaction.atomic():
            # Delete in reverse FK order to avoid constraints
            FacultyLaboratory.objects.all().delete()
            FacultyAppointment.objects.all().delete()
            ScheduleItem.objects.all().delete()
            StudentGrade.objects.all().delete()
            Student.objects.all().delete()
            Course.objects.all().delete()
            AlumniStory.objects.all().delete()
            FacultyMember.objects.all().delete()
            Program.objects.all().delete()
            Faculty.objects.all().delete()
            NewsArticle.objects.all().delete()
            Event.objects.all().delete()
            AcademicCalendarEvent.objects.all().delete()
            JobApplication.objects.all().delete()
            JobOffer.objects.all().delete()
            AdmissionApplication.objects.all().delete()
            UserNotificationState.objects.all().delete()
            UserNotificationPreference.objects.all().delete()
            Notification.objects.all().delete()
            ActivityLog.objects.all().delete()
            BookReservation.objects.all().delete()
            Book.objects.all().delete()
            ResearchPublication.objects.all().delete()
            ResearchArea.objects.all().delete()
            ResearchCenter.objects.all().delete()
            HousingFeature.objects.all().delete()
            StudentClub.objects.all().delete()
            SportActivity.objects.all().delete()
            CampusLifeOverview.objects.all().delete()
            SiteSetting.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully cleared all data from university tables!\n"
                "ALL user accounts (UserProfile) and credentials remain safely intact."
            )
        )
