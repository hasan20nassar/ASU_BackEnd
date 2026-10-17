import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

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

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
