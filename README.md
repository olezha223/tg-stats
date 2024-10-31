# tg_chats

Веб приложение, которое выводит статистику вашего личного чата в Telegram

## Как пользоваться

1. Выберите любой ваш чат в desktop версии Telegram
2. Скачайте историю чата в формате json
3. Загрузите ваш чат в приложение и введите свой ник в Telegram 
4. Отправьте данные на анализ
5. Получите дашборды

## Как запустить

```shell
docker-compose up --build
```

## Стек приложения

1. Фронтенд:
    - React JS
    - Vite
    - axios
    - recharts
2. Бэкенд:
    - FastAPI
    - MongoDB

## Структура проекта

backend
├───src
│   ├───app
│   │   └───v1
│   │       └───handlers
│   ├───database
│   ├───models
│   ├───repository
│   └───service
│       ├───data
│       └───files
│   main.py
│   Dockerfile
│   requirements.txt
│   .gitignore

frontend
├───src
│   └───App.jsx
│   └───index.css
│   └───main.jsx
│   Dockerfile
│   .gitignore

nginx
│   nginx.conf
│   Dockerfile


### Контакты

telegram @olezha223 