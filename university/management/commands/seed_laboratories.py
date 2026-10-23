import sys
from django.core.management.base import BaseCommand
from university.models import Faculty, FacultyLaboratory


class Command(BaseCommand):
    help = "Seeds initial laboratories and research facilities for all faculties in the database."

    def handle(self, *args, **options):
        if hasattr(sys.stdout, "reconfigure"):
            try:
                sys.stdout.reconfigure(encoding="utf-8")
            except Exception:
                pass

        self.stdout.write(self.style.NOTICE("==> Seeding Faculty Laboratories into Database..."))

        LABS_BY_KEYWORD = [
            (
                ["informatic", "comput", "it", "ce", "software", "eng"],
                [
                    {
                        "name_ar": "مخبر الذكاء الاصطناعي والحوسبة الفائقة",
                        "name_en": "Artificial Intelligence & HPC Lab",
                        "description_ar": "مجهز بوحدات معالجة رسومية متطورة (NVIDIA GPU Cluster) لتدريب نماذج التعلم العميق، الرؤية الحاسوبية وتطبيقات الذكاء التوليدي.",
                        "description_en": "Equipped with advanced NVIDIA GPU clusters for deep learning, computer vision, and generative AI research.",
                        "equipment_ar": "خوادم معالجة رسومية NVIDIA RTX 4090/A100، شاشات عرض تفاعلية، بيئة سحابية خاصة للتدريب.",
                        "equipment_en": "NVIDIA GPU clusters, 4K collaborative touchscreens, high-throughput private cloud.",
                        "location_ar": "مبنى الهندسة - الطابق الثالث - القاعة 302",
                        "location_en": "Engineering Building - 3rd Floor - Lab 302",
                        "capacity": 35,
                        "supervisor_name_ar": "د. مايا النجار",
                        "supervisor_name_en": "Dr. Maya Al-Najjar",
                    },
                    {
                        "name_ar": "مخبر النظم المدمجة وإنترنت الأشياء (IoT)",
                        "name_en": "Embedded Systems & IoT Lab",
                        "description_ar": "بيئة تطبيقية متكاملة لبرمجة المتحكمات الدقيقة، المستشعرات الذكية، وأنظمة الأتمتة الصناعية والروبوتات.",
                        "description_en": "Integrated hands-on environment for microcontroller programming, smart sensors, industrial automation, and robotics.",
                        "equipment_ar": "منصات Arduino/Raspberry Pi، راسمات إشارة رقمية، مجسات ذكية وأذرع روبوتية تعليمية.",
                        "equipment_en": "Arduino & ARM testbenches, digital oscilloscopes, IoT sensor kits, programmable robotic arms.",
                        "location_ar": "مبنى الهندسة - الطابق الثالث - القاعة 305",
                        "location_en": "Engineering Building - 3rd Floor - Lab 305",
                        "capacity": 30,
                        "supervisor_name_ar": "أ.د. سامر الحلبي",
                        "supervisor_name_en": "Prof. Samer Al-Halabi",
                    },
                    {
                        "name_ar": "مخبر الأمن السيبراني والشبكات السحابية",
                        "name_en": "Cybersecurity & Cloud Networks Lab",
                        "description_ar": "مختبر معزول لاختبار الاختراق الأخلاقي، محاكاة الهجمات والتهديدات السيبرانية، وإدارة البنى التحتية السحابية الموزعة.",
                        "description_en": "Isolated environment for ethical hacking, penetration testing, threat simulation, and distributed cloud systems.",
                        "equipment_ar": "مبدلات وموجهات Cisco/MikroTik معتمدة، جدران نارية مادية، مزارع افتراضية معزولة.",
                        "equipment_en": "Enterprise Cisco/MikroTik switches & routers, hardware firewalls, sandboxed virtualization racks.",
                        "location_ar": "مبنى الهندسة - الطابق الثاني - القاعة 210",
                        "location_en": "Engineering Building - 2nd Floor - Lab 210",
                        "capacity": 28,
                        "supervisor_name_ar": "د. كنان منصور",
                        "supervisor_name_en": "Dr. Kinan Mansour",
                    },
                    {
                        "name_ar": "مخبر هندسة البرمجيات والواقع الافتراضي",
                        "name_en": "Software Engineering & VR Studio",
                        "description_ar": "محطات عمل عالية الأداء لتصميم النظم البرمجية المعقدة، اختبار الجودة، وبناء بيئات الواقع المعزز والافتراضي.",
                        "description_en": "High-performance workstations for large-scale software modeling, automated testing, and immersive VR/AR experiences.",
                        "equipment_ar": "نظارات Meta Quest Pro / HTC Vive، محطات تطوير برمجية متقدمة، بيئات اختبار تكامل مستمر.",
                        "equipment_en": "VR/AR headsets (Meta Quest Pro/HTC Vive), precision code development stations, CI/CD runners.",
                        "location_ar": "مبنى الهندسة - الطابق الأول - القاعة 115",
                        "location_en": "Engineering Building - 1st Floor - Lab 115",
                        "capacity": 32,
                        "supervisor_name_ar": "م. رامي حداد",
                        "supervisor_name_en": "Eng. Rami Haddad",
                    },
                ],
            ),
            (
                ["dent", "med", "health"],
                [
                    {
                        "name_ar": "مخبر المحاكاة ورؤوس الفانتوم السريرية",
                        "name_en": "Phantom Head & Clinical Simulation Lab",
                        "description_ar": "بيئة محاكاة سريرية متقدمة مزودة برؤوس فانتوم تفاعلية لتدريب الطلاب على المهارات السريرية التشخيصية والعلاجية.",
                        "description_en": "Advanced phantom simulator units allowing students to master hands-on clinical and diagnostic skills in a safe environment.",
                        "equipment_ar": "وحدات فانتوم هيد كافو (KaVo) بمواصفات ألمانية، كاميرات مجهرية داخلية، شاشات متابعة للمدربين.",
                        "equipment_en": "KaVo dental simulator units, intraoral microscopic cameras, live instructor demonstration displays.",
                        "location_ar": "مبنى الكليات الطبية - الطابق الأول - القاعة 101",
                        "location_en": "Medical Sciences Building - 1st Floor - Lab 101",
                        "capacity": 40,
                        "supervisor_name_ar": "د. غسان شريف",
                        "supervisor_name_en": "Dr. Ghassan Sharif",
                    },
                    {
                        "name_ar": "مخبر التشريح الرقمي والمحاكاة ثلاثية الأبعاد",
                        "name_en": "Digital Anatomy & 3D Virtual Dissection Lab",
                        "description_ar": "طاولات تشريح رقمية تفاعلية لعرض التفاصيل المجهرية والتشريحية بدقة فائقة وبشكل تفاعلي ثلاثي الأبعاد.",
                        "description_en": "Interactive digital dissection tables enabling students to explore high-resolution 3D anatomical structures.",
                        "equipment_ar": "طاولات Anatomage رقمية جراحية، أجهزة عرض هولوغرافي ونماذج تشريحية عالية الدقة.",
                        "equipment_en": "Anatomage virtual dissection tables, high-definition anatomical models, 3D surgical display monitors.",
                        "location_ar": "مبنى الكليات الطبية - الطابق الثاني - القاعة 204",
                        "location_en": "Medical Sciences Building - 2nd Floor - Lab 204",
                        "capacity": 30,
                        "supervisor_name_ar": "د. ريم العلي",
                        "supervisor_name_en": "Dr. Reem Al-Ali",
                    },
                    {
                        "name_ar": "مخبر التعويضات والابتسامة الرقمية (CAD/CAM)",
                        "name_en": "Digital Prosthetics & CAD/CAM Lab",
                        "description_ar": "أنظمة مسح وتصميم رقمي متطورة وطباعة ثلاثية الأبعاد لإنتاج التركيبات والتعويضات بدقة ميكرونية متقدمة.",
                        "description_en": "State-of-the-art 3D scanners, CAD/CAM milling units, and fabrication systems for modern restorative dentistry.",
                        "equipment_ar": "ماسحات فموية ثلاثية الأبعاد 3Shape، آلات تفريز خماسية المحاور، أفران تلبيد الزركونيا الرقمية.",
                        "equipment_en": "3Shape intraoral scanners, 5-axis dental milling machines, high-temp zirconia sintering furnaces.",
                        "location_ar": "مبنى الكليات الطبية - الطابق الثالث - القاعة 312",
                        "location_en": "Medical Sciences Building - 3rd Floor - Lab 312",
                        "capacity": 25,
                        "supervisor_name_ar": "د. عمار الخالد",
                        "supervisor_name_en": "Dr. Ammar Al-Khaled",
                    },
                ],
            ),
            (
                ["pharm"],
                [
                    {
                        "name_ar": "مخبر الكيمياء الصيدلية وتصميم الدواء",
                        "name_en": "Medicinal Chemistry & Drug Design Lab",
                        "description_ar": "مجهز بأجهزة قياس الطيف، المحاكاة الجزيئية، والتخليق الكيميائي للمركبات الدوائية المبتكرة.",
                        "description_en": "Equipped with spectrophotometers, molecular modeling software, and synthesis tools for novel therapeutic compounds.",
                        "equipment_ar": "أجهزة UV-Vis، مبخرات دوارة Buchi، محطات نمذجة جزيئية حاسوبية.",
                        "equipment_en": "UV-Vis spectrophotometers, Buchi rotary evaporators, molecular docking computer stations.",
                        "location_ar": "مبنى الصيدلة - الطابق الثاني - القاعة 201",
                        "location_en": "Pharmacy Building - 2nd Floor - Lab 201",
                        "capacity": 30,
                        "supervisor_name_ar": "د. لين طحان",
                        "supervisor_name_en": "Dr. Leen Tahhan",
                    },
                    {
                        "name_ar": "مخبر الصيدلانيات وتكنولوجيا النانو",
                        "name_en": "Pharmaceutics & Nanotechnology Lab",
                        "description_ar": "أجهزة متقدمة لتصنيع الأشكال الصيدلانية، اختبارات الذوبان والانحلال، وتطوير نواقل الأدوية النانوية.",
                        "description_en": "Advanced equipment for pharmaceutical dosage formulation, dissolution profiling, and nanocarrier research.",
                        "equipment_ar": "أجهزة قياس حجم الجسيمات النانوية، أجهزة قياس الذوبانية USP، مكابس أقراص آلية.",
                        "equipment_en": "Zetasizer nanoparticle analyzers, automated USP dissolution testers, tablet compression stations.",
                        "location_ar": "مبنى الصيدلة - الطابق الثالث - القاعة 308",
                        "location_en": "Pharmacy Building - 3rd Floor - Lab 308",
                        "capacity": 28,
                        "supervisor_name_ar": "د. حسام المصري",
                        "supervisor_name_en": "Dr. Hussam Al-Masri",
                    },
                ],
            ),
            (
                ["arch", "civil", "art"],
                [
                    {
                        "name_ar": "استوديو التصميم المعماري ونمذجة BIM",
                        "name_en": "BIM & Architectural Design Studio",
                        "description_ar": "محطات نمذجة متقدمة وبرمجيات نمذجة معلومات البناء وتوليد الرسوم والواقع الافتراضي للمشاريع الحضرية.",
                        "description_en": "Advanced workstations running industry-standard BIM, parametric modeling, and architectural rendering suites.",
                        "equipment_ar": "محطات رسم رقمية Wacom، برمجيات Revit/Rhino/Lumion، أجهزة مسح ليزري ثلاثي الأبعاد للمواقع.",
                        "equipment_en": "Wacom Cintiq drawing tablets, Revit/Rhino/Lumion licenses, 3D laser site scanners.",
                        "location_ar": "مبنى العمارة - الطابق الرابع - الأتيليه 401",
                        "location_en": "Architecture Building - 4th Floor - Studio 401",
                        "capacity": 35,
                        "supervisor_name_ar": "أ.د. باسل ناصر",
                        "supervisor_name_en": "Prof. Bassel Nasser",
                    },
                    {
                        "name_ar": "مخبر ميكانيك التربة وفحص المواد الإنشائية",
                        "name_en": "Soil Mechanics & Materials Testing Lab",
                        "description_ar": "أجهزة قياس قوة الخرسانة، اختبارات الشد والضغط للمواد، وأجهزة الفحص الجيوتقني للتربة.",
                        "description_en": "Universal testing machines for concrete and steel tensile/compression tests, plus geotechnical soil equipment.",
                        "equipment_ar": "مكابس كسر الخرسانة الرقمية، أجهزة القص المباشر للتربة، أجهزة الموجات فوق الصوتية لاختبار المواد.",
                        "equipment_en": "Digital concrete compression machines, direct shear apparatus, ultrasonic pulse velocity testers.",
                        "location_ar": "مبنى الهندسة المدنية - الطابق الأرضي - القاعة G-04",
                        "location_en": "Civil Engineering Building - Ground Floor - Lab G-04",
                        "capacity": 25,
                        "supervisor_name_ar": "د. زياد عيسى",
                        "supervisor_name_en": "Dr. Ziad Issa",
                    },
                ],
            ),
        ]

        DEFAULT_FALLBACK_LABS = [
            {
                "name_ar": "مخبر الأبحاث العلمية والدراسات التخصصية",
                "name_en": "Advanced Scientific & Research Lab",
                "description_ar": "بيئة بحثية تفاعلية مزودة بأحدث التجهيزات والبرمجيات المتخصصة لدعم أبحاث الطلاب ومشاريع التخرج.",
                "description_en": "Interactive research environment equipped with modern specialized equipment to support graduation research.",
                "equipment_ar": "شاشات تفاعلية ذكية، حزم برمجيات التحليل المتقدم، محطات عمل مخصصة للبحث التطبيقي.",
                "equipment_en": "Smart interactive displays, statistical & simulation software suites, dedicated research benches.",
                "location_ar": "المبنى الأكاديمي الرئيسي - الطابق الثاني",
                "location_en": "Main Academic Building - 2nd Floor",
                "capacity": 30,
                "supervisor_name_ar": "أمانة الكلية البحثية",
                "supervisor_name_en": "Faculty Research Secretariat",
            },
            {
                "name_ar": "حاضنة الابتكار ومشاريع التخرج",
                "name_en": "Innovation & Graduation Projects Hub",
                "description_ar": "مساحة عمل مشتركة تتيح للفرق الطلابية تطوير نماذجهم التطبيقية وربطها بمتطلبات سوق العمل والمجتمع.",
                "description_en": "Collaborative workspace enabling student teams to develop prototypes and align projects with industry needs.",
                "equipment_ar": "طابعات ثلاثية الأبعاد، أدوات النمذجة السريعة، شبكة اتصالات عالية السرعة.",
                "equipment_en": "3D prototyping printers, maker tools, high-speed dedicated network link.",
                "location_ar": "المبنى الأكاديمي الرئيسي - الطابق الأول",
                "location_en": "Main Academic Building - 1st Floor",
                "capacity": 35,
                "supervisor_name_ar": "لجنة المشاريع التطبيقية",
                "supervisor_name_en": "Applied Projects Committee",
            },
        ]

        total_created = 0
        faculties = Faculty.objects.all()

        if not faculties.exists():
            self.stdout.write(self.style.WARNING("No faculties found in database. Please run seed_db first."))
            return

        for faculty in faculties:
            # Check if faculty already has laboratories in the new table
            existing_labs = FacultyLaboratory.objects.filter(faculty=faculty)
            if existing_labs.exists():
                self.stdout.write(f"  [OK] Faculty '{faculty.name_en or faculty.slug}' already has {existing_labs.count()} laboratories.")
                continue

            slug_lower = faculty.slug.lower()
            name_lower = faculty.name_en.lower()

            # Find matching lab templates
            selected_templates = None
            for keywords, templates in LABS_BY_KEYWORD:
                if any(kw in slug_lower or kw in name_lower for kw in keywords):
                    selected_templates = templates
                    break

            if not selected_templates:
                selected_templates = DEFAULT_FALLBACK_LABS

            # Create labs for this faculty
            created_labs_list = []
            for idx, lab_data in enumerate(selected_templates):
                lab_obj = FacultyLaboratory.objects.create(
                    faculty=faculty,
                    name_ar=lab_data["name_ar"],
                    name_en=lab_data["name_en"],
                    description_ar=lab_data.get("description_ar", ""),
                    description_en=lab_data.get("description_en", ""),
                    equipment_ar=lab_data.get("equipment_ar", ""),
                    equipment_en=lab_data.get("equipment_en", ""),
                    location_ar=lab_data.get("location_ar", ""),
                    location_en=lab_data.get("location_en", ""),
                    capacity=lab_data.get("capacity", 30),
                    supervisor_name_ar=lab_data.get("supervisor_name_ar", ""),
                    supervisor_name_en=lab_data.get("supervisor_name_en", ""),
                    order=idx,
                    is_active=True,
                )
                created_labs_list.append({
                    "nameAr": lab_obj.name_ar,
                    "nameEn": lab_obj.name_en,
                    "descriptionAr": lab_obj.description_ar,
                    "descriptionEn": lab_obj.description_en,
                })
                total_created += 1

            # Update faculty counters and facilities JSON
            faculty.labs_count = len(selected_templates)
            faculty.facilities = created_labs_list
            faculty.save(update_fields=["labs_count", "facilities"])

            self.stdout.write(
                self.style.SUCCESS(
                    f"  [CREATED] Created {len(selected_templates)} laboratories for '{faculty.name_en or faculty.slug}' ({faculty.slug})"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f"\nSuccessfully seeded {total_created} laboratories across all faculties.")
        )
