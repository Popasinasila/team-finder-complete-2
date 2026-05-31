"""Management command to populate the database with test data."""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create test users and projects for development"

    def handle(self, *args, **options):
        from projects.models import Project, FavoriteProject

        # ------------------------------------------------------------------ #
        # Users
        # ------------------------------------------------------------------ #
        users_data = [
            {
                "email": "admin@example.com",
                "first_name": "Администратор",
                "last_name": "Системы",
                "password": "adminpass123",
                "is_staff": True,
                "is_superuser": True,
                "bio": "Администратор платформы Team Finder",
                "phone": "+7 (000) 000-00-00",
                "github": "https://github.com/admin",
            },
            {
                "email": "alice@example.com",
                "first_name": "Алиса",
                "last_name": "Иванова",
                "password": "testpass123",
                "bio": "Full-stack разработчик, люблю Python и React",
                "phone": "+7 (999) 111-11-11",
                "github": "https://github.com/alice",
            },
            {
                "email": "bob@example.com",
                "first_name": "Борис",
                "last_name": "Петров",
                "password": "testpass123",
                "bio": "Дизайнер UX/UI, работаю с Figma",
                "phone": "+7 (999) 222-22-22",
                "github": "https://github.com/bob",
            },
            {
                "email": "carol@example.com",
                "first_name": "Карина",
                "last_name": "Сидорова",
                "password": "testpass123",
                "bio": "Data Scientist, ML-инженер",
                "phone": "+7 (999) 333-33-33",
                "github": "https://github.com/carol",
            },
        ]

        created_users = []
        for data in users_data:
            email = data["email"]
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                self.stdout.write(f"  User already exists: {email}")
            else:
                is_staff = data.pop("is_staff", False)
                is_superuser = data.pop("is_superuser", False)
                password = data.pop("password")
                user = User(**data)
                user.set_password(password)
                user.is_staff = is_staff
                user.is_superuser = is_superuser
                user.save()
                self.stdout.write(self.style.SUCCESS(f"  Created user: {email}"))
            created_users.append(user)

        admin_user, alice, bob, carol = created_users

        # ------------------------------------------------------------------ #
        # Projects
        # ------------------------------------------------------------------ #
        projects_data = [
            {
                "title": "Платформа для поиска команды",
                "description": (
                    "Разрабатываем веб-приложение для поиска участников в IT-проекты. "
                    "Нужны фронтендеры и дизайнеры."
                ),
                "author": alice,
                "status": "open",
            },
            {
                "title": "Мобильное приложение для медитации",
                "description": (
                    "Создаём iOS/Android-приложение с гидами по медитации. "
                    "Ищем React Native разработчиков."
                ),
                "author": alice,
                "status": "in_progress",
            },
            {
                "title": "Редизайн корпоративного сайта",
                "description": (
                    "Полный редизайн сайта крупной компании. "
                    "Требуется опыт работы с корпоративными брендбуками."
                ),
                "author": bob,
                "status": "open",
            },
            {
                "title": "Система анализа данных финансового рынка",
                "description": (
                    "Разрабатываем инструменты для анализа биржевых данных с использованием ML."
                ),
                "author": carol,
                "status": "open",
            },
            {
                "title": "Чат-бот для поддержки клиентов",
                "description": (
                    "Создаём AI-чат-бот на основе GPT для автоматизации клиентской поддержки."
                ),
                "author": admin_user,
                "status": "in_progress",
            },
        ]

        created_projects = []
        for data in projects_data:
            title = data["title"]
            if Project.objects.filter(title=title, author=data["author"]).exists():
                project = Project.objects.get(title=title, author=data["author"])
                self.stdout.write(f"  Project already exists: {title}")
            else:
                project = Project.objects.create(**data)
                self.stdout.write(self.style.SUCCESS(f"  Created project: {title}"))
            created_projects.append(project)

        p1, p2, p3, p4, p5 = created_projects

        # ------------------------------------------------------------------ #
        # Participants
        # ------------------------------------------------------------------ #
        participants = [
            (p1, bob),
            (p1, carol),
            (p2, bob),
            (p3, alice),
            (p4, alice),
            (p5, carol),
        ]
        for project, user in participants:
            if not project.participants.filter(pk=user.pk).exists():
                project.participants.add(user)

        # ------------------------------------------------------------------ #
        # Favorites
        # ------------------------------------------------------------------ #
        favorites = [
            (alice, p3),
            (alice, p4),
            (bob, p1),
            (bob, p4),
            (carol, p1),
            (carol, p2),
            (admin_user, p1),
        ]
        for user, project in favorites:
            FavoriteProject.objects.get_or_create(user=user, project=project)

        self.stdout.write(self.style.SUCCESS("\nTest data created successfully!"))
        self.stdout.write("Logins:")
        self.stdout.write("  admin@example.com / adminpass123  (superuser)")
        self.stdout.write("  alice@example.com / testpass123")
        self.stdout.write("  bob@example.com   / testpass123")
        self.stdout.write("  carol@example.com / testpass123")
