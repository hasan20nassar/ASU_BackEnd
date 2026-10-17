from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


def default_faculty_layout():
    return {
        "header_style": "hero_split",
        "show_quick_stats": True,
        "show_dean_message": True,
        "show_programs": True,
        "show_news": True,
        "show_events": True,
        "show_facilities": True,
        "show_staff": True,
        "show_top_students": True,
        "show_alumni_stories": True,
        "sections_order": [
            "stats",
            "dean",
            "programs",
            "news",
            "events",
            "facilities",
            "staff",
            "top_students",
            "alumni_stories",
        ],
    }


class Faculty(models.Model):
    """
    Represents a university Faculty (e.g. Faculty of Engineering).
    Operates as a dedicated faculty microsite with custom branding, dean details, stats, & labs.
    """

    slug = models.SlugField(max_length=100, unique=True, verbose_name="Faculty Slug")
    name_ar = models.CharField(max_length=255, verbose_name="Name (AR)")
    name_en = models.CharField(max_length=255, verbose_name="Name (EN)")
    description_ar = models.TextField(
        blank=True, default="", verbose_name="Description (AR)"
    )
    description_en = models.TextField(
        blank=True, default="", verbose_name="Description (EN)"
    )
    icon = models.CharField(
        max_length=100, default="Building2", verbose_name="Icon Name"
    )
    color = models.CharField(
        max_length=100, default="bg-blue-500", verbose_name="Color Class"
    )
    image = models.TextField(
        blank=True, default="", verbose_name="Image Path or Base64"
    )

    # Custom Branding & Visual Identity
    motto_ar = models.CharField(
        max_length=255,
        blank=True,
        default="الصرح الأكاديمي والبحثي الرائد",
        verbose_name="Motto (AR)",
    )
    motto_en = models.CharField(
        max_length=255,
        blank=True,
        default="Pioneering Academic & Research Excellence",
        verbose_name="Motto (EN)",
    )
    primary_color = models.CharField(
        max_length=50, default="#800000", verbose_name="Primary Theme Color (HEX)"
    )
    accent_color = models.CharField(
        max_length=50, default="#D4AF37", verbose_name="Accent Theme Color (HEX)"
    )
    hero_banner = models.TextField(
        blank=True, default="", verbose_name="Hero Banner Image / URL"
    )
    logo_url = models.TextField(
        blank=True, default="", verbose_name="Faculty Emblem / Logo URL"
    )

    # Dean & Leadership
    dean = models.ForeignKey(
        "FacultyMember",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dean_faculties",
        verbose_name="Faculty Dean",
    )
    dean_name_ar = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Dean Name (AR)"
    )
    dean_name_en = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Dean Name (EN)"
    )
    dean_message_ar = models.TextField(
        blank=True, default="", verbose_name="Dean Welcome Message (AR)"
    )
    dean_message_en = models.TextField(
        blank=True, default="", verbose_name="Dean Welcome Message (EN)"
    )
    dean_photo = models.TextField(blank=True, default="", verbose_name="Dean Photo URL")

    # Key Statistics & Metrics
    established_year = models.PositiveIntegerField(
        default=2005, verbose_name="Established Year"
    )
    students_count = models.PositiveIntegerField(
        default=1200, verbose_name="Active Students Count"
    )
    labs_count = models.PositiveIntegerField(
        default=12, verbose_name="Labs & Research Facilities Count"
    )
    research_papers_count = models.PositiveIntegerField(
        default=250, verbose_name="Published Research Papers"
    )
    employment_rate = models.PositiveIntegerField(
        default=92, verbose_name="Graduate Employment Rate (%)"
    )

    # Research Facilities & Downloads
    facilities = models.JSONField(
        blank=True, default=list, verbose_name="Labs & Facilities List"
    )
    guide_document_url = models.CharField(
        max_length=500, blank=True, default="", verbose_name="Guide Prospectus PDF URL"
    )

    # Page Layout & Builder Configuration
    layout_config = models.JSONField(
        blank=True, default=default_faculty_layout, verbose_name="Page Layout Configuration"
    )

    def __str__(self):
        return self.name_en

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"


def default_program_layout():
    return {
        "header_style": "hero_split",
        "show_quick_stats": True,
        "show_head_message": True,
        "show_news": True,
        "show_curriculum": True,
        "show_career_paths": True,
        "show_facilities": True,
        "show_staff": True,
        "show_top_students": True,
        "show_alumni_stories": True,
        "sections_order": [
            "stats",
            "head",
            "news",
            "curriculum",
            "career_paths",
            "facilities",
            "staff",
            "top_students",
            "alumni_stories",
        ],
    }


class Program(models.Model):
    """
    Represents an Academic Program/Branch (e.g. Civil Engineering) under a Faculty.
    Matches the structure of 'Program' in the frontend.
    """

    BRANCH_CHOICES = [
        ("scientific", "Scientific"),
        ("literary", "Literary"),
        ("both", "Both"),
    ]

    slug = models.SlugField(max_length=100, unique=True, verbose_name="Program Slug")
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="programs",
        verbose_name="Faculty",
    )
    name_ar = models.CharField(max_length=255, verbose_name="Name (AR)")
    name_en = models.CharField(max_length=255, verbose_name="Name (EN)")
    description_ar = models.TextField(
        blank=True, default="", verbose_name="Description (AR)"
    )
    description_en = models.TextField(
        blank=True, default="", verbose_name="Description (EN)"
    )
    credit_hours = models.PositiveIntegerField(verbose_name="Credit Hours")
    min_score_percent = models.PositiveIntegerField(verbose_name="Min Score (%)")
    min_score_points = models.PositiveIntegerField(verbose_name="Min Score Points")
    tuition_syrian = models.PositiveIntegerField(verbose_name="Tuition Syrian (SYP)")
    tuition_non_resident = models.PositiveIntegerField(
        verbose_name="Tuition Non-Resident (USD)"
    )
    branch = models.CharField(
        max_length=50,
        choices=BRANCH_CHOICES,
        default="both",
        verbose_name="Branch Requirement",
    )
    duration = models.PositiveIntegerField(
        help_text="Duration in years", verbose_name="Duration (Years)"
    )
    head = models.ForeignKey(
        "FacultyMember",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="head_programs",
        verbose_name="Department Head",
    )

    motto_ar = models.CharField(
        max_length=255,
        blank=True,
        default="نحو التميز الأكاديمي والمهني",
        verbose_name="Motto (AR)",
    )
    motto_en = models.CharField(
        max_length=255,
        blank=True,
        default="Towards Academic & Professional Excellence",
        verbose_name="Motto (EN)",
    )
    primary_color = models.CharField(
        max_length=50, default="#1E3A8A", blank=True, verbose_name="Primary Color"
    )
    accent_color = models.CharField(
        max_length=50, default="#F59E0B", blank=True, verbose_name="Accent Color"
    )
    hero_banner = models.TextField(
        blank=True, default="", verbose_name="Hero Banner Image / Base64"
    )
    logo_url = models.TextField(
        blank=True, default="", verbose_name="Department Logo / Base64"
    )
    head_name_ar = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Head Name (AR)"
    )
    head_name_en = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Head Name (EN)"
    )
    head_message_ar = models.TextField(
        blank=True, default="", verbose_name="Head Message (AR)"
    )
    head_message_en = models.TextField(
        blank=True, default="", verbose_name="Head Message (EN)"
    )
    head_photo = models.TextField(
        blank=True, default="", verbose_name="Head Photo / Base64"
    )
    established_year = models.PositiveIntegerField(
        default=2005, blank=True, null=True, verbose_name="Established Year"
    )
    students_count = models.PositiveIntegerField(
        default=350, blank=True, null=True, verbose_name="Students Count"
    )
    labs_count = models.PositiveIntegerField(
        default=6, blank=True, null=True, verbose_name="Labs Count"
    )
    research_papers_count = models.PositiveIntegerField(
        default=80, blank=True, null=True, verbose_name="Research Papers Count"
    )
    employment_rate = models.PositiveIntegerField(
        default=90, blank=True, null=True, verbose_name="Employment Rate (%)"
    )
    facilities = models.JSONField(
        default=list, blank=True, verbose_name="Laboratories & Facilities"
    )
    career_paths = models.TextField(
        blank=True, default="", verbose_name="Career Opportunities"
    )
    guide_document_url = models.CharField(
        max_length=500,
        blank=True,
        default="",
        verbose_name="Study Plan Guide Document URL",
    )
    layout_config = models.JSONField(
        default=default_program_layout,
        blank=True,
        verbose_name="Page Layout Configuration",
    )

    def __str__(self):
        return self.name_en

    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "Programs"


class FacultyMember(models.Model):
    """
    Represents a member of the teaching faculty.
    Matches 'FacultyMember' in the frontend.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faculty_profile",
        verbose_name="User Auth Account",
    )
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
        verbose_name="Faculty",
    )
    name_ar = models.CharField(max_length=255, verbose_name="Name (AR)")
    name_en = models.CharField(max_length=255, verbose_name="Name (EN)")
    title_ar = models.CharField(max_length=255, verbose_name="Title (AR)")
    title_en = models.CharField(max_length=255, verbose_name="Title (EN)")
    department_ar = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Department (AR)"
    )
    department_en = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Department (EN)"
    )
    description_ar = models.TextField(
        blank=True, default="", verbose_name="Description (AR)"
    )
    description_en = models.TextField(
        blank=True, default="", verbose_name="Description (EN)"
    )
    email = models.EmailField(verbose_name="Email Address")
    office_hours = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Office Hours"
    )
    location_ar = models.CharField(
        max_length=255,
        blank=True,
        default="حرم معرة صيدنايا - مبنى الإدارة",
        verbose_name="Location (AR)",
    )
    location_en = models.CharField(
        max_length=255,
        blank=True,
        default="Maarat Saidnaya Campus - Admin Building",
        verbose_name="Location (EN)",
    )
    image = models.TextField(
        blank=True, default="/user.png", verbose_name="Image Path or Base64"
    )
    is_head = models.BooleanField(default=False, verbose_name="Is Head/Dean")
    bio_ar = models.TextField(blank=True, default="", verbose_name="Bio (AR)")
    bio_en = models.TextField(blank=True, default="", verbose_name="Bio (EN)")
    education_ar = models.JSONField(
        blank=True, default=list, verbose_name="Education (AR)"
    )
    education_en = models.JSONField(
        blank=True, default=list, verbose_name="Education (EN)"
    )
    research_ar = models.TextField(
        blank=True, default="", verbose_name="Research Interests (AR)"
    )
    research_en = models.TextField(
        blank=True, default="", verbose_name="Research Interests (EN)"
    )
    publications = models.JSONField(
        blank=True, default=list, verbose_name="Publications List"
    )
    office_hour_slots = models.JSONField(
        blank=True, default=list, verbose_name="Office Hour Slots"
    )
    appointment_location = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Appointment Hall / Room"
    )
    department = models.ForeignKey(
        "Program",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teachers",
        verbose_name="Academic Department",
    )

    def save(self, *args, **kwargs):
        if self.department:
            if self.department.faculty:
                self.faculty = self.department.faculty
            if not self.department_ar or self.department_ar != self.department.name_ar:
                self.department_ar = self.department.name_ar
            if not self.department_en or self.department_en != self.department.name_en:
                self.department_en = self.department.name_en
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_en

    class Meta:
        verbose_name = "Faculty Member"
        verbose_name_plural = "Faculty Members"


class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("name_ar", email.split("@")[0])
        username = extra_fields.get("username") or email
        extra_fields["username"] = username
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Unified Custom User Model representing both auth account & university profile:
    Roles:
    1. admin: مدير النظام
    2. faculty: عضو هيئة تدريسية
    3. alumni: طالب خريج
    4. student: طالب
    5. content_manager: مسؤول إدارة المحتوى
    """

    ROLE_CHOICES = [
        ("admin", "System Admin (مدير النظام)"),
        ("faculty", "Faculty Member (عضو هيئة تدريسية)"),
        ("alumni", "Alumni Student (طالب خريج)"),
        ("student", "Current Student (طالب)"),
        ("content_manager", "Content Manager (مسؤول إدارة المحتوى)"),
    ]

    username = models.CharField(
        max_length=150, unique=True, null=True, blank=True, verbose_name="Username"
    )
    email = models.EmailField(unique=True, verbose_name="Email Address")
    name_ar = models.CharField(max_length=255, verbose_name="Name (AR)")
    name_en = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Name (EN)"
    )
    role = models.CharField(
        max_length=50, choices=ROLE_CHOICES, default="student", verbose_name="User Role"
    )
    assigned_faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="content_managers",
        verbose_name="Assigned Faculty Scope",
    )
    assigned_faculties = models.ManyToManyField(
        Faculty,
        blank=True,
        related_name="scoped_managers",
        verbose_name="Assigned Faculties Scope",
    )
    phone = models.CharField(
        max_length=50, blank=True, default="", verbose_name="Phone Number"
    )
    birth_date = models.DateField(
        null=True, blank=True, verbose_name="Date of Birth / Age"
    )
    bio = models.TextField(
        blank=True, default="", verbose_name="User Bio / Short Description"
    )
    avatar = models.TextField(
        blank=True, default="/user.png", verbose_name="Avatar Path or Base64"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active Account")
    is_staff = models.BooleanField(default=False, verbose_name="Is Staff / Admin Access")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name_ar"]

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        if self.role in ["admin", "content_manager"]:
            self.is_staff = True
        if self.role == "admin":
            self.is_superuser = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name_ar} ({self.role}) - {self.email}"

    @property
    def first_name(self):
        return self.name_ar

    @property
    def last_name(self):
        return self.name_en


class FacultyAppointment(models.Model):
    """
    Represents an office hour appointment booking request for a faculty member.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    faculty_member = models.ForeignKey(
        FacultyMember,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Faculty Member",
    )
    student_name = models.CharField(max_length=255, verbose_name="Student Name")
    student_email = models.EmailField(verbose_name="Student Email")
    student_id = models.CharField(
        max_length=50, blank=True, default="", verbose_name="Student ID"
    )
    day_ar = models.CharField(max_length=100, verbose_name="Day (AR)")
    day_en = models.CharField(max_length=100, verbose_name="Day (EN)")
    time_slot = models.CharField(max_length=100, verbose_name="Time Slot")
    reason = models.TextField(blank=True, default="", verbose_name="Reason")
    status = models.CharField(
        max_length=50, default="pending", choices=STATUS_CHOICES, verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.faculty_member.name_en} ({self.time_slot})"

    class Meta:
        verbose_name = "Faculty Appointment"
        verbose_name_plural = "Faculty Appointments"


class AlumniStory(models.Model):
    """
    Represents successful alumni stories.
    Matches 'AlumniStory' in the frontend.
    """

    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="alumni_stories",
        verbose_name="Faculty",
    )
    name_ar = models.CharField(max_length=255, verbose_name="Name (AR)")
    name_en = models.CharField(max_length=255, verbose_name="Name (EN)")
    graduation_year = models.PositiveIntegerField(verbose_name="Graduation Year")
    program_ar = models.CharField(max_length=255, verbose_name="Program (AR)")
    program_en = models.CharField(max_length=255, verbose_name="Program (EN)")
    current_role_ar = models.CharField(max_length=255, verbose_name="Current Role (AR)")
    current_role_en = models.CharField(max_length=255, verbose_name="Current Role (EN)")
    company_ar = models.CharField(max_length=255, verbose_name="Company (AR)")
    company_en = models.CharField(max_length=255, verbose_name="Company (EN)")
    story_ar = models.TextField(verbose_name="Story (AR)")
    story_en = models.TextField(verbose_name="Story (EN)")
    image = models.CharField(max_length=255, verbose_name="Image Path")

    def __str__(self):
        return self.name_en

    class Meta:
        verbose_name = "Alumni Story"
        verbose_name_plural = "Alumni Stories"


class Course(models.Model):
    """
    Represents a course/subject in the system with curriculum details.
    """

    code = models.CharField(max_length=50, unique=True, verbose_name="Course Code")
    name_ar = models.CharField(max_length=255, verbose_name="Name (AR)")
    name_en = models.CharField(max_length=255, verbose_name="Name (EN)")
    credits = models.PositiveIntegerField(default=3, verbose_name="Credits")
    program = models.ForeignKey(
        "Program",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="Academic Program",
    )
    year = models.PositiveIntegerField(default=1, verbose_name="Study Year (1-5)")
    semester = models.PositiveIntegerField(default=1, verbose_name="Semester (1 or 2)")
    description_ar = models.TextField(
        blank=True, default="", verbose_name="Description (AR)"
    )
    description_en = models.TextField(
        blank=True, default="", verbose_name="Description (EN)"
    )
    prerequisites_text = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Prerequisites"
    )

    def __str__(self):
        return f"{self.name_en} ({self.code})"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["year", "semester", "code"]


class Student(models.Model):
    """
    Represents a student profile linked to user auth.
    """

    RANK_CHOICES = [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
        null=True,
        blank=True,
        verbose_name="User Account",
    )
    student_id = models.CharField(max_length=50, unique=True, verbose_name="Student ID")
    name_ar = models.CharField(max_length=255, verbose_name="Name (AR)")
    name_en = models.CharField(max_length=255, verbose_name="Name (EN)")
    email = models.EmailField(verbose_name="Email")
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="students",
        verbose_name="Faculty",
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="students",
        verbose_name="Program",
    )
    year = models.PositiveIntegerField(default=1, verbose_name="Year of Study")
    gpa = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.00, verbose_name="GPA"
    )
    total_credits = models.PositiveIntegerField(default=0, verbose_name="Total Credits")
    completed_credits = models.PositiveIntegerField(
        default=0, verbose_name="Completed Credits"
    )
    image = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Image Path"
    )
    is_top = models.BooleanField(default=False, verbose_name="Is Top Student")
    rank = models.PositiveIntegerField(
        choices=RANK_CHOICES, blank=True, null=True, verbose_name="Rank"
    )

    def save(self, *args, **kwargs):
        if self.program and self.program.faculty:
            self.faculty = self.program.faculty
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name_en} ({self.student_id})"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class ScheduleItem(models.Model):
    """
    Represents a schedule class session for a student.
    Matches 'studentSchedule' in the frontend.
    """

    DAY_CHOICES = [
        ("sunday", "Sunday"),
        ("monday", "Monday"),
        ("tuesday", "Tuesday"),
        ("wednesday", "Wednesday"),
        ("thursday", "Thursday"),
        ("friday", "Friday"),
        ("saturday", "Saturday"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="schedule_items",
        verbose_name="Student",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="schedule_items",
        verbose_name="Course",
    )
    day = models.CharField(max_length=50, choices=DAY_CHOICES, verbose_name="Day Slug")
    day_ar = models.CharField(max_length=50, verbose_name="Day Name (AR)")
    day_en = models.CharField(max_length=50, verbose_name="Day Name (EN)")
    time = models.CharField(
        max_length=100, verbose_name="Time Period (e.g. 08:00 - 09:30)"
    )
    room = models.CharField(max_length=100, verbose_name="Class Room")
    instructor = models.CharField(max_length=255, verbose_name="Instructor Name (AR)")
    instructor_en = models.CharField(
        max_length=255, verbose_name="Instructor Name (EN)"
    )

    def __str__(self):
        return f"{self.student.name_en} - {self.course.code} on {self.day_en}"

    class Meta:
        verbose_name = "Schedule Item"
        verbose_name_plural = "Schedule Items"


class StudentGrade(models.Model):
    """
    Represents grades of a student.
    Matches 'studentGrades' in the frontend.
    """

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="grades", verbose_name="Student"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="grades", verbose_name="Course"
    )
    grade = models.CharField(max_length=20, verbose_name="Letter Grade (e.g. A, B+)")
    points = models.DecimalField(
        max_digits=3, decimal_places=2, verbose_name="GPA Points"
    )

    def __str__(self):
        return f"{self.student.name_en} - {self.course.code}: {self.grade}"

    class Meta:
        verbose_name = "Student Grade"
        verbose_name_plural = "Student Grades"


class NewsArticle(models.Model):
    """
    Represents a news article or announcement across university, faculty, and department levels.
    Matches 'NewsArticle' in the frontend.
    """

    CATEGORY_CHOICES = [
        ("announcement", "Announcement"),
        ("event", "Event"),
        ("achievement", "Achievement"),
        ("research", "Research"),
    ]

    SCOPE_CHOICES = [
        ("university", "University-Wide"),
        ("faculty", "Faculty-Level"),
        ("department", "Department-Level"),
    ]

    STATUS_CHOICES = [
        ("published", "Published"),
        ("draft", "Draft"),
        ("archived", "Archived"),
    ]

    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    title_ar = models.CharField(max_length=255, verbose_name="Title (AR)")
    title_en = models.CharField(max_length=255, verbose_name="Title (EN)")
    excerpt_ar = models.TextField(verbose_name="Excerpt (AR)")
    excerpt_en = models.TextField(verbose_name="Excerpt (EN)")
    content_ar = models.TextField(verbose_name="Content (AR)")
    content_en = models.TextField(verbose_name="Content (EN)")
    image = models.TextField(blank=True, default="", verbose_name="Cover Image Path or URL")
    image_caption_ar = models.CharField(max_length=255, blank=True, default="", verbose_name="Image Caption (AR)")
    image_caption_en = models.CharField(max_length=255, blank=True, default="", verbose_name="Image Caption (EN)")
    
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, verbose_name="Category"
    )
    scope = models.CharField(
        max_length=20, choices=SCOPE_CHOICES, default="university", verbose_name="Publishing Scope"
    )
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news_articles",
        verbose_name="Target Faculty Scope",
    )
    program = models.ForeignKey(
        "Program",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news_articles",
        verbose_name="Target Department / Program Scope",
    )

    # Attribution & Editorial Metadata
    author_name_ar = models.CharField(max_length=255, blank=True, default="", verbose_name="Author / Source Name (AR)")
    author_name_en = models.CharField(max_length=255, blank=True, default="", verbose_name="Author / Source Name (EN)")
    author_title_ar = models.CharField(max_length=255, blank=True, default="", verbose_name="Author Title / Role (AR)")
    author_title_en = models.CharField(max_length=255, blank=True, default="", verbose_name="Author Title / Role (EN)")
    reading_time = models.PositiveIntegerField(default=3, verbose_name="Reading Time (Minutes)")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Views Count")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="published", verbose_name="Publication Status")

    # Rich Media Galleries and Attachments
    gallery_images = models.JSONField(
        default=list, blank=True, verbose_name="Gallery Images [{url, caption_ar, caption_en}]"
    )
    attachments = models.JSONField(
        default=list, blank=True, verbose_name="Document Attachments [{title_ar, title_en, url, size, file_type}]"
    )

    date = models.DateField(verbose_name="Publish Date")
    featured = models.BooleanField(default=False, verbose_name="Featured (Syndicate to Home)")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"
        ordering = ["-date", "-id"]


class Event(models.Model):
    """
    Represents university events.
    Matches 'Event' in the frontend.
    """

    TYPE_CHOICES = [
        ("academic", "Academic"),
        ("cultural", "Cultural"),
        ("sports", "Sports"),
        ("career", "Career"),
    ]

    title_ar = models.CharField(max_length=255, verbose_name="Title (AR)")
    title_en = models.CharField(max_length=255, verbose_name="Title (EN)")
    description_ar = models.TextField(verbose_name="Description (AR)")
    description_en = models.TextField(verbose_name="Description (EN)")
    date = models.DateField(verbose_name="Event Date")
    time = models.CharField(max_length=100, verbose_name="Event Time")
    location_ar = models.CharField(max_length=255, verbose_name="Location (AR)")
    location_en = models.CharField(max_length=255, verbose_name="Location (EN)")
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, verbose_name="Event Type"
    )
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
        verbose_name="Target Faculty Scope",
    )

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"


class AcademicCalendarEvent(models.Model):
    """
    Represents an item in the Academic Calendar.
    """

    event_ar = models.CharField(max_length=255, verbose_name="Event Name (AR)")
    event_en = models.CharField(max_length=255, verbose_name="Event Name (EN)")
    date_ar = models.CharField(max_length=100, verbose_name="Date / Month (AR)")
    date_en = models.CharField(max_length=100, verbose_name="Date / Month (EN)")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"{self.event_en} ({self.date_en})"

    class Meta:
        verbose_name = "Academic Calendar Event"
        verbose_name_plural = "Academic Calendar Events"
        ordering = ["order", "id"]


class JobOffer(models.Model):
    """
    Represents a university job opening / vacancy.
    """

    TYPE_CHOICES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("contract", "Contract"),
    ]

    title_ar = models.CharField(max_length=255, verbose_name="Job Title (AR)")
    title_en = models.CharField(max_length=255, verbose_name="Job Title (EN)")
    department_ar = models.CharField(max_length=255, verbose_name="Department (AR)")
    department_en = models.CharField(max_length=255, verbose_name="Department (EN)")
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default="full_time",
        verbose_name="Job Type",
    )
    location_ar = models.CharField(
        max_length=255, default="حرم معرة صيدنايا", verbose_name="Location (AR)"
    )
    location_en = models.CharField(
        max_length=255, default="Maarat Saidnaya Campus", verbose_name="Location (EN)"
    )
    deadline = models.CharField(max_length=100, verbose_name="Application Deadline")
    requirements_ar = models.TextField(verbose_name="Requirements (AR)")
    requirements_en = models.TextField(verbose_name="Requirements (EN)")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return self.title_ar

    class Meta:
        verbose_name = "Job Offer"
        verbose_name_plural = "Job Offers"


class JobApplication(models.Model):
    """
    Represents a job application submitted by an applicant.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("under_review", "Under Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    job = models.ForeignKey(
        JobOffer,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name="Job Offer",
    )
    applicant_name = models.CharField(max_length=255, verbose_name="Applicant Name")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=50, verbose_name="Phone Number")
    cover_letter = models.TextField(blank=True, verbose_name="Cover Letter")
    resume_url = models.CharField(
        max_length=500, blank=True, verbose_name="Resume / CV Link"
    )
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="pending", verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted At")

    def __str__(self):
        return f"{self.applicant_name} - {self.job.title_ar}"

    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"


class AdmissionApplication(models.Model):
    """
    Represents a university admission application submitted by a prospective student.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("under_review", "Under Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    full_name_ar = models.CharField(max_length=255, verbose_name="Full Name (AR)")
    full_name_en = models.CharField(max_length=255, verbose_name="Full Name (EN)")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=50, verbose_name="Phone Number")
    high_school_branch = models.CharField(
        max_length=100, verbose_name="High School Branch"
    )
    high_school_score = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="High School Score (%)"
    )
    desired_faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Desired Faculty",
    )
    desired_program = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Desired Program",
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Application Status",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submission Date")

    def __str__(self):
        return f"{self.full_name_ar} ({self.email})"

    class Meta:
        verbose_name = "Admission Application"
        verbose_name_plural = "Admission Applications"


class Notification(models.Model):
    """
    Represents a system or targeted user notification/alert.
    """

    TYPE_CHOICES = [
        ("message", "New Message (رسالة جديدة)"),
        ("result", "Results Published (تم نشر النتائج)"),
        ("info", "Information (تنبيه عام)"),
        ("warning", "Warning (تحذير)"),
        ("urgent", "Urgent (عاجل)"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
        verbose_name="Target User",
    )
    title_ar = models.CharField(max_length=255, verbose_name="Title (AR)")
    title_en = models.CharField(max_length=255, verbose_name="Title (EN)")
    message_ar = models.TextField(verbose_name="Message (AR)")
    message_en = models.TextField(verbose_name="Message (EN)")
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default="info",
        verbose_name="Notification Type",
    )
    link = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Action Link"
    )
    is_read = models.BooleanField(default=False, verbose_name="Is Read")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"{self.title_ar} ({'Read' if self.is_read else 'Unread'})"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]


class ActivityLog(models.Model):
    """
    Represents system audit logs / activity logs for admin actions.
    """

    STATUS_CHOICES = [
        ("update", "Update (تعديل)"),
        ("success", "Success / Publish (نشر / نجاح)"),
        ("warning", "Warning / Alert (تحذير)"),
        ("info", "Information (معلومات)"),
    ]

    user_name = models.CharField(max_length=255, verbose_name="User / System Name")
    user_name_en = models.CharField(
        max_length=255, blank=True, default="", verbose_name="User / System Name (EN)"
    )
    action_ar = models.TextField(verbose_name="Action Description (AR)")
    action_en = models.TextField(verbose_name="Action Description (EN)")
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="info", verbose_name="Log Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"{self.user_name} - {self.action_ar[:30]}"

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        ordering = ["-created_at"]


class UserNotificationState(models.Model):
    """
    Tracks per-user read state for broadcast and targeted notifications.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_states",
        verbose_name="User",
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="user_states",
        verbose_name="Notification",
    )
    is_read = models.BooleanField(default=False, verbose_name="Is Read")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="Read At")

    class Meta:
        unique_together = ("user", "notification")
        verbose_name = "User Notification State"
        verbose_name_plural = "User Notification States"


class UserNotificationPreference(models.Model):
    """
    Stores user notification preferences / category mute settings.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_preference",
        verbose_name="User",
    )
    mute_messages = models.BooleanField(
        default=False, verbose_name="Mute Message Alerts"
    )
    mute_results = models.BooleanField(default=False, verbose_name="Mute Result Alerts")
    mute_info = models.BooleanField(default=False, verbose_name="Mute Info Alerts")
    mute_warning = models.BooleanField(
        default=False, verbose_name="Mute Warning Alerts"
    )
    mute_urgent = models.BooleanField(default=False, verbose_name="Mute Urgent Alerts")

    def __str__(self):
        return f"Notification Preferences for {self.user.username}"

    class Meta:
        verbose_name = "User Notification Preference"
        verbose_name_plural = "User Notification Preferences"


def default_social_links():
    return {
        "facebook": {
            "key": "facebook",
            "nameAr": "فيسبوك",
            "nameEn": "Facebook",
            "url": "https://www.facebook.com/asu.edu.sy.private",
            "enabled": True,
        },
        "linkedin": {
            "key": "linkedin",
            "nameAr": "لينكد إن",
            "nameEn": "LinkedIn",
            "url": "https://linkedin.com/school/antioch-syrian-university",
            "enabled": True,
        },
        "youtube": {
            "key": "youtube",
            "nameAr": "يوتيوب",
            "nameEn": "YouTube",
            "url": "https://youtube.com/@antiochsyrianuniversity",
            "enabled": True,
        },
        "instagram": {
            "key": "instagram",
            "nameAr": "إنستغرام",
            "nameEn": "Instagram",
            "url": "https://instagram.com/asu_syria",
            "enabled": True,
        },
        "telegram": {
            "key": "telegram",
            "nameAr": "تلجرام",
            "nameEn": "Telegram",
            "url": "https://t.me/asu_syria",
            "enabled": True,
        },
        "twitter": {
            "key": "twitter",
            "nameAr": "منصة X",
            "nameEn": "X",
            "url": "https://x.com/asu_syria",
            "enabled": True,
        },
    }


def default_contact_fields():
    return {
        "email": {"value": "info@asu.edu.sy", "enabled": True},
        "phone": {"value": "(+963) 11 5954910", "enabled": True},
        "address": {
            "valueAr": "معرة صيدنايا، ريف دمشق، سوريا",
            "valueEn": "Maarat Saidnaya, Damascus Countryside, Syria",
            "value": "معرة صيدنايا، ريف دمشق، سوريا",
            "enabled": True,
        },
        "officeAddress": {
            "valueAr": "دمشق، البرامكة، مقابل كلية الحقوق - مكتب المتابعة والتسجيل",
            "valueEn": "Damascus, Baramkeh, Opposite Faculty of Law - Follow-up & Registration Office",
            "value": "دمشق، البرامكة، مقابل كلية الحقوق - مكتب المتابعة والتسجيل",
            "enabled": True,
        },
        "workingHours": {
            "valueAr": "الأحد - الخميس: 8:00 ص - 4:00 م",
            "valueEn": "Sunday - Thursday: 8:00 AM - 4:00 PM",
            "value": "الأحد - الخميس: 8:00 ص - 4:00 م",
            "enabled": True,
        },
    }


class SiteSetting(models.Model):
    """
    Stores system-wide configuration, university contact info, and social media links.
    """

    email = models.EmailField(default="info@asu.edu.sy", verbose_name="Email")
    phone = models.CharField(
        max_length=100, default="(+963) 11 5954910", verbose_name="Inquiries Phone"
    )
    address = models.CharField(
        max_length=255,
        default="معرة صيدنايا، ريف دمشق، سوريا",
        verbose_name="Main Campus Address (AR)",
    )
    address_en = models.CharField(
        max_length=255,
        default="Maarat Saidnaya, Damascus Countryside, Syria",
        blank=True,
        verbose_name="Main Campus Address (EN)",
    )
    office_address = models.CharField(
        max_length=255,
        default="دمشق، البرامكة، مقابل كلية الحقوق - مكتب المتابعة والتسجيل",
        blank=True,
        verbose_name="Office Address (AR)",
    )
    office_address_en = models.CharField(
        max_length=255,
        default="Damascus, Baramkeh, Opposite Faculty of Law - Follow-up & Registration Office",
        blank=True,
        verbose_name="Office Address (EN)",
    )
    working_hours = models.CharField(
        max_length=255,
        default="الأحد - الخميس: 8:00 ص - 4:00 م",
        blank=True,
        verbose_name="Working Hours (AR)",
    )
    working_hours_en = models.CharField(
        max_length=255,
        default="Sunday - Thursday: 8:00 AM - 4:00 PM",
        blank=True,
        verbose_name="Working Hours (EN)",
    )
    contact_fields = models.JSONField(
        default=default_contact_fields, blank=True, verbose_name="Contact Fields JSON"
    )
    registration_open = models.BooleanField(
        default=True, verbose_name="Open Registration"
    )
    maintenance_mode = models.BooleanField(
        default=False, verbose_name="Maintenance Mode"
    )
    show_results = models.BooleanField(default=True, verbose_name="Show Public Results")
    social_links = models.JSONField(
        default=default_social_links, blank=True, verbose_name="Social Media Links JSON"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Site Setting (#{self.pk})"

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"


@receiver(pre_delete, sender=Program)
def handle_program_deletion(sender, instance, **kwargs):
    # Nullify teachers department and clear stale text values
    FacultyMember.objects.filter(department=instance).update(
        department=None,
        department_ar="",
        department_en="",
    )
    # Log to ActivityLog
    try:
        ActivityLog.objects.create(
            user_name="System",
            action_ar=f"تم حذف القسم/التخصص ({instance.name_ar}) وتم فك ارتباط كافة المدرسين التابعين له",
            action_en=f"Program ({instance.name_en}) deleted; all linked teachers disassociated",
            status="warning",
        )
    except Exception:
        pass


class Book(models.Model):
    """
    Represents an Academic Book or Scientific Reference in ASU Central Library.
    Supports physical copies tracking and strictly verified PDF digital editions.
    """

    title_ar = models.CharField(max_length=255, verbose_name="Title (AR)")
    title_en = models.CharField(max_length=255, verbose_name="Title (EN)")
    author_ar = models.CharField(max_length=255, verbose_name="Author (AR)")
    author_en = models.CharField(max_length=255, verbose_name="Author (EN)")
    isbn = models.CharField(max_length=50, blank=True, default="", verbose_name="ISBN")

    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
        verbose_name="Faculty",
    )
    category = models.CharField(
        max_length=50,
        default="engineering",
        verbose_name="Category Slug",
    )
    category_name_ar = models.CharField(
        max_length=100, blank=True, default="", verbose_name="Category Name (AR)"
    )
    category_name_en = models.CharField(
        max_length=100, blank=True, default="", verbose_name="Category Name (EN)"
    )

    publication_year = models.PositiveIntegerField(
        default=2024, verbose_name="Publication Year"
    )
    edition = models.CharField(
        max_length=100, blank=True, default="", verbose_name="Edition"
    )
    pages_count = models.PositiveIntegerField(default=0, verbose_name="Pages Count")
    language = models.CharField(
        max_length=50, default="العربية", verbose_name="Language"
    )

    description_ar = models.TextField(
        blank=True, default="", verbose_name="Description (AR)"
    )
    description_en = models.TextField(
        blank=True, default="", verbose_name="Description (EN)"
    )

    # Cover art
    cover_image = models.TextField(
        blank=True, default="", verbose_name="Cover Image URL"
    )
    cover_color = models.CharField(
        max_length=100,
        default="from-blue-600 to-indigo-950",
        verbose_name="Fallback Cover Gradient",
    )

    # Digital document (PDF strictly)
    pdf_file = models.TextField(blank=True, default="", verbose_name="PDF File URL")
    pdf_file_size = models.PositiveBigIntegerField(
        default=0, verbose_name="PDF File Size (Bytes)"
    )
    pdf_file_size_formatted = models.CharField(
        max_length=30, blank=True, default="", verbose_name="PDF File Size Formatted"
    )
    allow_download = models.BooleanField(
        default=True, verbose_name="Allow Direct PDF Download"
    )

    # Physical inventory & availability
    total_copies = models.PositiveIntegerField(
        default=1, verbose_name="Total Physical Copies"
    )
    available_copies = models.PositiveIntegerField(
        default=1, verbose_name="Available Copies"
    )
    shelf_location = models.CharField(
        max_length=100, blank=True, default="", verbose_name="Shelf Location"
    )
    is_available = models.BooleanField(
        default=True, verbose_name="Available for Borrowing"
    )

    # Metrics
    views_count = models.PositiveIntegerField(default=0, verbose_name="Views Count")
    downloads_count = models.PositiveIntegerField(
        default=0, verbose_name="Downloads Count"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title_ar} - {self.author_ar} ({self.isbn})"

    class Meta:
        verbose_name = "Academic Book"
        verbose_name_plural = "Academic Books"
        ordering = ["-created_at"]


class BookReservation(models.Model):
    """
    Tracks book borrow and reservation requests from students.
    """

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار (Pending)"),
        ("approved", "تمت الموافقة (Approved)"),
        ("borrowed", "مستعار حالياً (Borrowed)"),
        ("returned", "تمت الإعادة (Returned)"),
        ("cancelled", "ملغى (Cancelled)"),
        ("rejected", "مرفوض (Rejected)"),
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="Book",
    )
    student_name = models.CharField(max_length=200, verbose_name="Student Name")
    student_id = models.CharField(
        max_length=50, verbose_name="Student University ID"
    )
    student_major = models.CharField(
        max_length=150, blank=True, default="", verbose_name="Student Major"
    )
    student_email = models.EmailField(
        blank=True, default="", verbose_name="Student Email"
    )
    student_phone = models.CharField(
        max_length=50, blank=True, default="", verbose_name="Student Phone"
    )

    status = models.CharField(
        max_length=30, default="pending", choices=STATUS_CHOICES, verbose_name="Status"
    )
    reserved_at = models.DateTimeField(auto_now_add=True, verbose_name="Reserved At")
    expires_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Pickup Expiration Date"
    )
    returned_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Returned At"
    )

    notes = models.TextField(blank=True, default="", verbose_name="Student Notes")
    admin_notes = models.TextField(
        blank=True, default="", verbose_name="Admin Notes"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservation: {self.student_name} -> {self.book.title_ar} [{self.status}]"

    class Meta:
        verbose_name = "Book Reservation"
        verbose_name_plural = "Book Reservations"
        ordering = ["-reserved_at"]


class ResearchCenter(models.Model):
    """
    Academic Research Centers at Antioch Syrian University
    """
    title_ar = models.CharField(max_length=255, verbose_name="Center Title (AR)")
    title_en = models.CharField(max_length=255, verbose_name="Center Title (EN)")
    description_ar = models.TextField(verbose_name="Description (AR)")
    description_en = models.TextField(verbose_name="Description (EN)")
    icon = models.CharField(max_length=100, default="Microscope", verbose_name="Icon Name")
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="research_centers",
        verbose_name="Associated Faculty",
    )
    director_name_ar = models.CharField(
        max_length=200, blank=True, default="", verbose_name="Director Name (AR)"
    )
    director_name_en = models.CharField(
        max_length=200, blank=True, default="", verbose_name="Director Name (EN)"
    )
    location = models.CharField(
        max_length=200, blank=True, default="", verbose_name="Location / Campus Wing"
    )
    contact_email = models.EmailField(
        blank=True, default="", verbose_name="Contact Email"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_ar

    class Meta:
        verbose_name = "Research Center"
        verbose_name_plural = "Research Centers"
        ordering = ["order", "created_at"]


class ResearchArea(models.Model):
    """
    Research Areas & Disciplines at ASU
    """
    name_ar = models.CharField(max_length=150, verbose_name="Area Name (AR)")
    name_en = models.CharField(max_length=150, verbose_name="Area Name (EN)")
    description_ar = models.TextField(
        blank=True, default="", verbose_name="Description (AR)"
    )
    description_en = models.TextField(
        blank=True, default="", verbose_name="Description (EN)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_ar

    class Meta:
        verbose_name = "Research Area"
        verbose_name_plural = "Research Areas"
        ordering = ["order", "name_ar"]


class ResearchPublication(models.Model):
    """
    Published Scientific Papers and Articles
    """
    title_ar = models.CharField(max_length=350, verbose_name="Publication Title (AR)")
    title_en = models.CharField(max_length=350, verbose_name="Publication Title (EN)")
    authors_ar = models.CharField(max_length=300, verbose_name="Authors (AR)")
    authors_en = models.CharField(max_length=300, verbose_name="Authors (EN)")
    journal_ar = models.CharField(
        max_length=250, verbose_name="Journal / Conference (AR)"
    )
    journal_en = models.CharField(
        max_length=250, verbose_name="Journal / Conference (EN)"
    )
    publication_year = models.PositiveIntegerField(
        default=2024, verbose_name="Publication Year"
    )

    research_area = models.ForeignKey(
        ResearchArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="publications",
        verbose_name="Research Area",
    )
    center = models.ForeignKey(
        ResearchCenter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="publications",
        verbose_name="Research Center",
    )
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="research_publications",
        verbose_name="Faculty",
    )

    abstract_ar = models.TextField(blank=True, default="", verbose_name="Abstract (AR)")
    abstract_en = models.TextField(blank=True, default="", verbose_name="Abstract (EN)")

    doi_url = models.URLField(
        max_length=500, blank=True, default="", verbose_name="DOI or Article URL"
    )
    pdf_file = models.TextField(blank=True, default="", verbose_name="PDF File URL")
    pdf_file_size = models.PositiveBigIntegerField(
        default=0, verbose_name="PDF File Size (Bytes)"
    )
    pdf_file_size_formatted = models.CharField(
        max_length=30, blank=True, default="", verbose_name="PDF File Size Formatted"
    )

    views_count = models.PositiveIntegerField(default=0, verbose_name="Views Count")
    downloads_count = models.PositiveIntegerField(
        default=0, verbose_name="Downloads Count"
    )

    is_featured = models.BooleanField(default=False, verbose_name="Is Featured")
    is_active = models.BooleanField(default=True, verbose_name="Is Published/Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title_ar} ({self.publication_year})"

    class Meta:
        verbose_name = "Research Publication"
        verbose_name_plural = "Research Publications"
        ordering = ["-publication_year", "-created_at"]


class HousingFeature(models.Model):
    """
    Features and amenities offered in student housing.
    """
    title_ar = models.CharField(max_length=200, verbose_name="Title (AR)")
    title_en = models.CharField(max_length=200, blank=True, default="", verbose_name="Title (EN)")
    description_ar = models.TextField(verbose_name="Description (AR)")
    description_en = models.TextField(blank=True, default="", verbose_name="Description (EN)")
    icon = models.CharField(max_length=50, default="Bed", verbose_name="Icon Name")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_ar

    class Meta:
        verbose_name = "Housing Feature"
        verbose_name_plural = "Housing Features"
        ordering = ["order", "id"]


class StudentClub(models.Model):
    """
    Student clubs and cultural/scientific groups.
    """
    name_ar = models.CharField(max_length=200, verbose_name="Club Name (AR)")
    name_en = models.CharField(max_length=200, blank=True, default="", verbose_name="Club Name (EN)")
    description_ar = models.TextField(verbose_name="Description (AR)")
    description_en = models.TextField(blank=True, default="", verbose_name="Description (EN)")
    icon = models.CharField(max_length=50, default="Users", verbose_name="Icon Name")
    category = models.CharField(max_length=100, blank=True, default="عام", verbose_name="Category")
    supervisor = models.CharField(max_length=200, blank=True, default="", verbose_name="Supervisor / Leader")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_ar

    class Meta:
        verbose_name = "Student Club"
        verbose_name_plural = "Student Clubs"
        ordering = ["order", "id"]


class SportActivity(models.Model):
    """
    Sports and athletic activities/disciplines.
    """
    name_ar = models.CharField(max_length=200, verbose_name="Sport Name (AR)")
    name_en = models.CharField(max_length=200, blank=True, default="", verbose_name="Sport Name (EN)")
    description_ar = models.TextField(blank=True, default="", verbose_name="Description (AR)")
    description_en = models.TextField(blank=True, default="", verbose_name="Description (EN)")
    icon = models.CharField(max_length=50, default="Dumbbell", verbose_name="Icon Name")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_ar

    class Meta:
        verbose_name = "Sport Activity"
        verbose_name_plural = "Sport Activities"
        ordering = ["order", "id"]


class CampusLifeOverview(models.Model):
    """
    Singleton-style overview configuration for Campus Life section texts and banners.
    """
    housing_title_ar = models.CharField(max_length=255, default="السكن الجامعي")
    housing_title_en = models.CharField(max_length=255, default="Student Housing")
    housing_desc_ar = models.TextField(
        default="توفر جامعة أنطاكية السورية سكناً جامعياً مريحاً وآمناً للطلاب من خارج دمشق، مع توفير جميع الخدمات الأساسية."
    )
    housing_desc_en = models.TextField(
        default="Antioch Syrian University provides comfortable and safe housing for students from outside Damascus, with all essential services."
    )
    housing_image = models.CharField(max_length=500, blank=True, default="/images/pages/campus-life.png")
    housing_contact_note_ar = models.TextField(default="تواصل مع قسم شؤون الطلاب للحصول على مزيد من المعلومات")
    housing_contact_note_en = models.TextField(default="Contact the Student Affairs department for more information")

    sports_title_ar = models.CharField(max_length=255, default="الأنشطة الرياضية")
    sports_title_en = models.CharField(max_length=255, default="Sports Activities")
    sports_desc_ar = models.TextField(
        default="تولي الجامعة اهتماماً كبيراً بالجانب الرياضي وتوفر مرافق رياضية متنوعة للطلاب."
    )
    sports_desc_en = models.TextField(
        default="The university pays great attention to sports and provides various sports facilities for students."
    )
    sports_image = models.CharField(max_length=500, blank=True, default="/images/pages/campus-life.png")
    championships_title_ar = models.CharField(max_length=255, default="البطولات السنوية")
    championships_title_en = models.CharField(max_length=255, default="Annual Championships")
    championships_desc_ar = models.TextField(
        default="تنظم الجامعة بطولات رياضية سنوية بين الكليات في مختلف الألعاب"
    )
    championships_desc_en = models.TextField(
        default="The university organizes annual sports championships between faculties in various games"
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Campus Life Overview"

    class Meta:
        verbose_name = "Campus Life Overview"
        verbose_name_plural = "Campus Life Overviews"





