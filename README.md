# 🚀 Template Matching Service

---

## 📘 Описание проекта

Это веб-приложение на основе **FastAPI**, которое позволяет находить лучшие совпадения шаблонов для переданных параметров запроса. Приложение использует асинхронный подход для обработки запросов и эффективно обрабатывает поиск совпадений шаблонов.

---

## 🔧 **Основные компоненты**

- **FastAPI** — быстрый и асинхронный фреймворк для разработки веб-приложений.
- **Docker** — для контейнеризации приложения.
- **pytest** — для тестирования.
- **mocker** — для мокирования функций в тестах.

---

## 📜 **Структура проекта**
```
/app
    main.py
    utils.py
    handler.py
    db.py
    templates.json

/tests
    test_template_matcher.py
    requests_test.py
    test_identify_field_type.py

Dockerfile
requirements.txt
README.md
```

---

## ⚙️ **Инструкция по запуску проекта через Docker**

---

### 📌 **Предварительные требования**

Убедитесь, что у вас установлен **Docker** и **Docker Compose**.

- [Docker](https://docs.docker.com/get-started/docker-overview/)


---

## 🚀 **Шаги запуска через Docker**

### 1. **Клонируйте репозиторий**

Склонируйте репозиторий проекта:

```bash
git clone https://github.com/NikolayBogachev/Web.git
cd your-repository
```
### 2. **Соберите Docker-образ**

Выполните команду для сборки Docker-образа:

```bash

docker build -t template-matching-service .
```
 - -t template-matching-service — это имя образа.

### 3. **Запустите контейнер**

Теперь запустите контейнер:

```bash

docker run -d -p 8000:8000 template-matching-service
```
- -d — запускает контейнер в фоновом режиме.
- -p 8000:8000 — перенаправляет порт 8000 хоста в порт контейнера.

### 4. **Проверьте работу приложения**

После запуска FastAPI будет доступно по адресу:

```
http://localhost:8000
```
Вы можете использовать Postman или браузер для тестирования API.

