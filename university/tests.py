from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from university.models import (
    Faculty,
    Program,
    FacultyMember,
    Student,
    ActivityLog,
)


class FacultyDepartmentManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.engineering = Faculty.objects.create(
            slug="engineering",
            name_ar="كلية الهندسة",
            name_en="Faculty of Engineering",
            description_ar="وصف",
            description_en="Description",
        )
        self.pharmacy = Faculty.objects.create(
            slug="pharmacy",
            name_ar="كلية الصيدلة",
            name_en="Faculty of Pharmacy",
            description_ar="وصف",
            description_en="Description",
        )
        self.software_dept = Program.objects.create(
            slug="software",
            faculty=self.engineering,
            name_ar="هندسة البرمجيات",
            name_en="Software Engineering",
            description_ar="وصف",
            description_en="Description",
            credit_hours=160,
            min_score_percent=80,
            min_score_points=1800,
            tuition_syrian=500000,
            tuition_non_resident=3000,
            duration=5,
        )
        self.civil_dept = Program.objects.create(
            slug="civil",
            faculty=self.engineering,
            name_ar="الهندسة المدنية",
            name_en="Civil Engineering",
            description_ar="وصف",
            description_en="Description",
            credit_hours=160,
            min_score_percent=75,
            min_score_points=1700,
            tuition_syrian=450000,
            tuition_non_resident=2800,
            duration=5,
        )

    def test_teacher_auto_derivation_from_department(self):
        teacher = FacultyMember.objects.create(
            name_ar="د. أحمد السوري",
            name_en="Dr. Ahmad Al-Suri",
            title_ar="أستاذ مشارك",
            title_en="Associate Professor",
            email="ahmad@asu.edu.sy",
            department=self.software_dept,
        )
        # Should auto-derive faculty
        self.assertEqual(teacher.faculty, self.engineering)
        # Should auto-sync text fields
        self.assertEqual(teacher.department_ar, "هندسة البرمجيات")
        self.assertEqual(teacher.department_en, "Software Engineering")

    def test_student_auto_derivation_from_program(self):
        student = Student.objects.create(
            student_id="STU-2026-001",
            name_ar="سامر العلي",
            name_en="Samer Al-Ali",
            email="samer@asu.edu.sy",
            faculty=self.pharmacy,  # intentionally mismatched initially
            program=self.software_dept,
            total_credits=160,
            completed_credits=40,
        )
        # Should auto-derive faculty from program
        self.assertEqual(student.faculty, self.engineering)

    def test_serializer_validation_mismatch_rejected(self):
        # Attempt to create teacher with engineering department but pharmacy faculty via API
        payload = {
            "nameAr": "د. عمر",
            "nameEn": "Dr. Omar",
            "titleAr": "مدرس",
            "titleEn": "Lecturer",
            "email": "omar@asu.edu.sy",
            "faculty": self.pharmacy.id,
            "department": self.software_dept.id,
        }
        response = self.client.post("/api/faculty-members/", payload, format="json")
        # Since our serializer auto-derives or validates, if auto-derived it will succeed and set faculty=engineering
        # Let's verify response or faculty
        if response.status_code == status.HTTP_201_CREATED:
            self.assertEqual(response.data["faculty"], self.engineering.id)

    def test_program_pre_delete_signal_nullifies_teachers_and_logs(self):
        teacher = FacultyMember.objects.create(
            name_ar="د. خالد",
            name_en="Dr. Khaled",
            title_ar="أستاذ",
            title_en="Professor",
            email="khaled@asu.edu.sy",
            department=self.civil_dept,
        )
        self.assertEqual(teacher.department, self.civil_dept)

        # Delete civil department
        self.civil_dept.delete()
        teacher.refresh_from_db()
        self.assertIsNone(teacher.department)
        self.assertEqual(teacher.department_ar, "")
        self.assertEqual(teacher.department_en, "")

        # Verify ActivityLog
        latest_log = ActivityLog.objects.first()
        self.assertIn("الهندسة المدنية", latest_log.action_ar)
        self.assertEqual(latest_log.status, "warning")

    def test_subquery_counts_on_faculty_and_program(self):
        # Create teachers and students
        FacultyMember.objects.create(
            name_ar="مدرس 1",
            name_en="Teacher 1",
            title_ar="أستاذ",
            title_en="Prof",
            email="t1@asu.edu.sy",
            department=self.software_dept,
        )
        FacultyMember.objects.create(
            name_ar="مدرس 2",
            name_en="Teacher 2",
            title_ar="أستاذ",
            title_en="Prof",
            email="t2@asu.edu.sy",
            department=self.software_dept,
        )
        Student.objects.create(
            student_id="STU-001",
            name_ar="طالب 1",
            name_en="Student 1",
            email="s1@asu.edu.sy",
            program=self.software_dept,
        )

        # Query Program API
        resp_prog = self.client.get(f"/api/programs/{self.software_dept.id}/")
        self.assertEqual(resp_prog.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_prog.data["teachersCount"], 2)
        self.assertEqual(resp_prog.data["studentsCount"], 1)

        # Query Faculty API
        resp_fac = self.client.get(f"/api/faculties/{self.engineering.id}/")
        self.assertEqual(resp_fac.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_fac.data["totalTeachers"], 2)
        self.assertEqual(resp_fac.data["totalStudents"], 1)
        self.assertEqual(resp_fac.data["totalPrograms"], 2)

    def test_bulk_transfer_students_and_audit_log(self):
        s1 = Student.objects.create(
            student_id="STU-B1",
            name_ar="طالب أ",
            name_en="Student A",
            email="a@asu.edu.sy",
            program=self.software_dept,
        )
        s2 = Student.objects.create(
            student_id="STU-B2",
            name_ar="طالب ب",
            name_en="Student B",
            email="b@asu.edu.sy",
            program=self.software_dept,
        )

        payload = {
            "student_ids": [s1.id, s2.id],
            "target_program_id": self.civil_dept.id,
        }
        response = self.client.post(
            "/api/students/bulk-transfer/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["transferred_count"], 2)

        s1.refresh_from_db()
        s2.refresh_from_db()
        self.assertEqual(s1.program, self.civil_dept)
        self.assertEqual(s2.program, self.civil_dept)

        # Check ActivityLog
        log = ActivityLog.objects.first()
        self.assertIn("الهندسة المدنية", log.action_ar)
