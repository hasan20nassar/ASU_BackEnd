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
    FacultyMember,
    Event,
    UserProfile,
)

User = get_user_model()
DEFAULT_PASSWORD = "Password123!"

print("Starting Faculty (ce) enhancements: Dean, Facilities, and Events...")

# 1. Fetch Faculty (ce)
faculty_ce = Faculty.objects.get(slug="ce")

# 2. Create Dean User & FacultyMember
dean_email = "dean.ce@asu.edu.sy"
dean_user = User.objects.filter(email=dean_email).first()
if not dean_user:
    dean_user = User.objects.create_user(
        email=dean_email,
        password=DEFAULT_PASSWORD,
        username=dean_email,
        name_ar="أ.د. عصام الدين خوري",
        name_en="Prof. Dr. Issam Eldin Khoury",
        role="faculty",
        avatar="/images/faculty/prof_male_5.png",
        phone="+963 944 123789",
        assigned_faculty=faculty_ce,
        bio="أستاذ دكتور في علوم الحاسوب وهندسة البرمجيات، عميد كلية الهندسة المعلوماتية بجامعة أنطاكية السورية.",
    )
    print(f"Created Dean User: {dean_email}")
else:
    dean_user.name_ar = "أ.د. عصام الدين خوري"
    dean_user.name_en = "Prof. Dr. Issam Eldin Khoury"
    dean_user.avatar = "/images/faculty/prof_male_5.png"
    dean_user.set_password(DEFAULT_PASSWORD)
    dean_user.save()
    print(f"Updated Dean User: {dean_email}")

dean_member, _ = FacultyMember.objects.update_or_create(
    email=dean_email,
    defaults={
        "user": dean_user,
        "faculty": faculty_ce,
        "name_ar": "أ.د. عصام الدين خوري",
        "name_en": "Prof. Dr. Issam Eldin Khoury",
        "title_ar": "أستاذ دكتور - عميد كلية الهندسة المعلوماتية",
        "title_en": "Professor & Dean of Informatics Engineering",
        "department_ar": "عمادة كلية الهندسة المعلوماتية",
        "department_en": "Deanship of Faculty of Informatics",
        "description_ar": "دكتوراه في هندسة النظم الذكية وشبكات المعلومات، عميد الكلية ومستشار التحول الرقمي.",
        "description_en": "Ph.D. in Intelligent Systems & Information Networks, Dean of Informatics Engineering.",
        "office_hours": "يومياً من 10:00 إلى 13:00",
        "location_ar": "مبنى كلية الهندسة المعلوماتية - مكتب العميد (الطابق الثالث)",
        "location_en": "Faculty of Informatics - Dean's Office (3rd Floor)",
        "image": "/images/faculty/prof_male_5.png",
        "is_head": True,
        "bio_ar": "دكتوراه في علوم الحاسوب وهندسة النظم الذكية، خبرة تزيد عن 20 عاماً في التعليم الأكاديمي والبحث العلمي وتطوير المناهج الهندسية.",
        "bio_en": "Ph.D. in Computer Science & Intelligent Systems, over 20 years of experience in higher education and engineering research.",
        "education_ar": [
            "دكتوراه في هندسة النظم الذكية - جامعة السوربون (2005)",
            "ماجستير في علوم الحاسوب - جامعة دمشق (2000)",
            "إجازة في الهندسة المعلوماتية - جامعة دمشق (1996)",
        ],
        "education_en": [
            "Ph.D. in Intelligent Systems - Sorbonne University (2005)",
            "M.Sc. in Computer Science - Damascus University (2000)",
            "B.Sc. in Informatics Engineering - Damascus University (1996)",
        ],
        "research_ar": "الذكاء الاصطناعي، أمن الشبكات المتقدم، واستراتيجيات التحول الرقمي في التعليم العالي.",
        "research_en": "Artificial Intelligence, Advanced Network Security, Higher Education Digital Transformation.",
        "publications": [
            "Frameworks for National Digital Transformation in Higher Education (2024)",
            "Scalable Architectures for Enterprise Knowledge Graphs (2022)",
        ],
    }
)
print(f"Dean FacultyMember created/updated: {dean_member.name_ar}")

# 3. Update Faculty Dean & Facilities
faculty_ce.dean = dean_member
faculty_ce.dean_name_ar = "أ.د. عصام الدين خوري"
faculty_ce.dean_name_en = "Prof. Dr. Issam Eldin Khoury"
faculty_ce.dean_photo = "/images/faculty/prof_male_5.png"
faculty_ce.dean_message_ar = (
    "أهلاً بكم في رحاب كلية الهندسة المعلوماتية بجامعة أنطاكية السورية. "
    "تحرص كليتنا منذ تأسيسها على تقديم تعليم هندسي تقني بمعايير عالمية يرتكز على الإبداع والبحث العلمي والشراكة مع قطاع التكنولوجيا، "
    "لإعداد كوادر وطنية متميزة قادرة على قيادة التحول الرقمي ومواكبة الثورة الصناعية الرابعة وبناء مستقبل تكنولوجي واعد."
)
faculty_ce.dean_message_en = (
    "Welcome to the Faculty of Informatics Engineering at Antioch Syrian University. "
    "Since our foundation, we have been dedicated to delivering world-class technical engineering education centered on innovation, "
    "applied research, and industry collaboration to empower future engineers to spearhead digital transformation."
)

faculty_ce.facilities = [
    {
        "nameAr": "مجمع مخابر الحوسبة المتقدمة والأنظمة الذكية",
        "nameEn": "Advanced Computing & Intelligent Systems Lab Complex",
        "descriptionAr": "مجهز بوحدات معالجة رسومية فائقة السرعة GPU ومخدمات متخصصة لمعالجة الخوارزميات وتدريب نماذج الذكاء الاصطناعي والتعلم العميق.",
        "descriptionEn": "Equipped with high-performance GPU clusters and servers for deep learning, AI training, and parallel computing research.",
    },
    {
        "nameAr": "مختبر البرمجيات والأنظمة السحابية الموزعة",
        "nameEn": "Cloud & Distributed Software Systems Lab",
        "descriptionAr": "محطات عمل حديثة مجهزة بأحدث أدوات التطوير ومحاكيات البنى السحابية والحاويات الافتراضية وبيئات CI/CD المتكاملة.",
        "descriptionEn": "Modern workstations equipped with cloud emulation platforms, containerized environments, and CI/CD pipelines.",
    },
    {
        "nameAr": "مختبر الأمن السيبراني وتأمين الشبكات الحيوية",
        "nameEn": "Cybersecurity & Critical Infrastructure Defense Lab",
        "descriptionAr": "بيئة معزولة مخصصة لاختبارات الاختراق الأمني ومحاكاة الهجمات وتأمين حركة البيانات وتشفير البروتوكولات الحساسة.",
        "descriptionEn": "Isolated sandbox environment designed for penetration testing, attack simulation, and cryptographic protocols research.",
    },
    {
        "nameAr": "مختبر النظم المدمجة وإنترنت الأشياء (IoT & Embedded Systems)",
        "nameEn": "IoT & Embedded Systems Engineering Lab",
        "descriptionAr": "أجهزة قياس إلكترونية وراسمات إشارة ومتحكمات دقيقة ومجموعات استشعار لتطوير الأجهزة الذكية والأنظمة الصناعية المتقدمة.",
        "descriptionEn": "Oscilloscopes, microcontrollers, sensor kits, and FPGA development boards for smart hardware engineering.",
    },
    {
        "nameAr": "استوديو تصميم واجهات وتجربة المستخدم (UI/UX Design Studio)",
        "nameEn": "UI/UX & Interactive Design Studio",
        "descriptionAr": "أجهزة لوحية ومختبرات تتبع حركة العين وأحدث برمجيات النمذجة التفاعلية لتصميم ودراسة تجربة المستخدم الرقمية.",
        "descriptionEn": "Interactive design stations, prototyping software, and usability testing tools for digital product design.",
    },
    {
        "nameAr": "مخبر بحوث وتنقيب البيانات الضخمة (Big Data Research Lab)",
        "nameEn": "Big Data Analytics & Mining Lab",
        "descriptionAr": "بنية تحتية سحابية متقدمة مخصصة لمعالجة التدفقات الضخمة للبيانات، والتحليل الإحصائي، ونمذجة الأعمال الذكية.",
        "descriptionEn": "High-throughput data processing infrastructure for big data streaming, predictive analytics, and business intelligence.",
    },
]

# Ensure layout_config has all 9 sections enabled
faculty_ce.layout_config = {
    "headerStyle": "hero_split",
    "showQuickStats": True,
    "showDeanMessage": True,
    "showPrograms": True,
    "showNews": True,
    "showEvents": True,
    "showFacilities": True,
    "showStaff": True,
    "showTopStudents": True,
    "showAlumniStories": True,
    "sectionsOrder": [
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
    "sectionsConfig": {
        "stats": {"titleAr": "أرقام وإحصائيات الكلية", "titleEn": "Faculty Key Statistics", "layoutVariant": "grid"},
        "dean": {"titleAr": "كلمة عميد الكلية ومجلسها", "titleEn": "Dean's Welcome Message", "layoutVariant": "split", "showCta": True, "ctaTextAr": "تواصل مع مكتب العميد", "ctaLink": "#contact"},
        "programs": {"titleAr": "الأقسام والتخصصات الأكاديمية", "titleEn": "Departments & Academic Programs", "layoutVariant": "grid"},
        "news": {"titleAr": "أخبار وإعلانات الكلية الحصرية", "titleEn": "Faculty News & Announcements", "layoutVariant": "grid", "itemLimit": 6},
        "events": {"titleAr": "فعاليات وأنشطة الكلية", "titleEn": "Faculty Events & Seminars", "layoutVariant": "grid", "itemLimit": 6},
        "facilities": {"titleAr": "المختبرات والعيادات والمشاغل", "titleEn": "Laboratories & Clinical Facilities", "layoutVariant": "grid"},
        "staff": {"titleAr": "دليل الكادر التدريسي والأكاديمي", "titleEn": "Faculty Teaching Staff", "layoutVariant": "grid", "itemLimit": 8},
        "top_students": {"titleAr": "لوحة الشرف وأوائل الكلية", "titleEn": "Faculty Honor Roll"},
        "alumni_stories": {"titleAr": "قصص نجاح الخريجين", "titleEn": "Alumni Success Stories"},
    }
}

faculty_ce.save()
print("Faculty (ce) updated with Dean, Facilities, and Layout Config.")

# 4. Seed Events for Faculty of Informatics
print("\n--- Seeding Faculty Events ---")

events_data = [
    {
        "title_ar": "المؤتمر السنوي للذكاء الاصطناعي وهندسة البيانات الضخمة (ASU AI Conference 2026)",
        "title_en": "Annual Conference on Artificial Intelligence & Big Data 2026",
        "description_ar": "مؤتمر علمي دولي بمشاركة نخبة من الباحثين لمناقشة أحدث تقنيات نماذج اللغات الضخمة وتطبيقاتها في الأنظمة الذكية.",
        "description_en": "International scientific conference featuring leading researchers exploring Large Language Models and intelligent systems applications.",
        "date": date(2026, 10, 15),
        "time": "09:30 - 15:00",
        "location_ar": "مدرج الباسل المركزي - حرم معرة صيدنايا",
        "location_en": "Al-Bassel Grand Auditorium - Main Campus",
        "type": "academic",
    },
    {
        "title_ar": "الهاكاثون البرمجي السنوي لحلول التحول الرقمي (ASU Codeathon 2026)",
        "title_en": "Annual Codeathon for Digital Transformation Solutions",
        "description_ar": "مسابقة برمجية مكثفة على مدار 48 ساعة لفرق طلابية لتطوير حلول برمجية مبتكرة برعاية كبرى شركات التكنولوجيا.",
        "description_en": "48-hour intensive coding hackathon for student teams to develop innovative software solutions sponsored by top tech firms.",
        "date": date(2026, 10, 22),
        "time": "10:00 - 18:00",
        "location_ar": "مجمع المخابر التخصصية - الطابق الثاني",
        "location_en": "Advanced Labs Complex - 2nd Floor",
        "type": "career",
    },
    {
        "title_ar": "اليوم المهني ومعرض التوظيف لقطاع تكنولوجيا المعلومات (IT Career Fair 2026)",
        "title_en": "Informatics & IT Career Fair 2026",
        "description_ar": "ملتقى توظيفي يجمع طلاب وخريجي الكلية مع أكثر من 20 شركة برمجيات واتصالات لتقديم فرص تدريب وتوظيف مباشرة.",
        "description_en": "Annual career fair connecting informatics students and graduates with over 20 leading software and telecom companies.",
        "date": date(2026, 11, 5),
        "time": "10:00 - 16:00",
        "location_ar": "بهو كلية الهندسة المعلوماتية وقاعة المعارض",
        "location_en": "Faculty Exhibition Hall & Main Lobby",
        "type": "career",
    },
    {
        "title_ar": "سلسلة ورشات الأمن السيبراني واختبار الاختراق الأخلاقي (CyberSec Bootcamp)",
        "title_en": "Cybersecurity & Ethical Hacking Hands-on Bootcamp",
        "description_ar": "ورشات تدريبية عملية تركز على تأمين التطبيقات السحابية ومحاكاة الهجمات السيبرانية للدفاع عن البنى الرقمية الحيوية.",
        "description_en": "Hands-on technical workshops focused on cloud security posture and ethical hacking defense mechanisms.",
        "date": date(2026, 11, 18),
        "time": "12:00 - 14:30",
        "location_ar": "مختبر الشبكات والأمن السيبراني - قاعة 205",
        "location_en": "Cybersecurity & Networks Lab - Hall 205",
        "type": "academic",
    },
    {
        "title_ar": "معرض الابتكار والملصقات البحثية لطلاب مشاريع التخرج والدراسات العليا",
        "title_en": "Capstone Innovations & Scientific Posters Exhibition",
        "description_ar": "استعراض الملصقات البحثية والمشاريع المبتكرة التي أنجزها طلاب الكلية بحضور ممثلي غرف التجارة والصناعة.",
        "description_en": "Research poster expo highlighting student capstone innovations in front of industry stakeholders.",
        "date": date(2026, 12, 2),
        "time": "11:00 - 15:30",
        "location_ar": "مركز المؤتمرات الأكاديمية",
        "location_en": "Academic Conference Center",
        "type": "academic",
    },
    {
        "title_ar": "البطولة الرياضية السنوية لكليات الجامعة في كرة السلة والشطرنج",
        "title_en": "Annual Inter-Faculty Sports Tournament (Basketball & Chess)",
        "description_ar": "منافسات رياضية تفاعلية بين طلاب كليات الجامعة لتعزيز الروح الرياضية والتواصل الطلابي.",
        "description_en": "Friendly tournament between university faculties promoting student sportsmanship and campus life.",
        "date": date(2026, 12, 10),
        "time": "14:00 - 18:00",
        "location_ar": "الصالة الرياضية المغلقة - الحرم الجامعي",
        "location_en": "Indoor Sports Complex - Main Campus",
        "type": "sports",
    },
]

for ev in events_data:
    ev_obj, _ = Event.objects.update_or_create(
        title_ar=ev["title_ar"],
        faculty=faculty_ce,
        defaults={
            "title_en": ev["title_en"],
            "description_ar": ev["description_ar"],
            "description_en": ev["description_en"],
            "date": ev["date"],
            "time": ev["time"],
            "location_ar": ev["location_ar"],
            "location_en": ev["location_en"],
            "type": ev["type"],
        }
    )
    print(f"Event created: {ev_obj.title_ar} ({ev_obj.date})")

print("\nFaculty enhancements completed successfully!")
