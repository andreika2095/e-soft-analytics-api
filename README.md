API-сервис для анализа данных
https://img.shields.io/badge/Python-3.10%252B-blue
https://img.shields.io/badge/Flask-2.2.2-green
https://img.shields.io/badge/PostgreSQL-14%252B-blue

API-сервис для обработки и анализа данных с возможностью загрузки файлов, вычисления статистики, очистки данных и генерации графиков. Реализован в рамках задания компании «E-soft».

Особенности
📤 Загрузка файлов (CSV/XLSX) через API

📊 Вычисление статистики: среднее, медиана, корреляции

🧹 Очистка данных: удаление дубликатов, заполнение пропущенных значений

📈 Генерация графиков (гистограммы, scatter-графики)

💾 Хранение данных и результатов в PostgreSQL

✅ Полная реализация CRUD операций

Технологический стек
Backend: Python, Flask

База данных: PostgreSQL

Анализ данных: Pandas, NumPy

Визуализация: Matplotlib

ORM: SQLAlchemy

Тестирование: pytest

Установка и запуск
Предварительные требования
Python 3.10+

PostgreSQL 14+

pip (менеджер пакетов Python)

Шаг 1: Клонирование репозитория
bash
git clone https://github.com/andreika2095/e-soft-analytics-api.git
cd e-soft-analytics-api
Шаг 2: Создание виртуального окружения
bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
Шаг 3: Установка зависимостей
bash
pip install -r requirements.txt
Шаг 4: Настройка базы данных
Создайте базу данных PostgreSQL:

bash
sudo -u postgres psql -c "CREATE DATABASE analytics_db;"
Создайте пользователя БД:

bash
sudo -u postgres psql -c "CREATE USER api_user WITH PASSWORD 'secure_password';"
Назначьте права:

bash
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE analytics_db TO api_user;"
Шаг 5: Настройка переменных окружения
Создайте файл .env в корне проекта:

ini
DATABASE_URL=postgresql://api_user:secure_password@localhost/analytics_db
SECRET_KEY=your_secret_key_here
Шаг 6: Инициализация базы данных
bash
python init_db.py
Шаг 7: Запуск приложения
bash
python run.py
Сервис будет доступен по адресу: http://localhost:5000

Использование API
Основные эндпоинты
Метод	Эндпоинт	Описание	Параметры
POST	/upload	Загрузка файла (CSV/XLSX)	file (обязательный)
GET	/files	Список загруженных файлов	-
GET	/files/{id}	Информация о файле	-
GET	/stats/{id}	Статистика по файлу	-
GET	/clean/{id}	Очистка данных файла	-
GET	/plot/{id}	Генерация графика	type (histogram, scatter, boxplot)
DELETE	/files/{id}	Удаление файла и связанных данных	-
Примеры запросов
1. Загрузка файла

bash
curl -X POST -F "file=@data/sales_data.csv" http://localhost:5000/upload
Пример ответа:

json
{
  "id": 1,
  "filename": "sales_data.csv",
  "message": "File uploaded successfully",
  "uploaded_at": "2023-10-15T14:30:00Z"
}
2. Получение статистики

bash
curl http://localhost:5000/stats/1
Пример ответа:

json
{
  "file_id": 1,
  "filename": "sales_data.csv",
  "stats": {
    "correlation": {
      "price": {"quantity": 0.87},
      "quantity": {"price": 0.87}
    },
    "mean": {"price": 150.5, "quantity": 25.3},
    "median": {"price": 140.0, "quantity": 22.0}
  }
}
3. Очистка данных

bash
curl http://localhost:5000/clean/1
Пример ответа:

json
{
  "message": "Data cleaned successfully",
  "file_id": 1,
  "cleaned_at": "2023-10-15T14:35:22Z"
}
4. Генерация графика

bash
curl http://localhost:5000/plot/1?type=histogram -o histogram.png
Доступные типы графиков:

histogram - Гистограмма распределения

scatter - Scatter plot для двух столбцов (требует указания колонок)

boxplot - Box plot распределения данных

Структура проекта
text
e-soft-analytics-api/
├── app/                  # Основной модуль приложения
│   ├── __init__.py       # Инициализация приложения
│   ├── models.py         # Модели базы данных
│   ├── routes.py         # Маршруты API
│   ├── services.py       # Бизнес-логика обработки данных
│   └── utils.py          # Вспомогательные функции
├── tests/                # Тесты
│   ├── test_api.py       # Тесты API эндпоинтов
│   └── test_services.py  # Тесты бизнес-логики
├── migrations/           # Миграции базы данных (Alembic)
├── data/                 # Примеры данных для тестирования
├── config.py             # Конфигурация приложения
├── init_db.py            # Инициализация базы данных
├── requirements.txt      # Список зависимостей
├── run.py                # Точка входа приложения
└── .env                  # Файл переменных окружения
Тестирование
Для запуска тестов:

bash
pytest tests/
Тесты покрывают:

Загрузку файлов разных форматов

Корректность вычисления статистики

Логику очистки данных

Генерацию различных типов графиков

Обработку ошибок и пограничных случаев