import os
import sys
import django
from datetime import date

# Set UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from university.models import (
    Faculty,
    Program,
    FacultyMember,
    Student,
    AlumniStory,
    NewsArticle,
    Course,
    UserProfile,
)

User = get_user_model()
DEFAULT_PASSWORD = "Password123!"

print("Starting ASU department, users, and content seeding...")

# 1. Ensure Faculty of Informatics (ce) exists
faculty_ce, created = Faculty.objects.get_or_create(
    slug="ce",
    defaults={
        "name_ar": "كلية الهندسة المعلوماتية",
        "name_en": "Faculty of Informatics Engineering",
        "description_ar": "صرح أكاديمي رائد في علوم الحاسوب وهندسة البرمجيات والذكاء الاصطناعي.",
        "description_en": "A premier academic institution in computer science, software engineering, and AI.",
        "icon": "Cpu",
        "color": "bg-emerald-600",
        "primary_color": "#059669",
        "accent_color": "#10B981",
        "established_year": 2018,
        "students_count": 850,
        "labs_count": 8,
        "research_papers_count": 120,
        "employment_rate": 95,
        "motto_ar": "نبتكر اليوم لنبني المستقبل الرقمي",
        "motto_en": "Innovating Today to Build the Digital Future",
    }
)
if not created:
    faculty_ce.name_ar = "كلية الهندسة المعلوماتية"
    faculty_ce.name_en = "Faculty of Informatics Engineering"
    faculty_ce.primary_color = "#059669"
    faculty_ce.accent_color = "#10B981"
    faculty_ce.save()
print(f"Faculty: {faculty_ce.name_ar} (id={faculty_ce.id})")

# 2. Ensure Software Engineering Program exists & update its details
program_se, created = Program.objects.get_or_create(
    slug="software-engineering",
    defaults={
        "faculty": faculty_ce,
        "name_ar": "قسم هندسة البرمجيات",
        "name_en": "Software Engineering Department",
        "description_ar": "برنامج رائد يهدف إلى إعداد مهندسي برمجيات محترفين في تصميم وتطوير النظم البرمجية السحابية والذكية.",
        "description_en": "A premier program aimed at preparing software engineering professionals in cloud, intelligent, and distributed systems.",
        "credit_hours": 160,
        "min_score_percent": 60,
        "min_score_points": 144,
        "tuition_syrian": 2500000,
        "tuition_non_resident": 1800,
        "duration": 5,
        "branch": "scientific",
        "primary_color": "#15803d",
        "accent_color": "#16a34a",
        "established_year": 2018,
        "students_count": 380,
        "labs_count": 4,
        "research_papers_count": 85,
        "employment_rate": 94,
    }
)

# Update layout_config and key fields
program_se.layout_config = {
    "headerStyle": "hero_split",
    "showQuickStats": True,
    "showDeanMessage": True,
    "showCurriculum": True,
    "showCareerPaths": True,
    "showFacilities": True,
    "showStaff": True,
    "showTopStudents": True,
    "showAlumniStories": True,
    "sectionsOrder": [
        "stats",
        "head",
        "curriculum",
        "career_paths",
        "facilities",
        "staff",
        "top_students",
        "alumni_stories",
    ],
    "sectionsConfig": {
        "stats": {"titleAr": "أرقام وإحصائيات القسم", "titleEn": "Department Key Numbers & Metrics"},
        "head": {"titleAr": "كلمة رئيس القسم", "titleEn": "Head of Department Message", "layoutVariant": "split"},
        "curriculum": {"titleAr": "الخطة الدراسية وتوزيع المقررات", "titleEn": "Curriculum & Study Plan"},
        "career_paths": {"titleAr": "الفرص والآفاق المهنية للخريجين", "titleEn": "Career Paths & Opportunities"},
        "facilities": {"titleAr": "المختبرات والمشاغل التخصصية", "titleEn": "Specialized Labs & Facilities"},
        "staff": {"titleAr": "دليل أساتذة وكادر القسم الأكاديمي", "titleEn": "Department Academic Staff", "itemLimit": 8},
        "top_students": {"titleAr": "لوحة الشرف وأوائل القسم", "titleEn": "Department Honor Roll"},
        "alumni_stories": {"titleAr": "قصص نجاح خريجي القسم", "titleEn": "Alumni Success Stories"},
    }
}

program_se.facilities = [
    {
        "nameAr": "مختبر البرمجيات والأنظمة المدمجة",
        "nameEn": "Software & Embedded Systems Lab",
        "descriptionAr": "مجهز بأحدث محطات العمل وشاشات التطوير السحابية وأنظمة الاختبار المؤتمتة وبيئات التطوير المتكاملة.",
    },
    {
        "nameAr": "مخبر الذكاء الاصطناعي والحوسبة المتقدمة",
        "nameEn": "AI & High Performance Computing Lab",
        "descriptionAr": "وحدات معالجة رسومية عالية الأداء GPU ومخدمات مخصصة لتدريب نماذج الذكاء الاصطناعي والتعلم العميق.",
    },
    {
        "nameAr": "مختبر الشبكات والأمن السيبراني",
        "nameEn": "Networks & Cybersecurity Workstation",
        "descriptionAr": "تجهيزات شبكية وسيرفرات محاكاة لاختبار الاختراق وتأمين البرمجيات والبنى التحتية الحيوية.",
    },
    {
        "nameAr": "استوديو تصميم واجهات وتجربة المستخدم (UI/UX Studio)",
        "nameEn": "UI/UX & Interactive Design Studio",
        "descriptionAr": "مختبر مخصص للبحث في قابلية الاستخدام وتصميم النماذج التفاعلية لتطبيقات الويب والهواتف الذكية.",
    }
]

program_se.career_paths = "\n".join([
    "تطوير البرمجيات والأنظمة السحابية المتقدمة",
    "هندسة الذكاء الاصطناعي ونظم تعلم الآلة",
    "إدارة وتصميم قواعد البيانات الضخمة",
    "أمن الشبكات والمعلومات والأمن السيبراني",
    "إدارة المشاريع التكنولوجية والتحول الرقمي",
    "البحث العلمي والتطوير الأكاديمي والصناعي",
])

program_se.head_name_ar = "أ.د. سامر الحلبي"
program_se.head_name_en = "Prof. Dr. Samer Al-Halabi"
program_se.head_photo = "/images/faculty/prof_male_1.png"
program_se.head_message_ar = "أهلاً بكم في قسم هندسة البرمجيات بجامعة أنطاكية السورية. نعمل بجهد متواصل لتمكين طلبتنا من أحدث المعارف النظرية والتطبيقية، وربطهم بسوق العمل عبر مشاريع واقعية وبنية مخبرية رائدة تضمن تفوقهم وتخرجهم على أعلى درجات الكفاءة."
program_se.head_message_en = "Welcome to the Department of Software Engineering at Antioch Syrian University. We are dedicated to providing our students with cutting-edge academic curricula and hands-on skills, preparing them to lead in the rapidly evolving tech market."
program_se.motto_ar = "رواد هندسة البرمجيات والذكاء الاصطناعي"
program_se.motto_en = "Pioneers in Software Engineering & Artificial Intelligence"
program_se.save()
print(f"Program: {program_se.name_ar} (id={program_se.id}) updated.")


# Helper to get or create User
def create_or_update_user(email, password, role, name_ar, name_en, avatar, phone="", assigned_faculty=None, bio=""):
    user = User.objects.filter(email=email).first()
    if not user:
        user = User.objects.create_user(
            email=email,
            password=password,
            username=email,
            name_ar=name_ar,
            name_en=name_en,
            role=role,
            avatar=avatar,
            phone=phone,
            assigned_faculty=assigned_faculty,
            bio=bio,
        )
        print(f"Created user: {email} ({role})")
    else:
        user.name_ar = name_ar
        user.name_en = name_en
        user.role = role
        user.avatar = avatar
        user.phone = phone
        user.bio = bio
        if assigned_faculty:
            user.assigned_faculty = assigned_faculty
        user.set_password(password)
        user.save()
        print(f"Updated user: {email} ({role})")
    return user


# 3. Create Content Managers
print("\n--- Seeding Content Managers ---")
cm_ce = create_or_update_user(
    email="content.ce@asu.edu.sy",
    password=DEFAULT_PASSWORD,
    role="content_manager",
    name_ar="م. علاء الدين الأحمد",
    name_en="Eng. Alaa El-Din Al-Ahmad",
    avatar="/images/faculty/prof_male_4.png",
    phone="+963 944 778899",
    assigned_faculty=faculty_ce,
    bio="مسؤول إدارة ونشر المحتوى الأكاديمي والإخباري لكلية الهندسة المعلوماتية وأقسامها."
)

cm_gen = create_or_update_user(
    email="content.general@asu.edu.sy",
    password=DEFAULT_PASSWORD,
    role="content_manager",
    name_ar="أ. مروة العطار",
    name_en="Ms. Marwa Al-Attar",
    avatar="/images/faculty/prof_female_3.png",
    phone="+963 933 114477",
    assigned_faculty=None,
    bio="مديرة المحتوى الإعلامي المركزي وبوابة الأخبار الرسمية في جامعة أنطاكية السورية."
)


# 4. Create Faculty Members (Teachers)
print("\n--- Seeding Teachers & Faculty Members ---")

teachers_data = [
    {
        "email": "samer.halabi@asu.edu.sy",
        "name_ar": "أ.د. سامر الحلبي",
        "name_en": "Prof. Dr. Samer Al-Halabi",
        "title_ar": "أستاذ دكتور - رئيس قسم هندسة البرمجيات",
        "title_en": "Professor & Head of Software Engineering Department",
        "image": "/images/faculty/prof_male_1.png",
        "is_head": True,
        "phone": "+963 944 551122",
        "office_hours": "الأحد والثلاثاء: 10:00 - 13:00",
        "location_ar": "مبنى كلية الهندسة المعلوماتية - الطابق الثالث - مكتب 304",
        "location_en": "Faculty of Informatics - 3rd Floor - Office 304",
        "bio_ar": "دكتوراه في هندسة البرمجيات والأنظمة الموزعة من جامعة برلين التقنية. باحث ومستشار في معمارية النظم السحابية وهندسة البيانات الضخمة لأكثر من 15 عاماً.",
        "bio_en": "Ph.D. in Software Engineering & Distributed Systems from TU Berlin. Consultant and researcher in cloud architecture and enterprise data systems.",
        "education_ar": [
            "دكتوراه في هندسة البرمجيات - جامعة برلين التقنية (2012)",
            "ماجستير في هندسة نظم المعلومات - جامعة دمشق (2007)",
            "إجازة في الهندسة المعلوماتية - جامعة دمشق (2004)",
        ],
        "education_en": [
            "Ph.D. in Software Engineering - TU Berlin (2012)",
            "M.Sc. in Information Systems - Damascus University (2007)",
            "B.Sc. in Informatics Engineering - Damascus University (2004)",
        ],
        "research_ar": "معمارية النظم السحابية، أطر العمل الموزعة، أتمتة اختبار البرمجيات.",
        "research_en": "Cloud Architecture, Distributed Frameworks, Automated Software Testing.",
        "publications": [
            "Architectural Patterns for Cloud-Native Distributed Systems (IEEE 2023)",
            "Automated Microservices Orchestration and Fault Tolerance (ACM 2021)",
        ],
    },
    {
        "email": "reem.ali@asu.edu.sy",
        "name_ar": "د. ريم العلي",
        "name_en": "Dr. Reem Al-Ali",
        "title_ar": "أستاذ مشارك في الحوسبة السحابية وهندسة النظم",
        "title_en": "Associate Professor in Cloud Computing & Systems",
        "image": "/images/faculty/prof_female_1.png",
        "is_head": False,
        "phone": "+963 944 332211",
        "office_hours": "الإثنين والأربعاء: 11:00 - 13:00",
        "location_ar": "مبنى كلية الهندسة المعلوماتية - مكتب 308",
        "location_en": "Faculty of Informatics - Office 308",
        "bio_ar": "دكتوراه في الحوسبة السحابية وهندسة البرمجيات، خبيرة معتمدة في البنى التحتية السحابية وتطوير الحلول البرمجية عالية التوافر.",
        "bio_en": "Ph.D. in Cloud Computing and Software Engineering. Expert in high-availability software architectures and cloud native solutions.",
        "education_ar": [
            "دكتوراه في الحوسبة السحابية - جامعة غرونوبل بفرنسا (2015)",
            "إجازة في الهندسة المعلوماتية - جامعة حلب (2009)",
        ],
        "education_en": [
            "Ph.D. in Cloud Computing - University of Grenoble (2015)",
            "B.Sc. in Informatics Engineering - University of Aleppo (2009)",
        ],
        "research_ar": "الحوسبة الموزعة، الحوسبة بدون خادم (Serverless)، وهندسة الخدمات الميكروية.",
        "research_en": "Distributed Computing, Serverless Architectures, Microservices Engineering.",
        "publications": [
            "Scalability Metrics in Containerized Microservices (2022)",
            "Serverless Paradigms for Event-Driven Backends (2020)",
        ],
    },
    {
        "email": "omar.kurdi@asu.edu.sy",
        "name_ar": "د. عمر الكردي",
        "name_en": "Dr. Omar Al-Kurdi",
        "title_ar": "أستاذ مساعد في الأمن السيبراني وحماية البرمجيات",
        "title_en": "Assistant Professor in Cybersecurity & Secure Coding",
        "image": "/images/faculty/prof_male_2.png",
        "is_head": False,
        "phone": "+963 933 665544",
        "office_hours": "الأحد والخميس: 09:30 - 11:30",
        "location_ar": "مبنى كلية الهندسة المعلوماتية - مكتب 310",
        "location_en": "Faculty of Informatics - Office 310",
        "bio_ar": "دكتوراه في أمن المعلومات واختبار الاختراق وتطوير البرمجيات الآمنة (DevSecOps)، مستشار أمني لعدة جهات حكومية وخاصة.",
        "bio_en": "Ph.D. in Information Security and Secure Software Development (DevSecOps). Cybersecurity advisor for enterprise solutions.",
        "education_ar": [
            "دكتوراه في أمن المعلومات - جامعة مانشستر (2017)",
            "إجازة في الهندسة المعلوماتية - جامعة دمشق (2011)",
        ],
        "education_en": [
            "Ph.D. in Information Security - University of Manchester (2017)",
            "B.Sc. in Informatics Engineering - Damascus University (2011)",
        ],
        "research_ar": "الأمن السيبراني التطبيقي، التشفير الحديث، وتحليل الثغرات البرمجية في زمن التشغيل.",
        "research_en": "Applied Cybersecurity, Modern Cryptography, Runtime Vulnerability Analysis.",
        "publications": [
            "Automated Static Analysis for Zero-Day Vulnerability Detection (2023)",
        ],
    },
    {
        "email": "maya.najjar@asu.edu.sy",
        "name_ar": "د. مايا النجار",
        "name_en": "Dr. Maya Al-Najjar",
        "title_ar": "مدرس دكتور في الذكاء الاصطناعي وتعلم الآلة",
        "title_en": "Lecturer in Artificial Intelligence & Machine Learning",
        "image": "/images/faculty/prof_female_2.png",
        "is_head": False,
        "phone": "+963 955 889900",
        "office_hours": "الثلاثاء والأربعاء: 12:00 - 14:00",
        "location_ar": "مبنى كلية الهندسة المعلوماتية - مخبر الذكاء الاصطناعي",
        "location_en": "Faculty of Informatics - AI Lab",
        "bio_ar": "متخصصة في نماذج معالجة اللغات الطبيعية ورؤية الحاسوب وتطبيقاتها في هندسة البرمجيات الذكية.",
        "bio_en": "Specialized in Natural Language Processing, Computer Vision, and intelligent software engineering.",
        "education_ar": [
            "دكتوراه في الذكاء الاصطناعي - جامعة دمشق (2020)",
            "ماجستير في بحوث العمليات والذكاء الصنعي (2016)",
        ],
        "education_en": [
            "Ph.D. in Artificial Intelligence - Damascus University (2020)",
            "M.Sc. in Artificial Intelligence (2016)",
        ],
        "research_ar": "نماذج اللغات التوليدية، التعلم العميق، والأتمتة الذكية للكود.",
        "research_en": "Generative Language Models, Deep Learning, Intelligent Code Automation.",
        "publications": [
            "Deep Learning Techniques in Arabic Code Generation (2022)",
        ],
    },
    {
        "email": "hossam.sherif@asu.edu.sy",
        "name_ar": "د. حسام الدين شريف",
        "name_en": "Dr. Hossam Eldin Sherif",
        "title_ar": "أستاذ مشارك في قواعد البيانات وهندسة البيانات الضخمة",
        "title_en": "Associate Professor in Database Engineering & Big Data",
        "image": "/images/faculty/prof_male_3.png",
        "is_head": False,
        "phone": "+963 988 123456",
        "office_hours": "الإثنين والخميس: 10:00 - 12:00",
        "location_ar": "مبنى كلية الهندسة المعلوماتية - مكتب 306",
        "location_en": "Faculty of Informatics - Office 306",
        "bio_ar": "خبير معتمد في معمارية قواعد البيانات العلائقية وغير العلائقية (NoSQL) وهندسة خطوط معالجة البيانات الضخمة.",
        "bio_en": "Certified architect in Relational/NoSQL databases and scalable big data pipelines.",
        "education_ar": ["دكتوراه في قواعد البيانات - جامعة القاهرة (2014)"],
        "education_en": ["Ph.D. in Database Systems - Cairo University (2014)"],
        "research_ar": "قواعد البيانات الموزعة، الفهرسة المتقدمة، وهندسة تدفق البيانات.",
        "research_en": "Distributed Databases, Advanced Indexing, Stream Data Engineering.",
        "publications": ["High-Throughput Stream Processing for IoT Architectures (2021)"],
    },
    {
        "email": "nour.sleiman@asu.edu.sy",
        "name_ar": "د. نور الهدى سليمان",
        "name_en": "Dr. Nour Al-Huda Sleiman",
        "title_ar": "مدرس دكتور في تطوير برمجيات الويب وتجربة المستخدم",
        "title_en": "Lecturer in Web Engineering & UI/UX Design",
        "image": "/images/faculty/prof_female_3.png",
        "is_head": False,
        "phone": "+963 944 654321",
        "office_hours": "الأحد والثلاثاء: 12:30 - 14:30",
        "location_ar": "مبنى كلية الهندسة المعلوماتية - مكتب 312",
        "location_en": "Faculty of Informatics - Office 312",
        "bio_ar": "دكتوراه في هندسة نظم الويب والتفاعل بين الإنسان والحاسوب، مهتمة بتصميم التجارب الرقمية الذكية والتطبيقات فائقة السرعة.",
        "bio_en": "Ph.D. in Web Systems Engineering and Human-Computer Interaction, passionate about high-performance modern web platforms.",
        "education_ar": ["دكتوراه في هندسة الويب - جامعة دمشق (2021)"],
        "education_en": ["Ph.D. in Web Engineering - Damascus University (2021)"],
        "research_ar": "أطر عمل الويب التفاعلية، إمكانية الوصول، وأنظمة التصميم المعيارية.",
        "research_en": "Interactive Web Frameworks, Web Accessibility, Design Systems.",
        "publications": ["Design System Consistency and Component-Driven Architectures (2022)"],
    },
    {
        "email": "tareq.sabbagh@asu.edu.sy",
        "name_ar": "م. طارق الصباغ",
        "name_en": "Eng. Tareq Al-Sabbagh",
        "title_ar": "مشرف مخابر ومحاضر في البرمجة المتقدمة",
        "title_en": "Lab Supervisor & Advanced Programming Instructor",
        "image": "/images/faculty/prof_male_4.png",
        "is_head": False,
        "phone": "+963 933 998877",
        "office_hours": "يومياً من 09:00 إلى 15:00",
        "location_ar": "مبنى كلية الهندسة المعلوماتية - مختبر البرمجيات والأنظمة المدمجة",
        "location_en": "Faculty of Informatics - Software & Embedded Systems Lab",
        "bio_ar": "ماجستير في هندسة البرمجيات، مشرف ومسؤول عن التجارب المخبرية والتطبيقية في القسم وتدريب الفرق البرمجية المشاركة في المسابقات.",
        "bio_en": "M.Sc. in Software Engineering, lead lab supervisor and head coach for university competitive programming teams.",
        "education_ar": ["ماجستير هندسة البرمجيات - جامعة دمشق (2020)"],
        "education_en": ["M.Sc. Software Engineering - Damascus University (2020)"],
        "research_ar": "البرمجة التنافسية، هندسة النظم المضمنة، وتطوير الأنظمة المؤتمتة.",
        "research_en": "Competitive Programming, Embedded Systems, Automated Build Systems.",
        "publications": [],
    },
    {
        "email": "firas.jarrah@asu.edu.sy",
        "name_ar": "م. فراس الجراح",
        "name_en": "Eng. Firas Al-Jarrah",
        "title_ar": "مشرف مشاريع التخرج وهندسة البرمجيات التطبيقية",
        "title_en": "Graduation Projects Coordinator & Instructor",
        "image": "/images/faculty/prof_male_5.png",
        "is_head": False,
        "phone": "+963 944 887766",
        "office_hours": "الإثنين والأربعاء: 10:00 - 14:00",
        "location_ar": "مبنى كلية الهندسة المعلوماتية - مكتب 314",
        "location_en": "Faculty of Informatics - Office 314",
        "bio_ar": "مهندس استشاري ومحاضر، منسق لجنة مشاريع التخرج بالقسم وحلقة الوصل مع شركات البرمجيات وحاضنات الأعمال.",
        "bio_en": "Consultant engineer and lecturer, coordinator of capstone graduation projects and liaison with tech incubators.",
        "education_ar": ["ماجستير في إدارة المشاريع الهندسية ونظم المعلومات (2019)"],
        "education_en": ["M.Sc. in Engineering Project Management & IS (2019)"],
        "research_ar": "إدارة مشاريع أجايل، تكامل CI/CD، ومنهجيات التخرج الريادية.",
        "research_en": "Agile Project Management, CI/CD Integration, Tech Entrepreneurship.",
        "publications": [],
    },
]

head_member_instance = None
for t in teachers_data:
    u = create_or_update_user(
        email=t["email"],
        password=DEFAULT_PASSWORD,
        role="faculty",
        name_ar=t["name_ar"],
        name_en=t["name_en"],
        avatar=t["image"],
        phone=t["phone"],
        assigned_faculty=faculty_ce,
        bio=t["bio_ar"],
    )

    member, _ = FacultyMember.objects.update_or_create(
        email=t["email"],
        defaults={
            "user": u,
            "faculty": faculty_ce,
            "department": program_se,
            "name_ar": t["name_ar"],
            "name_en": t["name_en"],
            "title_ar": t["title_ar"],
            "title_en": t["title_en"],
            "department_ar": program_se.name_ar,
            "department_en": program_se.name_en,
            "description_ar": t["bio_ar"],
            "description_en": t["bio_en"],
            "office_hours": t["office_hours"],
            "location_ar": t["location_ar"],
            "location_en": t["location_en"],
            "image": t["image"],
            "is_head": t["is_head"],
            "bio_ar": t["bio_ar"],
            "bio_en": t["bio_en"],
            "education_ar": t["education_ar"],
            "education_en": t["education_en"],
            "research_ar": t["research_ar"],
            "research_en": t["research_en"],
            "publications": t["publications"],
        }
    )
    if t["is_head"]:
        head_member_instance = member
    print(f"FacultyMember: {member.name_ar} (Dept: {member.department_ar})")

if head_member_instance:
    program_se.head = head_member_instance
    program_se.save()
    print("Linked Head of Department to Program.")


# 5. Create Students & Top Students (Honor Roll)
print("\n--- Seeding Students & Top Honor Roll ---")

students_data = [
    {
        "student_id": "202110412",
        "email": "kinan.khaled@asu.edu.sy",
        "name_ar": "محمد كنان الخالد",
        "name_en": "Mohammad Kinan Al-Khaled",
        "avatar": "/images/students/student_male_1.png",
        "year": 4,
        "gpa": 3.98,
        "total_credits": 160,
        "completed_credits": 132,
        "is_top": True,
        "rank": 1,
        "phone": "+963 944 112244",
        "bio": "طالب سنة رابعة في هندسة البرمجيات، الأول على القسم، شغوف بهندسة النظم السحابية وتعلم الآلة.",
    },
    {
        "student_id": "202110255",
        "email": "sarah.yaziji@asu.edu.sy",
        "name_ar": "سارة أحمد اليازجي",
        "name_en": "Sarah Ahmad Al-Yaziji",
        "avatar": "/images/students/student_female_1.png",
        "year": 4,
        "gpa": 3.94,
        "total_credits": 160,
        "completed_credits": 130,
        "is_top": True,
        "rank": 2,
        "phone": "+963 933 223355",
        "bio": "طالبة متميزة في السنة الرابعة، قائدة فريق البرمجة التنافسية، متخصصة في أمن البرمجيات وتحليل البيانات.",
    },
    {
        "student_id": "202210089",
        "email": "ziad.ayoubi@asu.edu.sy",
        "name_ar": "زياد محمود الأيوبي",
        "name_en": "Ziad Mahmoud Al-Ayoubi",
        "avatar": "/images/students/student_male_2.png",
        "year": 3,
        "gpa": 3.91,
        "total_credits": 160,
        "completed_credits": 98,
        "is_top": True,
        "rank": 3,
        "phone": "+963 955 334466",
        "bio": "طالب سنة ثالثة متفوق، باحث في الذكاء الاصطناعي التوليدي ومطور تطبيقات جوال احترافية.",
    },
    {
        "student_id": "202210145",
        "email": "lana.badr@asu.edu.sy",
        "name_ar": "لانا خليل بدر",
        "name_en": "Lana Khalil Badr",
        "avatar": "/images/students/student_female_2.png",
        "year": 3,
        "gpa": 3.86,
        "total_credits": 160,
        "completed_credits": 96,
        "is_top": False,
        "rank": None,
        "phone": "+963 966 445577",
        "bio": "طالبة سنة ثالثة، ناشطة في نوادي الروبوتيك وتطوير واجهات المستخدم الحديثة.",
    },
    {
        "student_id": "202310302",
        "email": "youssef.rahman@asu.edu.sy",
        "name_ar": "يوسف عبد الرحمن",
        "name_en": "Youssef Abdulrahman",
        "avatar": "/images/students/student_male_3.png",
        "year": 2,
        "gpa": 3.82,
        "total_credits": 160,
        "completed_credits": 64,
        "is_top": False,
        "rank": None,
        "phone": "+963 988 556688",
        "bio": "طالب سنة ثانية، مهتم بهندسة الخوارزميات وتطوير أدوات الويب مفتوحة المصدر.",
    },
    {
        "student_id": "202310118",
        "email": "raneem.othman@asu.edu.sy",
        "name_ar": "رنيم حسام عثمان",
        "name_en": "Raneem Hossam Othman",
        "avatar": "/images/students/student_female_3.png",
        "year": 2,
        "gpa": 3.79,
        "total_credits": 160,
        "completed_credits": 62,
        "is_top": False,
        "rank": None,
        "phone": "+963 944 667799",
        "bio": "طالبة سنة ثانية، مبرمجة طموحة في بايثون وجافا سكريبت ومصممة واجهات UI/UX.",
    },
]

for s in students_data:
    u = create_or_update_user(
        email=s["email"],
        password=DEFAULT_PASSWORD,
        role="student",
        name_ar=s["name_ar"],
        name_en=s["name_en"],
        avatar=s["avatar"],
        phone=s["phone"],
        assigned_faculty=faculty_ce,
        bio=s["bio"],
    )

    st_obj, _ = Student.objects.update_or_create(
        student_id=s["student_id"],
        defaults={
            "user": u,
            "name_ar": s["name_ar"],
            "name_en": s["name_en"],
            "email": s["email"],
            "faculty": faculty_ce,
            "program": program_se,
            "year": s["year"],
            "gpa": s["gpa"],
            "total_credits": s["total_credits"],
            "completed_credits": s["completed_credits"],
            "image": s["avatar"],
            "is_top": s["is_top"],
            "rank": s["rank"],
        }
    )
    print(f"Student: {st_obj.name_ar} (ID: {st_obj.student_id}, is_top: {st_obj.is_top}, rank: {st_obj.rank})")


# 6. Create Alumni Stories
print("\n--- Seeding Alumni Success Stories ---")

alumni_data = [
    {
        "email": "louay.shawaf@asu.edu.sy",
        "name_ar": "م. لؤي الشواف",
        "name_en": "Eng. Louay Al-Shawaf",
        "graduation_year": 2022,
        "program_ar": "هندسة البرمجيات",
        "program_en": "Software Engineering",
        "current_role_ar": "كبير مهندسي الحلول السحابية",
        "current_role_en": "Lead Cloud Solutions Architect",
        "company_ar": "شركة أمازون ويب سيرفيسز (AWS)",
        "company_en": "Amazon Web Services (AWS)",
        "story_ar": "شكلت المناهج المتطورة والمشاريع العملية في قسم هندسة البرمجيات بجامعة أنطاكية الأساس المتين الذي مكنني من قيادة الفرق البرمجية وتصميم حلول سحابية تخدم ملايين المستخدمين حول العالم.",
        "story_en": "The advanced curriculum and practical hands-on projects in the Software Engineering department at ASU provided the solid foundation that enabled me to lead technical teams and design cloud architectures serving millions globally.",
        "image": "/images/alumni/alumni_male_1.png",
    },
    {
        "email": "yasmine.kassem@asu.edu.sy",
        "name_ar": "م. ياسمين قاسم",
        "name_en": "Eng. Yasmine Kassem",
        "graduation_year": 2023,
        "program_ar": "هندسة البرمجيات",
        "program_en": "Software Engineering",
        "current_role_ar": "باحثة ومهندسة ذكاء اصطناعي",
        "current_role_en": "AI Research & NLP Engineer",
        "company_ar": "مجموعة التقنيات المستقبلية للذكاء الاصطناعي",
        "company_en": "Future AI Tech Lab",
        "story_ar": "خلال دراستي، أتيحت لي فرصة البحث العملي في مخابر الذكاء الاصطناعي التخصصية بإشراف نخبة من أساتذة القسم، وهو ما مهد لي الطريق لنشر أبحاث علمية والمنافسة في مسابقات دولية مرموقة.",
        "story_en": "During my studies, I had the privilege of conducting research in specialized AI labs under inspiring faculty mentorship, which paved the way for publishing scientific papers and competing internationally.",
        "image": "/images/alumni/alumni_female_1.png",
    },
    {
        "email": "tareq.badr@asu.edu.sy",
        "name_ar": "م. طارق بدر الدين",
        "name_en": "Eng. Tareq Badr Al-Din",
        "graduation_year": 2021,
        "program_ar": "هندسة البرمجيات",
        "program_en": "Software Engineering",
        "current_role_ar": "مؤسس ومدير تنفيذي تقني (CTO)",
        "current_role_en": "Co-Founder & CTO",
        "company_ar": "منصة تك تالنت التقنية (TechTalent Global)",
        "company_en": "TechTalent Global",
        "story_ar": "الدعم والتشجيع المستمر من كادر القسم كان المحفز الرئيسي لي لتحويل مشروع تخرجي إلى شركة ناشئة ناجحة، واليوم نوظف عشرات المهندسين ونقدم حلولنا الرقمية في عدة دول.",
        "story_en": "The continuous guidance and encouragement from department professors motivated me to turn my graduation project into a thriving startup that now employs dozens of engineers across multiple countries.",
        "image": "/images/alumni/alumni_male_2.png",
    },
    {
        "email": "maysaa.ghanem@asu.edu.sy",
        "name_ar": "م. ميساء غانم",
        "name_en": "Eng. Maysaa Ghanem",
        "graduation_year": 2023,
        "program_ar": "هندسة البرمجيات",
        "program_en": "Software Engineering",
        "current_role_ar": "مهندسة أمن برمجيات واختبار اختراق",
        "current_role_en": "AppSec & Penetration Testing Specialist",
        "company_ar": "شركة سيكيور كور الدولية",
        "company_en": "SecureCore International",
        "story_ar": "التركيز على ممارسات تطوير البرمجيات الآمنة ومخابر الأمن السيبراني في القسم زودني بالمهارات العملية المطلوبة لسوق العمل واجتياز اختبارات الشهادات الدولية بتفوق والالتحاق بكبرى الشركات التقنية.",
        "story_en": "Focus on secure coding and cybersecurity labs in the department equipped me with high-demand industry skills to pass professional certifications and excel in top cybersecurity roles.",
        "image": "/images/alumni/alumni_female_2.png",
    },
]

for a in alumni_data:
    u = create_or_update_user(
        email=a["email"],
        password=DEFAULT_PASSWORD,
        role="alumni",
        name_ar=a["name_ar"],
        name_en=a["name_en"],
        avatar=a["image"],
        assigned_faculty=faculty_ce,
        bio=a["story_ar"],
    )

    al_obj, _ = AlumniStory.objects.update_or_create(
        name_ar=a["name_ar"],
        faculty=faculty_ce,
        defaults={
            "name_en": a["name_en"],
            "graduation_year": a["graduation_year"],
            "program_ar": a["program_ar"],
            "program_en": a["program_en"],
            "current_role_ar": a["current_role_ar"],
            "current_role_en": a["current_role_en"],
            "company_ar": a["company_ar"],
            "company_en": a["company_en"],
            "story_ar": a["story_ar"],
            "story_en": a["story_en"],
            "image": a["image"],
        }
    )
    print(f"AlumniStory: {al_obj.name_ar} ({al_obj.current_role_ar} at {al_obj.company_ar})")


# 7. Create Official Curriculum Courses
print("\n--- Seeding Official Curriculum Courses ---")

courses_data = [
    # Year 1 - Semester 1
    ("SE101", "برمجة 1", "Programming I", 1, 1, 3, "المفاهيم الأساسية للبرمجة بلغة C++، المتغيرات، التوابع والمصفوفات.", "لا يوجد متطلب سابق"),
    ("MATH101", "رياضيات هندسية 1", "Engineering Mathematics I", 1, 1, 3, "التفاضل والتكامل المتقدم وتطبيقاته الهندسية.", "لا يوجد متطلب سابق"),
    ("PHYS101", "فيزياء عامة وإلكترونيات", "General Physics & Electronics", 1, 1, 3, "أسس الكهرباء والمغناطيسية والدارات الإلكترونية.", "لا يوجد متطلب سابق"),
    ("COMP101", "مدخل إلى الهندسة المعلوماتية", "Introduction to Informatics", 1, 1, 2, "بنية الحاسوب وتاريخ الحوسبة وأنظمة التشغيل.", "لا يوجد متطلب سابق"),
    ("ENG101", "لغة إنكليزية تخصصية 1", "Technical English I", 1, 1, 2, "المصطلحات التقنية في تكنولوجيا المعلومات وهندسة البرمجيات.", "لا يوجد متطلب سابق"),
    
    # Year 1 - Semester 2
    ("SE102", "برمجة 2 وبرمجة كائنية التوجه", "OOP & Programming II", 1, 2, 3, "البرمجة الشيئية: الأصناف، الوراثة، تعدد الأشكال وتغليف البيانات.", "SE101"),
    ("SE103", "الدارات المنطقية وبنية الحاسوب", "Digital Logic Circuits", 1, 2, 3, "الجبر البولياني، الدارات التركيبية والتعاقبية وتصميم المعالجات.", "COMP101"),
    ("MATH102", "الجبر الخطي والتحليل العددي", "Linear Algebra & Numerical Analysis", 1, 2, 3, "المصفوفات، الفضاءات الشعاعية والتحويلات الخطية.", "MATH101"),
    ("MATH103", "الرياضيات المتقطعة", "Discrete Mathematics", 1, 2, 3, "نظرية المجموعات، المنطق الرياضي، العلاقات ونظرية المخططات.", "لا يوجد متطلب سابق"),
    ("ENG102", "لغة إنكليزية تخصصية 2", "Technical English II", 1, 2, 2, "كتابة التقارير التقنية وتوثيق المشاريع البرمجية.", "ENG101"),

    # Year 2 - Semester 1
    ("SE201", "بنى المعطيات والخوارزميات", "Data Structures & Algorithms", 2, 1, 3, "القوائم المترابطة، الأشجار، المكدسات، الطوابير وخوارزميات الفرز.", "SE102"),
    ("SE202", "هندسة البرمجيات 1: التحليل والنمذجة", "Software Engineering I", 2, 1, 3, "دورة حياة البرمجيات، لغة النمذجة الموحدة UML وجمع المتطلبات.", "SE102"),
    ("SE203", "قواعد البيانات ونظم إدارتها", "Database Systems", 2, 1, 3, "النموذج العلائقي، لغة SQL، الجبر العلائقي والتسوية.", "SE102"),
    ("MATH201", "الاحتمالات والإحصاء التطبيقي", "Probability & Applied Statistics", 2, 1, 3, "المتغيرات العشوائية والتوزيعات الإحصائية ونظرية أخذ العينات.", "MATH101"),

    # Year 2 - Semester 2
    ("SE204", "نظم التشغيل", "Operating Systems", 2, 2, 3, "إدارة العمليات، الذاكرة، التزامن، نظام الملفات وبرمجة النواة.", "SE103, SE201"),
    ("SE205", "شبكات الحاسوب وبروتوكولات الإنترنت", "Computer Networks", 2, 2, 3, "نموذج OSI، بروتوكولات TCP/IP، التوجيه وأمن الشبكات.", "SE103"),
    ("SE206", "تصميم واجهات وتجربة المستخدم (UI/UX)", "UI/UX Design", 2, 2, 3, "مبادئ التصميم المتمركز حول المستخدم، تصميم النماذج الأولية واختبار قابلية الاستخدام.", "SE202"),
    ("SE207", "تطوير تطبيقات الويب الحديثة", "Modern Web Development", 2, 2, 3, "هندسة الواجهات الأمامية والخلفية وأطر العمل الحديثة (React / Node / Django).", "SE203"),

    # Year 3 - Semester 1
    ("SE301", "معمارية وأنماط التصميم البرمجي", "Software Architecture & Design Patterns", 3, 1, 3, "أنماط GoF، المعمارية الموجهة بالخدمات SOA والخدمات المصغرة Microservices.", "SE201, SE202"),
    ("SE302", "اختبار وضمان جودة البرمجيات", "Software Testing & QA", 3, 1, 3, "الاختبارات الأحادية والتكاملية، أتمتة الاختبارات ومقاييس الجودة CI/CD.", "SE202"),
    ("SE303", "الحوسبة السحابية وهندسة النظم الموزعة", "Cloud Computing & Distributed Systems", 3, 1, 3, "الحوسبة الافتراضية، الحاويات Docker، إدارة المجموعات Kubernetes والبنى السحابية.", "SE204, SE205"),
    ("SE304", "الذكاء الاصطناعي وتعلم الآلة", "AI & Machine Learning", 3, 1, 3, "خوارزميات البحث الذكي، التعلم الخاضع وغير الخاضع للإشراف والشبكات العصبية.", "SE201, MATH201"),

    # Year 3 - Semester 2
    ("SE305", "أمن البرمجيات والأمن السيبراني (DevSecOps)", "Software Security & DevSecOps", 3, 2, 3, "البرمجة الآمنة، كشف الثغرات OWASP، واختبار الاختراق التطبيقي.", "SE205, SE301"),
    ("SE306", "تطوير تطبيقات الجوال المتقدمة", "Mobile App Development", 3, 2, 3, "تطوير التطبيقات الأصلية والمتعددة المنصات (Flutter / React Native).", "SE207"),
    ("SE307", "إدارة المشاريع البرمجية ومنهجيات Agile", "Agile Software Project Management", 3, 2, 3, "منهجيات Scrum وKanban، تقدير التكاليف، وإدارة المخاطر البرمجية.", "SE202"),

    # Year 4 & 5 - Advanced & Capstone
    ("SE401", "هندسة البيانات الضخمة (Big Data)", "Big Data Engineering", 4, 1, 3, "أنظمة التخزين الموزعة، Apache Spark، ومعالجة التدفقات الكبيرة.", "SE203, SE303"),
    ("SE402", "معالجة اللغات الطبيعية ونظم الذكاء التوليدي", "NLP & Generative AI", 4, 2, 3, "بنى المحولات Transformers، النماذج اللغوية الكبيرة LLM وضبط النماذج.", "SE304"),
    ("SE501", "مشروع التخرج 1 (دراسة وتحليل)", "Graduation Project I", 5, 1, 3, "تحديد المشكلة البحثية، دراسة الجدوى، التحليل وتصميم المعمارية البرمجية.", "اجتياز 120 ساعة"),
    ("SE502", "مشروع التخرج 2 (تنفيذ واختبار)", "Graduation Project II", 5, 2, 4, "التنفيذ العملي، الاختبار الميداني، نشر النظام ومناقشة المشروع.", "SE501"),
]

for code, name_ar, name_en, yr, sem, cr, desc, prereq in courses_data:
    c_obj, _ = Course.objects.update_or_create(
        code=code,
        defaults={
            "program": program_se,
            "name_ar": name_ar,
            "name_en": name_en,
            "year": yr,
            "semester": sem,
            "credits": cr,
            "description_ar": desc,
            "description_en": desc,
            "prerequisites_text": prereq,
        }
    )
    print(f"Course: {c_obj.code} - {c_obj.name_ar} (Yr {c_obj.year}, Sem {c_obj.semester})")


# 8. Create News Articles
print("\n--- Seeding University, Faculty & Department News Articles ---")

news_data = [
    # General University News (faculty=None)
    {
        "slug": "asu-digital-transformation-strategy-2026",
        "title_ar": "جامعة أنطاكية السورية تدشن استراتيجية التحول الرقمي وتحديث البنية التحتية التكنولوجية",
        "title_en": "Antioch Syrian University Launches Digital Transformation Strategy 2026",
        "excerpt_ar": "إطلاق منظومة الخدمات الطلابية الذكية وتوسعة شبكة الألياف الضوئية وربط الكليات بأحدث التقنيات السحابية.",
        "excerpt_en": "Launch of smart student services platform and expansion of campus-wide cloud infrastructure.",
        "content_ar": "أعلنت رئاسة جامعة أنطاكية السورية عن انطلاق المرحلة الجديدة من خطة التحول الرقمي الشامل، والتي تتضمن تحديثاً جذرياً لكافة المنظومات الأكاديمية والمخبرية، وتوفير بيئة تعليمية ذكية تواكب أفضل المعايير الجامعية العالمية.",
        "content_en": "Antioch Syrian University announced the rollout of its comprehensive digital transformation roadmap, upgrading academic systems, research facilities, and delivering a smart campus experience.",
        "category": "achievement",
        "image": "/images/news/docs.png",
        "faculty": None,
        "date": date(2026, 9, 20),
        "featured": True,
    },
    {
        "slug": "fall-semester-registration-academic-scholarships",
        "title_ar": "بدء التسجيل للفصل الدراسي الجديد والإعلان عن منح التفوق الأكاديمي للطلاب المتميزين",
        "title_en": "Fall Semester Registration Opens with Academic Excellence Scholarships",
        "excerpt_ar": "تعلن عمادة القبول والتسجيل عن بدء استقبال طلبات التسجيل للفصل الدراسي وتخصيص منح للطلبة الأوائل.",
        "excerpt_en": "Admissions & Registration Deanship announces registration kickoff and merit scholarship programs.",
        "content_ar": "فتحت جامعة أنطاكية السورية أبواب التسجيل للفصل الدراسي الجديد لجميع الطلاب الجدد والقدامى في مختلف الكليات. كما تؤكد الجامعة استمرار برنامج منح التفوق السنوي الذي يكافئ المتفوقين في امتحانات الشهادة الثانوية والمراحل الجامعية.",
        "content_en": "ASU has opened enrollment for the upcoming semester across all faculties, reiterating its commitment to awarding merit-based scholarships for high-achieving applicants and existing students.",
        "category": "announcement",
        "image": "/images/news/registration.png",
        "faculty": None,
        "date": date(2026, 9, 15),
        "featured": False,
    },
    {
        "slug": "annual-student-scientific-cultural-trip",
        "title_ar": "تنظيم الرحلة العلمية والاستكشافية السنوية لطلاب الجامعة إلى مجمع مراكز الأبحاث والتكنولوجيا",
        "title_en": "Annual Scientific and Tech Expedition for University Students",
        "excerpt_ar": "زيارة ميدانية لطلاب مختلف الكليات للاطلاع على أحدث الابتكارات الصناعية والبحثية في سوريا.",
        "excerpt_en": "Field trip for ASU students exploring cutting-edge industrial innovation and research centers.",
        "content_ar": "نظمت عمادة شؤون الطلاب رحلة علمية واستكشافية شارك فيها أكثر من 150 طالباً وطالبة من كليات الهندسة والعلوم الإدارية، للتعرف عن قرب على آليات العمل في كبرى الشركات التقنية والمصانع الذكية.",
        "content_en": "The Deanship of Student Affairs organized an educational expedition for over 150 students from various colleges to gain practical insights into modern tech hubs and smart industries.",
        "category": "event",
        "image": "/images/news/trip.png",
        "faculty": None,
        "date": date(2026, 9, 10),
        "featured": False,
    },

    # Faculty News (faculty=faculty_ce)
    {
        "slug": "informatics-faculty-new-computing-research-complex",
        "title_ar": "كلية الهندسة المعلوماتية تفتتح مجمع مخابر الحوسبة المتقدمة والأنظمة الذكية",
        "title_en": "Faculty of Informatics Inaugurates Advanced Computing & Intelligent Systems Lab Complex",
        "excerpt_ar": "تجهيز 4 مخابر تخصصية جديدة بأحدث محطات العمل ووحدات GPU لدعم بحوث الذكاء الاصطناعي.",
        "excerpt_en": "Four brand-new specialized laboratories equipped with GPU clusters to support AI and data research.",
        "content_ar": "افتتحت عمادة كلية الهندسة المعلوماتية مجمع المخابر التخصصية الجديد، والذي يضم تجهيزات حديثة لمحاكاة الشبكات وتطوير النظم المدمجة وتدريب نماذج التعلم العميق، بما يوفر للطلاب والباحثين بيئة استثنائية للإبداع التقني.",
        "content_en": "The Faculty of Informatics inaugurated its new advanced computing facility featuring high-performance clusters for deep learning, cybersecurity sandboxing, and embedded hardware development.",
        "category": "achievement",
        "image": "/images/research-lab.jpg",
        "faculty": faculty_ce,
        "date": date(2026, 9, 18),
        "featured": True,
    },
    {
        "slug": "cloud-architecture-workshop-engineers-syndicate",
        "title_ar": "ورشة عمل تدريبية متقدمة في كلية الهندسة المعلوماتية حول معمارية الأنظمة السحابية والسيبرانية",
        "title_en": "Faculty of Informatics Hosts Specialized Workshop on Cloud & Cyber Architecture",
        "excerpt_ar": "سلسلة جلسات تدريبية بمشاركة خبراء محليين ودوليين لتعزيز مهارات طلاب الكلية وسوق العمل.",
        "excerpt_en": "Technical seminar series featuring industry veterans discussing enterprise cloud deployment.",
        "content_ar": "أقامت الكلية ورشة عمل تخصصية استمرت لمدة ثلاثة أيام ركزت على تصميم البنى التحتية السحابية المقاومة للأعطال، وشهدت تفاعلاً لافتاً من أساتذة الكلية وطلاب السنوات المتقدمة.",
        "content_en": "The faculty conducted a three-day intensive workshop on resilient cloud architectures and DevSecOps pipelines with active participation from students and faculty researchers.",
        "category": "event",
        "image": "/images/pages/research.png",
        "faculty": faculty_ce,
        "date": date(2026, 9, 5),
        "featured": False,
    },

    # Department News (faculty=faculty_ce, focused on Software Engineering)
    {
        "slug": "software-engineering-wins-national-programming-contest",
        "title_ar": "قسم هندسة البرمجيات يحصد المركز الأول في المسابقة البرمجية الجامعية السنوية 2026",
        "title_en": "Software Engineering Department Claims 1st Place at National Collegiate Programming Contest",
        "excerpt_ar": "فريق طلابي من قسم هندسة البرمجيات يتوج بلقب بطل البرمجة ويحقق درع التميز الأكاديمي.",
        "excerpt_en": "Student coding team from Software Engineering wins championship trophy at collegiate coding competition.",
        "content_ar": "حقق فريق قسم هندسة البرمجيات في جامعة أنطاكية السورية إنجازاً متميزاً بحصوله على المركز الأول وكأس التفوق في المسابقة البرمجية التنافسية، متفوقاً على أكثر من 30 فريقاً جامعياً. وأشاد رئيس القسم بالمستوى الرفيع والتفاني الاستثنائي الذي أظهره طلاب القسم في حل المسائل الخوارزمية المعقدة في زمن قياسي.",
        "content_en": "The software engineering student team at Antioch Syrian University achieved top honors at the collegiate programming championship, besting over 30 university teams. The department chair commended the students' exceptional algorithmic problem-solving skills.",
        "category": "achievement",
        "image": "/images/alumni/graduation_project/graduation.jpg",
        "faculty": faculty_ce,
        "date": date(2026, 9, 22),
        "featured": True,
    },
    {
        "slug": "software-engineering-graduation-projects-expo-2026",
        "title_ar": "معرض مشاريع تخرج قسم هندسة البرمجيات يختتم أعماله بتوقيع 10 عقود رعاية لابتكارات الطلاب",
        "title_en": "Software Engineering Capstone Expo Concludes with 10 Industry Sponsorship Deals",
        "excerpt_ar": "عرض أكثر من 25 مشروعاً ابتكارياً في مجالات الذكاء الاصطناعي والتطبيقات الطبية والحلول المالية.",
        "excerpt_en": "Over 25 student capstone innovations presented, resulting in industry incubation agreements.",
        "content_ar": "اختتم قسم هندسة البرمجيات فعاليات معرض مشاريع التخرج السنوي بحضور نخبة من ممثلي الشركات التكنولوجية والبنوك وغرفة التجارة. وقد أثمر المعرض عن توقيع اتفاقيات احتضان ورعاية لعشرة مشاريع ريادية نفذها طلاب القسم، مما يؤكد جودة التعليم وتطابق المخرجات مع متطلبات السوق الحقيقية.",
        "content_en": "The Software Engineering Capstone Exhibition concluded with resounding success as top tech firms and financial institutions attended and signed 10 incubation agreements for student projects.",
        "category": "event",
        "image": "/images/alumni/graduation_project/IMG-20240714-WA0030.jpg",
        "faculty": faculty_ce,
        "date": date(2026, 9, 12),
        "featured": True,
    },
    {
        "slug": "software-engineering-generative-ai-frameworks-symposium",
        "title_ar": "ندوة علمية تفاعلية ينظمها قسم هندسة البرمجيات حول أطر العمل الحديثة والذكاء الاصطناعي التوليدي",
        "title_en": "Software Engineering Department Organizes Symposium on Generative AI & Modern Frameworks",
        "excerpt_ar": "جلسات حوارية وبحوث تطبيقية قدمها كادر القسم حول دمج تقنيات LLM في دورة حياة تطوير البرمجيات.",
        "excerpt_en": "Symposium exploring integration of Large Language Models and agents across software development life cycles.",
        "content_ar": "نظم قسم هندسة البرمجيات ندوة علمية بعنوان 'الذكاء الاصطناعي التوليدي ومستقبل هندسة البرمجيات'، ناقش خلالها المحاضرون والباحثون أحدث أساليب توليد الأكواد المؤتمتة، واختبار البرمجيات الذكي، وكيفية تطوير مناهج القسم لمواكبة هذه الثورة التقنية.",
        "content_en": "Software Engineering Department held a specialized symposium titled 'Generative AI and the Future of Software Engineering', discussing LLM integration, automated testing, and next-generation developer tooling.",
        "category": "research",
        "image": "/images/pages/news.png",
        "faculty": faculty_ce,
        "date": date(2026, 9, 1),
        "featured": False,
    },
]

for n in news_data:
    art_obj, _ = NewsArticle.objects.update_or_create(
        slug=n["slug"],
        defaults={
            "title_ar": n["title_ar"],
            "title_en": n["title_en"],
            "excerpt_ar": n["excerpt_ar"],
            "excerpt_en": n["excerpt_en"],
            "content_ar": n["content_ar"],
            "content_en": n["content_en"],
            "category": n["category"],
            "image": n["image"],
            "faculty": n["faculty"],
            "date": n["date"],
            "featured": n["featured"],
        }
    )
    scope = "University (General)" if not art_obj.faculty else f"Faculty ({art_obj.faculty.name_ar})"
    print(f"NewsArticle: {art_obj.title_ar} [{scope}]")

print("\nSeeding completed successfully!")
