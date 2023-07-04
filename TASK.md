### Task

Создать чат-бот в тг на python (aiogram), который будет выполнять задачу по отправке поста из админ панели .

Админ панель:

Нужно сделать на Fast api, в ней должно быть 2 страницы:

1. БД пользователей (никнейм тг (или уникальный id если нет никнейма), время и дата запуска бота пользователем ( дата
   формата 28.06.2023, время 24-часовое (12:14), часовой пояс - мск)).

2. Реализация страницы с возможностью отправки поста (окно для текста (можно в html формате), реализовать возможность
   прикрепления фото/видео к посту.

### 04.07.2023

1. В .env.example указаны не все переменные, которые используются в коде. Например, HOST для gunicorn.

2. В docker-compose используется образ coolworldocker/bot_admin_service:latest вместо билда из исходников

3. При установке пакетов ошибка: Error: pg_config executable not found. Нужно убрать из requirements.txt psycopg2 и
   оставить psycopg2-binary

4. В main.py функция start_polling_bot, которая нигде не используется

5. Вместо from bot_admin_service import crud, schemas нужно использовать  
   import bot_admin_service.crud as crud, import bot_admin_service.schemas as schemas