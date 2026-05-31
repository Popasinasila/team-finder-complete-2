# Team Finder — Вариант 1

Веб-приложение для поиска участников в IT-проекты. Реализован **Вариант 1**: «Избранное» и фильтрация пользователей.

---

## Быстрый старт для ревьюера

### Требования

- [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/)

### 1. Клонировать репозиторий

```bash
git clone <url-репозитория>
cd team-finder-ad-main-3
```

### 2. Создать `.env`

Скопируйте пример и при необходимости измените параметры:

```bash
cp .env_example .env
```

Файл `.env_example` уже содержит корректные значения для запуска через Docker Compose.
Убедитесь, что `TASK_VERSION=1`.

### 3. Запустить проект

```bash
docker compose up --build
```

При первом запуске:
- Установятся зависимости Python
- Выполнятся миграции БД
- Создадутся тестовые данные (пользователи и проекты)
- Запустится сервер на `http://localhost:8000`

> Если Docker требует `sudo`, добавьте его перед командой.

### 4. Открыть приложение

Перейдите по адресу: **http://localhost:8000**

---

## Тестовые пользователи

| Email                 | Пароль       | Роль        |
|-----------------------|--------------|-------------|
| `admin@example.com`   | `adminpass123` | Суперпользователь |
| `alice@example.com`   | `testpass123`  | Обычный пользователь |
| `bob@example.com`     | `testpass123`  | Обычный пользователь |
| `carol@example.com`   | `testpass123`  | Обычный пользователь |

Каждый пользователь имеет минимум один созданный проект и настроенные связи (участие, избранное).

Панель администратора: **http://localhost:8000/admin/**

---

## Структура проекта

```
team-finder-ad-main-3/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI через GitHub Actions
├── projects/                   # Приложение проектов
│   ├── models.py               # Project, FavoriteProject
│   ├── views.py                # Все вьюхи для проектов
│   ├── forms.py
│   └── urls.py
├── users/                      # Приложение пользователей
│   ├── models.py               # Кастомная модель User
│   ├── views.py                # Все вьюхи для пользователей
│   ├── forms.py
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── create_test_data.py
├── team_finder/                # Конфигурация Django
│   ├── settings.py
│   └── urls.py
├── templates_var1/             # HTML-шаблоны (Вариант 1)
│   ├── base.html
│   ├── projects/
│   └── users/
├── static/                     # CSS, JS, изображения
├── docker-compose.yml          # PostgreSQL + Django web
├── entrypoint.sh               # Скрипт запуска контейнера
├── requirements.txt
└── .env_example
```

---

## Реализованный функционал

### Общая функциональность

| Страница | URL |
|----------|-----|
| Главная (список проектов) | `/projects/list/` |
| Детальная страница проекта | `/projects/<id>/` |
| Создание проекта | `/projects/create/` |
| Редактирование проекта | `/projects/<id>/edit/` |
| Список пользователей | `/users/list/` |
| Профиль пользователя | `/users/profile/<id>/` |
| Редактирование профиля | `/users/profile/edit/` |
| Регистрация | `/users/register/` |
| Вход | `/users/login/` |
| Смена пароля | `/users/password/` |
| Панель администратора | `/admin/` |

### Вариант 1: Избранное и фильтрация

- Добавление/удаление проектов в «Избранное» с главной страницы и страницы проекта (AJAX, без перезагрузки)
- Страница «Избранное» `/projects/favorites/` — только для владельца
- Фильтрация на странице `/users/list/?filter=<значение>`:
  - `favorites_authors` — авторы избранных проектов
  - `joined_authors` — авторы проектов, в которых я участвую
  - `users_who_like_my_projects` — пользователи, которым нравятся мои проекты
  - `my_project_participants` — участники моих проектов
- Активный фильтр подсвечивается, есть кнопка сброса

---

## Остановка проекта

```bash
docker compose down
```

Данные PostgreSQL сохраняются в Docker volume `postgres_data` и не теряются при перезапуске.

Для полного сброса (включая данные):

```bash
docker compose down -v
```

---

## CI / GitHub Actions

При каждом push/PR в ветку `main` или `master` автоматически:
1. Запускается PostgreSQL как сервис
2. Устанавливаются зависимости
3. Выполняется проверка PEP 8 (`flake8 --max-line-length=100`)
4. Запускается `python manage.py check`
5. Применяются миграции
6. Создаются тестовые данные
7. Запускаются тесты Django

Конфигурация: `.github/workflows/ci.yml`
