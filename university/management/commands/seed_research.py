import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from university.models import ResearchCenter, ResearchArea, ResearchPublication, Faculty

def seed():
    print("Seeding Research Centers, Areas, and Publications...")

    # 1. Seed Research Centers
    centers_data = [
        {
            "title_ar": "مركز أبحاث العلوم الطبية",
            "title_en": "Medical Sciences Research Center",
            "description_ar": "أبحاث متقدمة في طب الأسنان والصيدلة والعلوم الطبية الحيوية والتقانات الدوائية.",
            "description_en": "Advanced research in dentistry, pharmacy, biomedical sciences and pharmaceutical technologies.",
            "icon": "Microscope",
            "director_name_ar": "أ.د. سمير النجار",
            "director_name_en": "Prof. Samir Al-Najjar",
            "location": "مبنى الكليات الطبية - الطابق الثالث",
            "contact_email": "medical.research@asu.edu.sy",
            "order": 1,
        },
        {
            "title_ar": "مركز أبحاث الهندسة والتقانة",
            "title_en": "Engineering & Technology Research Center",
            "description_ar": "بحوث تطبيقية في الهندسة المدنية والمعمارية وهندسة البرمجيات والذكاء الاصطناعي.",
            "description_en": "Applied research in civil, architectural engineering, software engineering and AI.",
            "icon": "FlaskConical",
            "director_name_ar": "د. طارق الحبيس",
            "director_name_en": "Dr. Tarek Al-Habbis",
            "location": "مبنى كلية الهندسة - الطابق الرابع",
            "contact_email": "eng.research@asu.edu.sy",
            "order": 2,
        },
        {
            "title_ar": "مركز الدراسات الإنسانية واللغات",
            "title_en": "Humanities & Languages Research Center",
            "description_ar": "أبحاث متخصصة في الترجمة الفورية واللسانيات التطبيقية والدراسات القانونية المقارنة.",
            "description_en": "Specialized research in simultaneous translation, applied linguistics and comparative legal studies.",
            "icon": "BookOpen",
            "director_name_ar": "د. ناديا مراد",
            "director_name_en": "Dr. Nadia Murad",
            "location": "مبنى كلية الآداب - جناح اللغات",
            "contact_email": "humanities.research@asu.edu.sy",
            "order": 3,
        },
        {
            "title_ar": "مركز الابتكار وريادة الأعمال",
            "title_en": "Innovation & Entrepreneurship Center",
            "description_ar": "حاضنة للمشاريع البحثية الناشئة، وتحويل الأبحاث والأفكار الأكاديمية إلى منتجات صناعية وخدمية منافسة.",
            "description_en": "Incubator for emerging research projects, transforming academic ideas into competitive industrial and commercial products.",
            "icon": "Lightbulb",
            "director_name_ar": "د. ريم الخوري",
            "director_name_en": "Dr. Reem Al-Khouri",
            "location": "المبنى المركزي - مجمع ريادة الأعمال",
            "contact_email": "innovation@asu.edu.sy",
            "order": 4,
        },
    ]

    centers = {}
    for data in centers_data:
        center, _ = ResearchCenter.objects.get_or_create(
            title_ar=data["title_ar"],
            defaults=data
        )
        centers[center.title_ar] = center
        print(f"Center ready: {center.title_ar}")

    # 2. Seed Research Areas
    areas_data = [
        {"name_ar": "الذكاء الاصطناعي وتعلم الآلة", "name_en": "Artificial Intelligence & Machine Learning", "order": 1},
        {"name_ar": "العلوم الصيدلانية وتطوير الأدوية", "name_en": "Pharmaceutical Sciences & Drug Design", "order": 2},
        {"name_ar": "الطاقة المتجددة والاستدامة", "name_en": "Renewable Energy & Sustainability", "order": 3},
        {"name_ar": "هندسة المواد والإنشاءات", "name_en": "Materials Engineering & Construction", "order": 4},
        {"name_ar": "العلوم القانونية والتشريعات الرقمية", "name_en": "Legal Sciences & Digital Legislation", "order": 5},
        {"name_ar": "الترجمة واللسانيات الحاسوبية", "name_en": "Translation & Computational Linguistics", "order": 6},
    ]

    areas = {}
    for a in areas_data:
        area, _ = ResearchArea.objects.get_or_create(
            name_ar=a["name_ar"],
            defaults=a
        )
        areas[area.name_ar] = area
        print(f"Area ready: {area.name_ar}")

    # 3. Seed Publications
    publications_data = [
        {
            "title_ar": "تطوير مواد بناء مستدامة من النفايات الصناعية المعاد تدويرها",
            "title_en": "Development of Sustainable Building Materials from Recycled Industrial Waste",
            "authors_ar": "د. أحمد محمد، م. خالد سليم",
            "authors_en": "Dr. Ahmad Mohammad, Eng. Khaled Salim",
            "journal_ar": "مجلة الهندسة المدنية والمواد المستدامة",
            "journal_en": "Journal of Civil Engineering & Sustainable Materials",
            "publication_year": 2024,
            "research_area": areas.get("هندسة المواد والإنشاءات"),
            "center": centers.get("مركز أبحاث الهندسة والتقانة"),
            "abstract_ar": "يبحث هذا العمل في استخدام مخلفات الخبث والركام الصناعي لتحسين الخواص الميكانيكية للخرسانة الخضراء، وتقليل البصمة الكربونية للمنشآت الإنشائية بنسبة 28%.",
            "abstract_en": "This work explores using industrial slag and aggregates to enhance mechanical properties of green concrete, reducing structural carbon footprint by 28%.",
            "doi_url": "https://doi.org/10.1016/j.jobe.2024.108920",
            "is_featured": True,
            "views_count": 340,
            "downloads_count": 85,
        },
        {
            "title_ar": "تأثير النواقل النانوية الحديثة على فعالية علاج الأمراض المزمنة",
            "title_en": "Impact of Novel Nanocarriers on Therapeutic Efficacy for Chronic Diseases",
            "authors_ar": "د. سارة علي، أ.د. سمير النجار",
            "authors_en": "Dr. Sarah Ali, Prof. Samir Al-Najjar",
            "journal_ar": "المجلة الصيدلانية المتقدمة للأبحاث السريرية",
            "journal_en": "Advanced Pharmaceutical Journal for Clinical Research",
            "publication_year": 2024,
            "research_area": areas.get("العلوم الصيدلانية وتطوير الأدوية"),
            "center": centers.get("مركز أبحاث العلوم الطبية"),
            "abstract_ar": "دراسة تجريبية وتطبيقية لتقييم الحويصلات الدهنية النانوية في تحسين امتصاص المركبات الدوائية ضعيفة الانحلال، وتقليل الآثار الجانبية بنسبة تتجاوز 40%.",
            "abstract_en": "Experimental study evaluating liposomal nanocarriers in improving bioavailability of poorly soluble active compounds and reducing adverse effects by over 40%.",
            "doi_url": "https://doi.org/10.1016/j.ijpharm.2024.123901",
            "is_featured": True,
            "views_count": 512,
            "downloads_count": 130,
        },
        {
            "title_ar": "نماذج الرؤية الحاسوبية المعمقة في الكشف المبكر عن التشوهات السنية والتصوير الشعاعي",
            "title_en": "Deep Vision Models in Early Dental Anomaly Detection and Radiographic Analysis",
            "authors_ar": "د. محمد خالد، د. ليلى حسن",
            "authors_en": "Dr. Mohammad Khaled, Dr. Leila Hassan",
            "journal_ar": "مجلة الذكاء الاصطناعي والتطبيقات الطبية",
            "journal_en": "Journal of AI & Medical Imaging",
            "publication_year": 2023,
            "research_area": areas.get("الذكاء الاصطناعي وتعلم الآلة"),
            "center": centers.get("مركز أبحاث العلوم الطبية"),
            "abstract_ar": "تطبيق خوارزميات شبكات الطي العصبونية المتقدمة على صور البانوراما السنية لتشخيص الآفات الذروية بدقة بلغت 96.4% مقارنة بالتشخيص السريري التقليدي.",
            "abstract_en": "Applying advanced convolutional neural networks to dental panoramic radiographs to detect periapical lesions with 96.4% accuracy compared to conventional clinical diagnosis.",
            "doi_url": "https://doi.org/10.1038/s41598-023-45120-1",
            "is_featured": True,
            "views_count": 680,
            "downloads_count": 195,
        },
        {
            "title_ar": "الأطر التشريعية المنظمة للذكاء الاصطناعي وحماية البيانات في الفضاء الرقمي السوري",
            "title_en": "Legislative Frameworks for AI Regulation & Data Protection in Syrian Cyberspace",
            "authors_ar": "د. حسام الدين عبد الله",
            "authors_en": "Dr. Husam Eddin Abdullah",
            "journal_ar": "مجلة الدراسات القانونية والقضائية المقارنة",
            "journal_en": "Comparative Legal Studies Journal",
            "publication_year": 2024,
            "research_area": areas.get("العلوم القانونية والتشريعات الرقمية"),
            "center": centers.get("مركز الدراسات الإنسانية واللغات"),
            "abstract_ar": "قراءة تحليلية ونقدية في القوانين السورية مقارنة بالقانون الأوروبي لحماية البيانات (GDPR) فيما يتعلق بالمسؤولية المدنية والجزائية الناتجة عن أنظمة الذكاء الاصطناعي التوليدي.",
            "abstract_en": "Critical comparative analysis of Syrian cyber laws versus GDPR regarding civil and criminal liability arising from generative AI systems.",
            "doi_url": "https://doi.org/10.1093/clsr/2024.105820",
            "is_featured": False,
            "views_count": 210,
            "downloads_count": 45,
        },
    ]

    for p in publications_data:
        pub, _ = ResearchPublication.objects.get_or_create(
            title_ar=p["title_ar"],
            defaults=p
        )
        print(f"Publication ready: {pub.title_ar}")

    print("Research seeding completed successfully!")

if __name__ == "__main__":
    seed()
