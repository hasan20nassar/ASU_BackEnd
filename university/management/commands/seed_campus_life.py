import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from university.models import (
    HousingFeature,
    StudentClub,
    SportActivity,
    CampusLifeOverview,
)

def seed_campus_life():
    print("Seeding Campus Life data...")

    # 1. Overview
    overview, created = CampusLifeOverview.objects.get_or_create(id=1)
    overview.housing_title_ar = "السكن الجامعي"
    overview.housing_title_en = "Student Housing"
    overview.housing_desc_ar = "توفر جامعة أنطاكية السورية سكناً جامعياً مريحاً وآمناً للطلاب من خارج دمشق، مع توفير جميع الخدمات الأساسية."
    overview.housing_desc_en = "Antioch Syrian University provides comfortable and safe housing for students from outside Damascus, with all essential services."
    overview.housing_image = "/images/pages/campus-life.png"
    overview.housing_contact_note_ar = "تواصل مع قسم شؤون الطلاب للحصول على مزيد من المعلومات"
    overview.housing_contact_note_en = "Contact the Student Affairs department for more information"
    overview.sports_title_ar = "الأنشطة الرياضية"
    overview.sports_title_en = "Sports Activities"
    overview.sports_desc_ar = "تولي الجامعة اهتماماً كبيراً بالجانب الرياضي وتوفر مرافق رياضية متنوعة للطلاب."
    overview.sports_desc_en = "The university pays great attention to sports and provides various sports facilities for students."
    overview.sports_image = "/images/pages/campus-life.png"
    overview.championships_title_ar = "البطولات السنوية"
    overview.championships_title_en = "Annual Championships"
    overview.championships_desc_ar = "تنظم الجامعة بطولات رياضية سنوية بين الكليات في مختلف الألعاب"
    overview.championships_desc_en = "The university organizes annual sports championships between faculties in various games"
    overview.save()
    print("  -> CampusLifeOverview seeded.")

    # 2. Housing Features
    housing_data = [
        {
            "title_ar": "غرف مريحة",
            "title_en": "Comfortable Rooms",
            "description_ar": "غرف مفردة ومزدوجة مجهزة بالكامل",
            "description_en": "Fully equipped single and double rooms",
            "icon": "Bed",
            "order": 1,
        },
        {
            "title_ar": "وجبات يومية",
            "title_en": "Daily Meals",
            "description_ar": "مطعم جامعي يقدم وجبات متنوعة",
            "description_en": "University cafeteria serving diverse meals",
            "icon": "Utensils",
            "order": 2,
        },
        {
            "title_ar": "إنترنت مجاني",
            "title_en": "Free WiFi",
            "description_ar": "إنترنت عالي السرعة في جميع المرافق",
            "description_en": "High-speed internet in all facilities",
            "icon": "Wifi",
            "order": 3,
        },
        {
            "title_ar": "مواصلات",
            "title_en": "Transportation",
            "description_ar": "خدمة نقل منتظمة من وإلى الحرم",
            "description_en": "Regular shuttle service to and from campus",
            "icon": "Bus",
            "order": 4,
        },
    ]

    for item in housing_data:
        feature, _ = HousingFeature.objects.update_or_create(
            title_ar=item["title_ar"],
            defaults={
                "title_en": item["title_en"],
                "description_ar": item["description_ar"],
                "description_en": item["description_en"],
                "icon": item["icon"],
                "order": item["order"],
                "is_active": True,
            },
        )
    print(f"  -> {len(housing_data)} Housing Features seeded.")

    # 3. Student Clubs
    clubs_data = [
        {
            "name_ar": "نادي الموسيقى",
            "name_en": "Music Club",
            "description_ar": "للطلاب المهتمين بالموسيقى والغناء",
            "description_en": "For students interested in music and singing",
            "icon": "Music",
            "category": "فنون وموسيقى",
            "supervisor": "أ. إياد كنعان",
            "order": 1,
        },
        {
            "name_ar": "نادي الفنون",
            "name_en": "Arts Club",
            "description_ar": "رسم وتصوير وفنون تشكيلية",
            "description_en": "Painting, photography, and visual arts",
            "icon": "Palette",
            "category": "فنون تشكيلية",
            "supervisor": "د. ريم حسون",
            "order": 2,
        },
        {
            "name_ar": "نادي القراءة",
            "name_en": "Reading Club",
            "description_ar": "مناقشات أدبية وثقافية",
            "description_en": "Literary and cultural discussions",
            "icon": "BookOpen",
            "category": "ثقافة وأدب",
            "supervisor": "أ. سامر علوش",
            "order": 3,
        },
        {
            "name_ar": "نادي اللغات",
            "name_en": "Language Club",
            "description_ar": "تعلم لغات جديدة وتبادل ثقافي",
            "description_en": "Learn new languages and cultural exchange",
            "icon": "Globe",
            "category": "لغات وتواصل",
            "supervisor": "د. نورا خوري",
            "order": 4,
        },
        {
            "name_ar": "نادي ريادة الأعمال",
            "name_en": "Entrepreneurship Club",
            "description_ar": "دعم المشاريع الناشئة والأفكار الإبداعية",
            "description_en": "Supporting startups and creative ideas",
            "icon": "Trophy",
            "category": "ريادة وابتكار",
            "supervisor": "د. طارق الحكيم",
            "order": 5,
        },
        {
            "name_ar": "نادي العمل التطوعي",
            "name_en": "Volunteer Club",
            "description_ar": "مبادرات خدمة المجتمع والمسؤولية الاجتماعية",
            "description_en": "Community service initiatives",
            "icon": "Heart",
            "category": "خدمة مجتمعية",
            "supervisor": "أ. مايا حداد",
            "order": 6,
        },
    ]

    for item in clubs_data:
        club, _ = StudentClub.objects.update_or_create(
            name_ar=item["name_ar"],
            defaults={
                "name_en": item["name_en"],
                "description_ar": item["description_ar"],
                "description_en": item["description_en"],
                "icon": item["icon"],
                "category": item["category"],
                "supervisor": item["supervisor"],
                "order": item["order"],
                "is_active": True,
            },
        )
    print(f"  -> {len(clubs_data)} Student Clubs seeded.")

    # 4. Sports Activities
    sports_data = [
        {"name_ar": "كرة القدم", "name_en": "Football", "icon": "Activity", "order": 1},
        {"name_ar": "كرة السلة", "name_en": "Basketball", "icon": "Activity", "order": 2},
        {"name_ar": "كرة الطائرة", "name_en": "Volleyball", "icon": "Activity", "order": 3},
        {"name_ar": "تنس الطاولة", "name_en": "Table Tennis", "icon": "Activity", "order": 4},
        {"name_ar": "الشطرنج", "name_en": "Chess", "icon": "Trophy", "order": 5},
        {"name_ar": "السباحة", "name_en": "Swimming", "icon": "Activity", "order": 6},
    ]

    for item in sports_data:
        sport, _ = SportActivity.objects.update_or_create(
            name_ar=item["name_ar"],
            defaults={
                "name_en": item["name_en"],
                "icon": item["icon"],
                "order": item["order"],
                "is_active": True,
            },
        )
    print(f"  -> {len(sports_data)} Sport Activities seeded.")

    print("Campus Life seeding completed successfully!")

if __name__ == "__main__":
    seed_campus_life()
