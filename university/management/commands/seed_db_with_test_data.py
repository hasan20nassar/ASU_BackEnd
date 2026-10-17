import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
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
    UserProfile,
)

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds the database with initial university data matching the frontend mock data."

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")
        
        with transaction.atomic():
            # 1. Create Superuser / Admin User
            admin_user, created = User.objects.get_or_create(
                email="admin@admin.com",
                defaults={
                    "username": "admin",
                    "name_ar": "مدير النظام الرئيسي",
                    "name_en": "Super Admin",
                    "role": "admin",
                    "phone": "+963911111111",
                    "bio": "الحساب الإداري الرئيسي للتحكم بالبوابة ولوحة إدارة الجامعة",
                    "avatar": "/user.png",
                    "is_active": True,
                    "is_staff": True,
                    "is_superuser": True,
                },
            )
            admin_user.username = "admin"
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.role = "admin"
            admin_user.set_password("admin123")
            admin_user.save()
            if created:
                self.stdout.write("Created superuser admin (admin@admin.com / admin123)")
            else:
                self.stdout.write("Superuser admin already exists, synced credentials")

            # 2. Create Faculties
            engineering, _ = Faculty.objects.get_or_create(
                slug="engineering",
                defaults={
                    "name_ar": "كلية الهندسة",
                    "name_en": "Faculty of Engineering",
                    "description_ar": "تقدم برامج متميزة في الهندسة المدنية والمعمارية وهندسة الحاسوب والاتصالات",
                    "description_en": "Offers distinguished programs in Civil Engineering, Architecture, and Computer & Communications Engineering",
                    "icon": "Building2",
                    "color": "bg-blue-500",
                    "image": "/images/faculties/engineering.png",
                }
            )
            business, _ = Faculty.objects.get_or_create(
                slug="business",
                defaults={
                    "name_ar": "كلية إدارة الأعمال",
                    "name_en": "Faculty of Business Administration",
                    "description_ar": "تهدف إلى إعداد قادة أعمال متميزين في مجالات المحاسبة والتسويق والإدارة",
                    "description_en": "Aims to prepare business leaders in Accounting, Marketing, and Management fields",
                    "icon": "Briefcase",
                    "color": "bg-emerald-500",
                    "image": "/images/faculties/business.png",
                }
            )
            dentistry, _ = Faculty.objects.get_or_create(
                slug="dentistry",
                defaults={
                    "name_ar": "كلية طب الأسنان",
                    "name_en": "Faculty of Dentistry",
                    "description_ar": "توفير تعليم وتدريب سريري عالي الجودة في مجال صحة الفم والأسنان",
                    "description_en": "Providing high-quality clinical training and education in oral health",
                    "icon": "Activity",
                    "color": "bg-purple-500",
                    "image": "/images/faculties/dentistry.png",
                }
            )
            pharmacy, _ = Faculty.objects.get_or_create(
                slug="pharmacy",
                defaults={
                    "name_ar": "كلية الصيدلة",
                    "name_en": "Faculty of Pharmacy",
                    "description_ar": "تركز على العلوم الصيدلانية وصناعة الأدوية والرعاية الصيدلانية المتميزة",
                    "description_en": "Focuses on pharmaceutical sciences, drug design, and patient care",
                    "icon": "Heart",
                    "color": "bg-rose-500",
                    "image": "/images/faculties/pharmacy.png",
                }
            )
            self.stdout.write("Faculties seeded.")

            # 3. Create Programs
            civil, _ = Program.objects.get_or_create(
                slug="civil",
                defaults={
                    "faculty": engineering,
                    "name_ar": "الهندسة المدنية",
                    "name_en": "Civil Engineering",
                    "description_ar": "برنامج شامل في تصميم وبناء البنية التحتية والمنشآت",
                    "description_en": "Comprehensive program in infrastructure design and construction",
                    "credit_hours": 168,
                    "min_score_percent": 70,
                    "min_score_points": 1680,
                    "tuition_syrian": 350000,
                    "tuition_non_resident": 100,
                    "branch": "scientific",
                    "duration": 5,
                }
            )
            arch, _ = Program.objects.get_or_create(
                slug="architecture",
                defaults={
                    "faculty": engineering,
                    "name_ar": "الهندسة المعمارية",
                    "name_en": "Architecture",
                    "description_ar": "برنامج يدمج بين الفن والتكنولوجيا لتصميم الفراغات والمنشآت الحديثة",
                    "description_en": "Integrates art and technology to design modern spaces and buildings",
                    "credit_hours": 175,
                    "min_score_percent": 75,
                    "min_score_points": 1800,
                    "tuition_syrian": 400000,
                    "tuition_non_resident": 120,
                    "branch": "scientific",
                    "duration": 5,
                }
            )
            cce, _ = Program.objects.get_or_create(
                slug="computer-communications",
                defaults={
                    "faculty": engineering,
                    "name_ar": "هندسة الحاسوب والاتصالات",
                    "name_en": "Computer and Communications Engineering",
                    "description_ar": "تخصص متقدم يغطي شبكات الاتصالات وأنظمة الحاسب والبرمجيات",
                    "description_en": "Advanced discipline covering networking, hardware, and software systems",
                    "credit_hours": 165,
                    "min_score_percent": 72,
                    "min_score_points": 1720,
                    "tuition_syrian": 380000,
                    "tuition_non_resident": 110,
                    "branch": "scientific",
                    "duration": 5,
                }
            )
            accounting, _ = Program.objects.get_or_create(
                slug="accounting",
                defaults={
                    "faculty": business,
                    "name_ar": "المحاسبة",
                    "name_en": "Accounting",
                    "description_ar": "دراسة المعايير والممارسات المالية والتحليل المحاسبي للشركات",
                    "description_en": "Study of financial standards, reporting, and company auditing",
                    "credit_hours": 132,
                    "min_score_percent": 60,
                    "min_score_points": 1400,
                    "tuition_syrian": 200000,
                    "tuition_non_resident": 70,
                    "branch": "both",
                    "duration": 4,
                }
            )
            marketing, _ = Program.objects.get_or_create(
                slug="marketing",
                defaults={
                    "faculty": business,
                    "name_ar": "التسويق",
                    "name_en": "Marketing",
                    "description_ar": "فهم سلوك المستهلك وإدارة الحملات واستراتيجيات الترويج الرقمية",
                    "description_en": "Understanding consumer behavior and managing promotional campaigns",
                    "credit_hours": 132,
                    "min_score_percent": 60,
                    "min_score_points": 1400,
                    "tuition_syrian": 200000,
                    "tuition_non_resident": 70,
                    "branch": "both",
                    "duration": 4,
                }
            )
            dentistry_prog, _ = Program.objects.get_or_create(
                slug="dentistry-program",
                defaults={
                    "faculty": dentistry,
                    "name_ar": "طب الأسنان",
                    "name_en": "Dentistry",
                    "description_ar": "دراسة طب وجراحة الفم والوجه والفكين والتدريب السريري المتطور",
                    "description_en": "Study of oral and maxillofacial medicine and advanced clinical training",
                    "credit_hours": 180,
                    "min_score_percent": 85,
                    "min_score_points": 2100,
                    "tuition_syrian": 650000,
                    "tuition_non_resident": 250,
                    "branch": "scientific",
                    "duration": 5,
                }
            )
            pharmacy_prog, _ = Program.objects.get_or_create(
                slug="pharmacy-program",
                defaults={
                    "faculty": pharmacy,
                    "name_ar": "الصيدلة",
                    "name_en": "Pharmacy",
                    "description_ar": "دراسة الكيمياء الدوائية وتصميم الأدوية والرعاية الصيدلانية الإكلينيكية",
                    "description_en": "Study of medicinal chemistry, drug formulation, and clinical pharmacy",
                    "credit_hours": 170,
                    "min_score_percent": 80,
                    "min_score_points": 1950,
                    "tuition_syrian": 550000,
                    "tuition_non_resident": 200,
                    "branch": "scientific",
                    "duration": 5,
                }
            )
            self.stdout.write("Programs seeded.")

            # 4. Create Courses
            c1, _ = Course.objects.get_or_create(code="MATH101", defaults={"name_ar": "الرياضيات 1", "name_en": "Mathematics I", "credits": 3})
            c2, _ = Course.objects.get_or_create(code="PHYS101", defaults={"name_ar": "الفيزياء العامة", "name_en": "General Physics", "credits": 3})
            c3, _ = Course.objects.get_or_create(code="COMP101", defaults={"name_ar": "مقدمة في البرمجة", "name_en": "Introduction to Programming", "credits": 4})
            c4, _ = Course.objects.get_or_create(code="CIV101", defaults={"name_ar": "الميكانيك الهندسي", "name_en": "Engineering Mechanics", "credits": 3})
            c5, _ = Course.objects.get_or_create(code="ARCH101", defaults={"name_ar": "الرسم المعماري", "name_en": "Architectural Drawing", "credits": 4})
            self.stdout.write("Courses seeded.")

            # 5. Create Student Profile for Admin (to view portal details)
            student, created = Student.objects.get_or_create(
                student_id="202210452",
                defaults={
                    "user": admin_user,
                    "name_ar": "أحمد المحمد",
                    "name_en": "Ahmad Al-Mohammad",
                    "email": "admin@admin.com",
                    "faculty": engineering,
                    "program": cce,
                    "year": 3,
                    "gpa": 3.75,
                    "total_credits": 165,
                    "completed_credits": 98,
                    "is_top": True,
                    "rank": 1,
                }
            )
            if created:
                self.stdout.write("Created student profile for admin@admin.com")
                
                # Create Schedule items for this student
                ScheduleItem.objects.get_or_create(
                    student=student,
                    course=c1,
                    day="sunday",
                    defaults={
                        "day_ar": "الأحد",
                        "day_en": "Sunday",
                        "time": "08:00 - 09:30",
                        "room": "القاعة 102",
                        "instructor": "د. علي منصور",
                        "instructor_en": "Dr. Ali Mansour",
                    }
                )
                ScheduleItem.objects.get_or_create(
                    student=student,
                    course=c3,
                    day="monday",
                    defaults={
                        "day_ar": "الإثنين",
                        "day_en": "Monday",
                        "time": "10:00 - 12:00",
                        "room": "مخبر الحاسوب 2",
                        "instructor": "د. ريم الخالد",
                        "instructor_en": "Dr. Reem Al-Khaled",
                    }
                )
                ScheduleItem.objects.get_or_create(
                    student=student,
                    course=c2,
                    day="tuesday",
                    defaults={
                        "day_ar": "الثلاثاء",
                        "day_en": "Tuesday",
                        "time": "12:30 - 14:00",
                        "room": "مدرج الفيزياء",
                        "instructor": "د. سامر العلي",
                        "instructor_en": "Dr. Samer Al-Ali",
                    }
                )

                # Create Grades for this student
                StudentGrade.objects.get_or_create(student=student, course=c1, defaults={"grade": "A", "points": 4.00})
                StudentGrade.objects.get_or_create(student=student, course=c2, defaults={"grade": "B+", "points": 3.50})
                StudentGrade.objects.get_or_create(student=student, course=c3, defaults={"grade": "A-", "points": 3.75})
            else:
                self.stdout.write("Student profile already exists")

            # 6. Faculty Members
            # Empty by request so user can add and manage faculty members from scratch.
            self.stdout.write("Faculty members section skipped (database is clean for manual entry).")



            # 7. Alumni Stories
            AlumniStory.objects.get_or_create(
                name_en="Yaser Al-Ahmed",
                defaults={
                    "faculty": engineering,
                    "name_ar": "ياسر الأحمد",
                    "graduation_year": 2021,
                    "program_ar": "هندسة الحاسوب",
                    "program_en": "Computer Engineering",
                    "current_role_ar": "مهندس برمجيات أول",
                    "current_role_en": "Senior Software Engineer",
                    "company_ar": "شركة جوجل العالمية",
                    "company_en": "Google Inc.",
                    "story_ar": "بدأت رحلتي في جامعة أنطاكية السورية حيث تعلمت الأساسيات الصلبة للهندسة وتلقيت الدعم الدائم من الأساتذة الكرام للمشاركة في المسابقات البرمجية.",
                    "story_en": "My journey started at ASU where I learned solid foundations of engineering and received constant encouragement from professors to participate in programming contests.",
                    "image": "/images/alumni/alumni_1.png",
                }
            )
            self.stdout.write("Alumni stories seeded.")

            # 8. News Articles
            NewsArticle.objects.get_or_create(
                slug="registration-steps-2025-2026",
                defaults={
                    "title_ar": "خطوات التسجيل للمقبولين وفق مفاضلات الفصل الأول 2025-2026",
                    "title_en": "Registration Steps for Admitted Students Fall 2025-2026",
                    "excerpt_ar": "دليل شامل لطلابنا المقبولين حول إجراءات التسجيل للفصل الدراسي الأول",
                    "excerpt_en": "Comprehensive guide for admitted students on registration procedures for the first semester",
                    "content_ar": "أعلنت جامعة أنطاكية السورية عن خطوات التسجيل للطلاب المقبولين وفق مفاضلات الفصل الأول للعام الدراسي 2025-2026. تتضمن الخطوات مراجعة شؤون الطلاب واستكمال الأوراق المطلوبة ودفع الرسوم المقررة.",
                    "content_en": "Antioch Syrian University announced the registration steps for students admitted according to the first semester competitions for the academic year 2025-2026. Steps include visiting student affairs, completing documents, and payment.",
                    "image": "/images/news/registration.png",
                    "category": "announcement",
                    "date": datetime.date(2025, 11, 18),
                    "featured": True,
                }
            )
            NewsArticle.objects.get_or_create(
                slug="required-documents-2025-2026",
                defaults={
                    "title_ar": "الوثائق المطلوبة للتسجيل في الجامعة 2025-2026",
                    "title_en": "Required Documents for University Registration 2025-2026",
                    "excerpt_ar": "قائمة الأوراق والوثائق الرسمية المطلوبة لإتمام عملية التسجيل الجامعي",
                    "excerpt_en": "List of official papers and documents required to complete the university registration process",
                    "content_ar": "حددت الجامعة الوثائق المطلوبة للتسجيل للعام الدراسي 2025-2026، بما في ذلك الشهادات الثانوية الأصلية المصدقة، وصور الهوية الشخصية، والشهادة الصحية، والصور الشخصية الحديثة.",
                    "content_en": "The university specified the documents required for registration for the academic year 2025-2026, including certified original secondary school certificates, ID card copies, medical certificate, and recent personal photos.",
                    "image": "/images/news/docs.png",
                    "category": "announcement",
                    "date": datetime.date(2025, 11, 18),
                    "featured": True,
                }
            )
            self.stdout.write("News articles seeded.")

            # 9. Events
            Event.objects.get_or_create(
                title_en="IT and Cybersecurity Forum 2026",
                defaults={
                    "title_ar": "منتدى تقنية المعلومات والأمن السيبراني 2026",
                    "description_ar": "منتدى تقني يجمع خبراء الشبكات والأمن الرقمي في جامعة أنطاكية لمناقشة التوجهات والحلول الحديثة لحماية البيانات والأنظمة.",
                    "description_en": "A tech forum bringing together network and cybersecurity experts at ASU to discuss modern trends and solutions in data protection.",
                    "date": datetime.date(2026, 4, 15),
                    "time": "10:00 AM - 02:00 PM",
                    "location_ar": "المسرح الرئيسي بالجامعة",
                    "location_en": "University Main Theater",
                    "type": "academic",
                }
            )
            self.stdout.write("Events seeded.")

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
