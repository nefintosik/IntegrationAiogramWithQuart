# IntegrationAiogramWithQuart
Интеграция Aiogram с Quart на Python

# Инструкция
## Установка
1. Установите Aiogram
```pip install aiogram==2.25.1```
2. Установите Quart
```pip install quart==0.19.6```
3. Установите DotEnv
```pip install python-dotenv```
4. Установите aiosqlite
```pip install aiosqlite==0.20.0```
## Настройка
5. Скачайте проект и создайте файл .env
6. Добавьте в файл .env токен бота, пример: (TOKEN=ваш_токен)
7. Чтобы узнать chat_id группы добавьте бота в группу: [тык](https://t.me/LeadConverterToolkitBot), после в чат группы напишите команду /get_chat_id и вам выведтся chat_id вашей группы (скопируйте его)
8. Добавьте в файл .env chat_id группы, пример: (GROUP_CHAT_ID=-123132131)
## Запуск
9. Запустите весь проект ```app.py``` и перейдите на сайт который вывыдется в консоль
