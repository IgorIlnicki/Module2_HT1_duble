import sqlite3

def create_tables():
    # Підключення до бази даних SQLite (створюється, якщо вона не існує)
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()

    # Створити таблицю БД users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    fullname VARCHAR(100),
                    email VARCHAR(100) UNIQUE
                 )''')

    # Створити таблицю БД status
    c.execute('''CREATE TABLE IF NOT EXISTS status (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(50) UNIQUE
                 )''')

    # Вставити значення стану за замовчуванням
    c.execute("INSERT OR IGNORE INTO status (name) VALUES ('new')")
    c.execute("INSERT OR IGNORE INTO status (name) VALUES ('in progress')")
    c.execute("INSERT OR IGNORE INTO status (name) VALUES ('completed')")

    # Створити таблицю БД tasks
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title VARCHAR(100),
                    description TEXT,
                    status_id INTEGER,
                    user_id INTEGER,
                    FOREIGN KEY (status_id) REFERENCES status(id) ON DELETE SET NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                 )''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()