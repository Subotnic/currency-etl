# Currency ETL Pipeline (Airflow + ClickHouse)

## Описание проекта

Этот проект реализует ETL-пайплайн для загрузки и обработки данных о валютных курсах.

Пайплайн автоматически:
- извлекает данные из внешнего API
- преобразует их в нужный формат
- загружает в аналитическую базу данных ClickHouse

Оркестрация процессов осуществляется с помощью Apache Airflow.

---

## Архитектура

Пайплайн состоит из трёх этапов:

extract → transform → load

Поток данных:

API → Airflow → ClickHouse

---

## Используемые технологии

- Python
- Apache Airflow — оркестрация задач
- ClickHouse — аналитическая база данных
- Docker / Docker Compose — контейнеризация
- Pandas — обработка данных

---

## Структура проекта

.
├── dags/
│   │── integration_currency.py      # DAG Airflow
│   └── maintenance_currency.py      # DAG Airflow
├── src/
│   ├── extract.py                   # Получение данных
│   ├── transform.py                 # Обработка данных
│   └── load.py                      # Загрузка в ClickHouse
├── sql/
│   └── create_table.sql             # Создание таблицы
├── docker/
│   └── docker-compose.yml           # Контейнеры

---

## Запуск проекта

### 1. Клонировать репозиторий

git clone <your_repo_url>
cd currency_etl

### 2. Запустить контейнеры

docker compose up --build

### 3. Открыть Airflow

http://localhost:8080

### 4. Данные для входа

Логин: admin  
Пароль: admin

---

## Как работает пайплайн

### 1. Extract
Получение данных о курсах валют из API

### 2. Transform
- добавление UUID
- преобразование типов данных
- подготовка к загрузке

### 3. Load
- подключение к ClickHouse
- вставка данных в таблицу currency

---

## Особенности реализации

- Используется UUID как уникальный идентификатор
- Данные проходят преобразование типов:
  - string → UUID
  - string → datetime
  - string → date
- Таблица в ClickHouse создаётся автоматически при запуске
- Проект полностью изолирован через Docker

---

## Структура таблицы

CREATE TABLE currency
(
    id UUID,
    date Date,
    usd Float64,
    euro Float64,
    created DateTime,
    updated Nullable(DateTime)
)
ENGINE = MergeTree()
ORDER BY date;

---

## Ограничения текущей реализации

- Используется XCom для передачи данных между задачами (подходит только для небольших объёмов)
- Установка зависимостей происходит при запуске контейнера
- Нет обработки ошибок и повторных попыток (retry)

---

## Возможные улучшения

- Убрать XCom и использовать staging (файлы или промежуточные таблицы)
- Создать кастомный Docker-образ с зависимостями
- Добавить retry и логирование в Airflow
- Реализовать валидацию данных перед загрузкой
- Добавить мониторинг (Prometheus / Grafana)
- Подключить BI-инструменты (Metabase / Superset)

---

## Пример данных

| id | date | usd | euro |
|----|------|-----|------|
| UUID | 2026-03-16 | 1.0 | 1.1478 |

---

## Автор

Макс
