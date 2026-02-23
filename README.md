# Token Platform Backend

Backend API для платформы токенов.

## Стек

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT

## Запуск

```bash
python -m uvicorn app.main:app --reload

# 🚀 Token Platform Backend

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-orange)
![JWT](https://img.shields.io/badge/Auth-JWT-black)

Backend API для платформы токенов с регистрацией пользователей, авторизацией и системой кошельков.

Проект реализован с использованием чистой архитектуры (Router → Service → Repository → Model).

---

# 📌 Возможности

- ✅ Регистрация пользователей
- ✅ JWT-аутентификация
- ✅ Ролевая модель (user / admin)
- ✅ Автоматическое создание кошелька при регистрации
- ✅ Swagger документация
- ✅ Миграции через Alembic
- ✅ Чистая архитектура

---

# 🏗 Архитектура проекта


token_platform/
│
├── app/
│ ├── models/ # SQLAlchemy модели
│ ├── schemas/ # Pydantic схемы
│ ├── routers/ # API endpoints
│ ├── services/ # Бизнес-логика
│ ├── repositories/ # Работа с БД
│ ├── core/ # Безопасность и зависимости
│ ├── database.py # Подключение к БД
│ └── main.py # Точка входа
│
├── alembic/ # Миграции
├── alembic.ini
├── requirements.txt
└── README.md


### Архитектурный принцип


Router → Service → Repository → Database


- Router — принимает HTTP запрос
- Service — содержит бизнес-логику
- Repository — работает с БД
- Model — описание таблиц

---

# 🛠 Технологический стек

- **FastAPI** — веб-фреймворк
- **PostgreSQL** — база данных
- **SQLAlchemy** — ORM
- **Alembic** — миграции
- **JWT (python-jose)** — авторизация
- **Passlib (bcrypt)** — хеширование паролей

---

# 🔐 Аутентификация

Используется JWT-токен:

- Алгоритм: HS256
- Access token expiration: 30 минут
- Пароли хешируются через bcrypt

---

# 📡 API Endpoints

### 🔹 Регистрация пользователя

POST /users/register


### 🔹 Профиль пользователя

GET /users/profile


### 🔹 Админ-панель (только admin)

GET /users/admin


---

# 📖 Документация API

После запуска сервера доступна по адресу:


http://127.0.0.1:8001/docs


---

# ▶ Запуск проекта

## 1️⃣ Клонирование

```bash
git clone https://github.com/2962414-create/token_platform.git
cd token_platform
2️⃣ Создание виртуального окружения
python -m venv venv
venv\Scripts\activate
3️⃣ Установка зависимостей
pip install -r requirements.txt
4️⃣ Настройка БД

Убедитесь, что PostgreSQL запущен
и строка подключения указана в database.py

5️⃣ Применение миграций
alembic upgrade head
6️⃣ Запуск сервера
python -m uvicorn app.main:app --reload
📈 Возможные улучшения

Redis для кэширования и rate-limiting

Docker контейнеризация

CI/CD

Транзакции и история операций

Тесты (pytest)

👨‍💻 Автор

Backend-разработчик (Python / FastAPI)

Проект создан для демонстрации навыков построения production-ready backend архитектуры.


