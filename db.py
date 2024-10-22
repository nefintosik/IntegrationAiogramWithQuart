import sqlite3


# Функция для создания таблицы
def init_db():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    
    # Создаем таблицу для хранения данных формы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS form_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            message TEXT NOT NULL,
            tg TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()


# Инициализируем базу данных при запуске
init_db()
