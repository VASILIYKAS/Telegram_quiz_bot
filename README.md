# Викторина для VK и Telegram

Бот-викторина, который задаёт случайные вопросы и проверяет ответы пользователей.  
Поддерживает работу как во ВКонтакте, так и в Telegram.  
Хранение состояния (текущих вопросов и счёта) реализовано через Redis.

<p align="center">
  <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnVwNzlmYTlsMmk2MjR2YnUzZ3ByYjQ2MDJ2aHdiN2QxNTNocTA4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YdXQlIYxcipNlWqPZM/giphy.gif" alt="Гифка">
</p>
## Оглавление

- [Установка](#установка-и-запуск)
    - [Переменные окружения](#переменные-окружения)
- [Запуск ботов](#запуск-ботов)
- [Цель проекта](#цель-проекта)

## Установка

- Python 3.13 должен быть установлен
- Скачайте код:
```bash
git clone https://github.com/VASILIYKAS/Telegram_quiz_bot.git
```
- Рекомендуется создать виртуальное окружение. Для этого нужно выполнить команду: 
```bash
python -m venv .venv
```
- Активируйте виртуальное окружение:
```bash
.venv\Scripts\activate    # Для Windows
source .venv/bin/activate # Для Linux
```
- Затем установите все необходимые библиотеки, сделать это можно командой: 
```bash
pip install -r requirements.txt
```

## Переменные окружения

Создайте файл .env в корне проекта со следующими переменными:
```ini
TG_BOT_TOKEN=ваш_токен_телеграм_бота
REDIS_DB_HOST=ваш_адрес_бд_redis
REDIS_DB_PASSWORD=ваш_пароль_от_бд_redis
REDIS_DB_PORT=порт_бд_redis
VK_BOT_TOKEN=ваш_токен_вк
QUESTIONS_FILES=имя_файла_с_вопросами
```

- `TG_BOT_TOKEN` - можно получить у отца ботов в телеграм [ссылка](https://t.me/BotFather)

- `VK_BOT_TOKEN` - для получения VK токена нужно создать [сообщество](https://vk.com/groups) в ВК (если оно не создано), зайти в "Управление" -> "Дополнительно" -> "Работа с API" -> "Создать ключ"

- `REDIS_DB_HOST` - можно получить на сайте [Redis](https://cloud.redis.io/#/login). 
    - Зарегистрируйтесь и зайди в Redis. 
    - В меню слева нажмите "Databases" и выбирете свою бд.
    - На вкладке "General" найдите "Public endpoint", это и есть ваш адрес бд, в конце после двоеточия идёт порт.   

- `REDIS_DB_PASSWORD` - можно получить на сайте [Redis](https://cloud.redis.io/#/login).
    - Зарегистрируйтесь и зайди в Redis. 
    - В меню слева нажмите "Databases" и выбирете свою бд.
    - На вкладке "Security" будет ваш пароль "Default user password"

- `REDIS_DB_PORT` - можно получить на сайте [Redis](https://cloud.redis.io/#/login). 
    - Зарегистрируйтесь и зайди в Redis. 
    - В меню слева нажмите "Databases" и выбирете свою бд.
    - На вкладке "General" найдите "Public endpoint", это и есть ваш адрес бд, в конце после двоеточия идёт порт. 

- `QUESTIONS_FILES` - в папке проекта "questions" есть несколько файлов с вопросами. По умолчанию используется "anime10.txt". Если хотите изменить вопросы укажите название файла с расширением. Например:
```python
QUESTIONS_FILES=6pers15.txt
```
Можете создать свой файл с вопросами, формат должен быть:
```txt
Вопрос 1:
ваш вопрос.

Ответ:
ваш ответ.

...

Вопрос 15:
ваш вопрос.

Ответ:
ваш ответ.
```

## Запуск ботов

Запустите каждый бот в отдельном терминале:
Для Telegram:
```bash
python -m tg_bot.bot
```

Для ВКонтакте:
```bash
python -m vk_bot.bot
```

## Цель проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
    
