from django.core.management.base import BaseCommand
from django.db import transaction
from university.models import (
    Faculty,
    Program,
    FacultyMember,
    AlumniStory,
    Course,
    Student,
    ScheduleItem,
    StudentGrade,
    NewsArticle,
    Event,
)

class Command(BaseCommand):
    help = "Clears all seeded university data from the database while keeping superusers intact."

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Also delete regular users linked to student profiles.',
        )

    def handle(self, *args, **options):
        self.stdout.write("Clearing university database tables...")

        with transaction.atomic():
            # Delete in reverse foreign key order to prevent CASCADE issues
            schedule_count, _ = ScheduleItem.objects.all().delete()
            grade_count, _ = StudentGrade.objects.all().delete()
            student_count, _ = Student.objects.all().delete()
            course_count, _ = Course.objects.all().delete()
            alumni_count, _ = AlumniStory.objects.all().delete()
            member_count, _ = FacultyMember.objects.all().delete()
            program_count, _ = Program.objects.all().delete()
            faculty_count, _ = Faculty.objects.all().delete()
            news_count, _ = NewsArticle.objects.all().delete()
            event_count, _ = Event.objects.all().delete()

            self.stdout.write(self.style.SUCCESS(
                f"Cleared data:\n"
                f"  - ScheduleItems: {schedule_count}\n"
                f"  - StudentGrades: {grade_count}\n"
                f"  - Students: {student_count}\n"
                f"  - Courses: {course_count}\n"
                f"  - AlumniStories: {alumni_count}\n"
                f"  - FacultyMembers: {member_count}\n"
                f"  - Programs: {program_count}\n"
                f"  - Faculties: {faculty_count}\n"
                f"  - NewsArticles: {news_count}\n"
                f"  - Events: {event_count}"
            ))

        self.stdout.write(self.style.SUCCESS("Database cleared successfully! Tables are now empty."))
