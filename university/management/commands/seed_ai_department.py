import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from university.models import Faculty, Program, Course, FacultyMember, NewsArticle

def seed_ai_department():
    faculty = Faculty.objects.get(slug="ce")
    
    # 1. Create or update AI Program
    ai_prog, created = Program.objects.get_or_create(
        slug="artificial-intelligence",
        faculty=faculty,
        defaults={
            "name_ar": "قسم الذكاء الاصطناعي وهندسة النظم",
            "name_en": "Department of Artificial Intelligence & Systems",
            "description_ar": "برنامج ريادي متخصص في هندسة خوارزميات الذكاء الاصطناعي، التعلم العميق، الرؤية الحاسوبية، والأنظمة التوليدية الذكية مع ربطها بالصناعة والتطبيقات الحيوية.",
            "description_en": "A premier academic program specializing in AI algorithms, deep learning, computer vision, and generative intelligence.",
            "motto_ar": "ريادة الابتكار في عصر الذكاء الاصطناعي",
            "motto_en": "Pioneering Innovation in the Age of AI",
            "primary_color": "#4338CA",
            "accent_color": "#06B6D4",
            "duration": 5,
            "credit_hours": 160,
            "min_score_percent": 68,
            "min_score_points": 140,
            "tuition_syrian": 2800000,
            "tuition_non_resident": 1600,
            "branch": "scientific",
            "head_name_ar": "د. مايا النجار",
            "head_name_en": "Dr. Maya Al-Najjar",
            "head_message_ar": "أهلاً بكم في قسم الذكاء الاصطناعي وهندسة النظم. نهدف إلى تأهيل جيل متميز من مهندسي وباحثي الذكاء الاصطناعي القادرين على تصميم وتطوير أحدث نماذج التعلم العميق والذكاء التوليدي وفق المعايير العالمية.",
            "head_message_en": "Welcome to the Department of Artificial Intelligence. We are dedicated to preparing high-caliber engineers and researchers ready to lead the global AI transformation.",
            "head_photo": "/images/faculty/prof_female_2.png",
            "career_paths": "مهندس خوارزميات الذكاء الاصطناعي\nعالم وباحث بيانات ضخمة (Data Scientist)\nمهندس نظم التعلم العميق والتعلم الآلي (MLOps Engineer)\nمطور تطبيقات الذكاء الاصطناعي التوليدي ونماذج LLMs\nمهندس الروبوتات والأنظمة الذكية المستقلة",
            "facilities": [
                {
                    "nameAr": "مجمع الحوسبة الفائقة ونظم التعلم العميق (GPU Cluster Lab)",
                    "nameEn": "Deep Learning & High Performance GPU Cluster",
                    "descriptionAr": "مجهز بوحدات معالجة رسومية فائقة الأداء من طراز NVIDIA A100 ومخدمات تدريب نماذج الذكاء الاصطناعي الضخمة."
                },
                {
                    "nameAr": "مخبر الروبوتات والرؤية الحاسوبية الذكية",
                    "nameEn": "Robotics & Computer Vision Laboratory",
                    "descriptionAr": "تجهيزات بصرية متطورة، كاميرات عمق ثلاثية الأبعاد، وأذرع روبوتية مخصصة للتحكم الذاتي والأتمتة."
                },
                {
                    "nameAr": "مختبر معالجة اللغات الطبيعية والذكاء التوليدي",
                    "nameEn": "NLP & Generative AI Innovation Hub",
                    "descriptionAr": "بيئات سحابية متقدمة لتطوير واختبار النماذج اللغوية الكبيرة وتطبيقات الوكلاء الأذكياء المستقلين."
                }
            ],
            "layout_config": {
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
                    "alumni_stories"
                ]
            }
        }
    )
    print(f"Program: {ai_prog.name_ar} (Created: {created})")

    # 2. Assign head of department faculty member if exists
    try:
        maya = FacultyMember.objects.get(name_ar__contains="مايا النجار")
        maya.is_head = True
        maya.department = ai_prog
        maya.department_ar = ai_prog.name_ar
        maya.department_en = ai_prog.name_en
        maya.save()
        ai_prog.head = maya
        ai_prog.save()
        print("Assigned Dr. Maya Al-Najjar as Head of AI Program")
    except FacultyMember.DoesNotExist:
        pass

    # 3. Seed AI Curriculum Courses
    courses_data = [
        # Year 1, Sem 1
        ("AI101", "مدخل إلى هندسة الذكاء الاصطناعي", "Introduction to AI Engineering", 3, 1, 1, "لا يوجد متطلبات سابقة", "مفاهيم الذكاء الاصطناعي، تاريخه، مجالات التطبيق، وأخلاقيات التقنية."),
        ("MATH101", "رياضيات متقدمة للذكاء الاصطناعي", "Advanced Mathematics for AI", 3, 1, 1, "لا يوجد متطلبات سابقة", "حساب التفاضل والتكامل متعدد المتغيرات، الدوال الهندسية والتحليل الرياضي."),
        ("PHYS101", "فيزياء النظم والإلكترونيات الذكية", "Systems Physics & Smart Electronics", 3, 1, 1, "لا يوجد متطلبات سابقة", "مبادئ الدارات الكهربائية، الحساسات الإلكترونية، والفيزياء التطبيقية."),
        ("COMP101", "البرمجة بلغة بايثون وهندسة الخوارزميات", "Python Programming & Algorithms", 3, 1, 1, "لا يوجد متطلبات سابقة", "بنى البرمجة الأساسية في Python، المكتبات العلمية NumPy و Pandas."),
        ("ENG101", "لغة إنكليزية تقنية 1", "Technical English I", 2, 1, 1, "لا يوجد متطلبات سابقة", "المصطلحات التقنية في مجال علوم الحاسوب والذكاء الاصطناعي."),

        # Year 1, Sem 2
        ("AI102", "البرمجة كائنية التوجه المتقدمة", "Advanced Object-Oriented Programming", 3, 1, 2, "ناجح في COMP101", "الفئات، الوراثة، تعدد الأشكال، وتصميم الأنظمة البرمجية الحديثة."),
        ("MATH102", "الجبر الخطي ونظرية المصفوفات", "Linear Algebra & Matrix Theory", 3, 1, 2, "ناجح في MATH101", "الفضاءات الشعاعية، التحويلات الخطية، المتجهات الذاتية وتحليل القيم المفردة SVD."),
        ("MATH103", "الاحتمالات والإحصاء التطبيقي", "Probability & Applied Statistics", 3, 1, 2, "ناجح في MATH101", "المتغيرات العشوائية، التوزيعات الاحتمالية، واختبار الفرضيات الإحصائية."),
        ("COMP102", "الدارات الرقمية ومعالجات الذكاء الاصطناعي", "Digital Circuits & AI Processors", 3, 1, 2, "ناجح في PHYS101", "المنطق الرقمي، المعماريات المعالجة GPU و TPU، ومسرعات الذكاء الاصطناعي."),
        ("ENG102", "لغة إنكليزية تقنية 2 وكتابة الأبحاث", "Technical English II & Research Writing", 2, 1, 2, "ناجح في ENG101", "كتابة التقارير العلمية والمنشورات التقنية وإعداد العروض التقديمية."),

        # Year 2, Sem 1
        ("AI201", "بنى المعطيات وتصميم الخوارزميات", "Data Structures & Algorithm Design", 3, 2, 1, "ناجح في AI102", "الأشجار، الرسوم البيانية، خوارزميات البحث والفرز والبرمجة الديناميكية."),
        ("AI202", "تعلم الآلة 1: النماذج الإحصائية والتقليدية", "Machine Learning I: Statistical Models", 3, 2, 1, "ناجح في MATH102 و MATH103", "الانحدار الخطي واللوجستي، أشجار القرار، SVM، وخوارزميات العنقودية."),
        ("AI203", "قواعد البيانات وهندسة البيانات الضخمة", "Database & Big Data Engineering", 3, 2, 1, "ناجح في AI102", "نظم إدارة قواعد البيانات SQL و NoSQL، وهندسة خطوط معالجة البيانات ETL."),
        ("AI204", "الحساب المتوازي وبرمجة وحدات GPU", "Parallel Computing & GPU Programming", 3, 2, 1, "ناجح في COMP102", "الحوسبة المتوازية باستخدام CUDA ومكتبات التسريع البرمجي للذكاء الاصطناعي."),

        # Year 2, Sem 2
        ("AI205", "التعلم العميق والشبكات العصبية الاصطناعية", "Deep Learning & Neural Networks", 3, 2, 2, "ناجح في AI202", "الشبكات العصبية الالتفافية CNN، الشبكات المتكررة RNN، وتدريب نماذج PyTorch."),
        ("AI206", "الرؤية الحاسوبية ومعالجة الصور الرقمية", "Computer Vision & Image Processing", 3, 2, 2, "ناجح في AI202", "التعرف على الكائنات، التجزئة الدلالية، والتحليل البصري بالفيديو في الوقت الحقيقي."),
        ("AI207", "معالجة اللغات الطبيعية واسترجاع المعلومات", "Natural Language Processing & IR", 3, 2, 2, "ناجح في AI202", "تمثيل الكلمات، التحليل النحوي والدلالي، ونماذج التضمين اللغوي Embeddings."),
        ("AI208", "هندسة البرمجيات وتصميم النظم الذكية", "AI Software Engineering", 3, 2, 2, "ناجح في AI201", "منهجيات التطوير السريع، معمارية الخدمات المصغرة، وأنماط دمج نماذج الذكاء."),

        # Year 3, Sem 1
        ("AI301", "نماذج الذكاء الاصطناعي التوليدي و LLMs", "Generative AI & Large Language Models", 3, 3, 1, "ناجح في AI205 و AI207", "معمارية المحولات Transformers، تدريب وتكييف النماذج اللغوية، وتقنيات RAG."),
        ("AI302", "الروبوتات والأنظمة المستقلة الذكية", "Robotics & Autonomous Systems", 3, 3, 1, "ناجح في AI206", "الملاحة الذاتية، التخطيط الحركي، ونظام تشغيل الروبوتات ROS 2."),
        ("AI303", "أمن وموثوقية نظم الذكاء الاصطناعي", "AI Safety, Security & Ethics", 2, 3, 1, "ناجح في AI205", "الهجمات العدائية على النماذج، التحيز والخوارزميات العادلة، والامتثال للخصوصية."),

        # Year 3, Sem 2
        ("AI304", "التعلم المعزز ونظم اتخاذ القرار", "Reinforcement Learning & Decision Making", 3, 3, 2, "ناجح في AI205", "سلاسل ماركوف، خوارزميات Q-Learning، وتطبيقات التعلم المعزز العميق."),
        ("AI305", "هندسة خطوط نشر النماذج (MLOps)", "MLOps & AI Model Deployment", 3, 3, 2, "ناجح في AI208", "مراقبة أداء النماذج، الحاويات Docker و Kubernetes، وأتمتة النشر السحابي CI/CD."),

        # Year 4 & 5
        ("AI401", "مشروع التخرج 1: الدراسة والنمذجة", "Graduation Project I", 3, 4, 1, "إنجاز 100 ساعة معتمدة", "دراسة المشكلة، مراجعة الأدبيات، واختيار معمارية الذكاء الاصطناعي المناسبة."),
        ("AI402", "مشروع التخرج 2: التنفيذ والاختبار الميداني", "Graduation Project II", 4, 4, 2, "ناجح في AI401", "تدريب النموذج، التحقق العملي، واختبار النظام وتقديمه أمام لجنة التحكيم الأكاديمية."),
    ]

    added_courses = 0
    for code, name_ar, name_en, credits, year, semester, prereq, desc in courses_data:
        c, created = Course.objects.update_or_create(
            code=code,
            defaults={
                "name_ar": name_ar,
                "name_en": name_en,
                "credits": credits,
                "program": ai_prog,
                "year": year,
                "semester": semester,
                "prerequisites_text": prereq,
                "description_ar": desc,
                "description_en": desc,
            }
        )
        if created:
            added_courses += 1

    print(f"Total AI Courses in DB: {Course.objects.filter(program=ai_prog).count()} (Newly created: {added_courses})")

    # 4. Add AI News Article
    news, created = NewsArticle.objects.get_or_create(
        slug="ai-department-launches-nvidia-gpu-lab-2026",
        defaults={
            "faculty": faculty,
            "title_ar": "قسم الذكاء الاصطناعي يدشن مجمع مخابر الحوسبة الفائقة ومعالجة النماذج التوليدية 2026",
            "title_en": "AI Department Inaugurates Supercomputing & Generative AI Lab Complex 2026",
            "excerpt_ar": "افتتح قسم الذكاء الاصطناعي وهندسة النظم في كلية الهندسة المعلوماتية مجمعاً مخبرياً متطوراً مخصصاً لأبحاث وتدريب نماذج الذكاء الاصطناعي التوليدي والتعلم العميق.",
            "excerpt_en": "The Department of Artificial Intelligence inaugurated an advanced computing facility dedicated to generative AI models and deep learning research.",
            "content_ar": "تأكيداً على ريادة جامعة أنطاكية السورية، افتتح قسم الذكاء الاصطناعي مجمع مخابر الحوسبة الفائقة المجهز بوحدات GPU من أحدث طراز، لتمكين الطلاب والباحثين من تدريب النماذج اللغوية الضخمة وتطوير ابتكارات الذكاء الاصطناعي التطبيقية.",
            "content_en": "Demonstrating academic excellence, the Department of AI opened a cutting-edge GPU supercomputing complex.",
            "image": "/images/news/docs.png",
            "category": "achievement",
            "featured": True,
            "date": "2026-09-28",
        }
    )
    print(f"AI Department news created: {created}")

if __name__ == "__main__":
    seed_ai_department()
