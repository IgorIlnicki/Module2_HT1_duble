from faker import Faker
import sqlite3

fake = Faker()

def populate_users(conn, num_users):
    c = conn.cursor()
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.email()
        c.execute("INSERT INTO users (fullname, email) VALUES (?, ?)", (fullname, email))
    conn.commit()

def populate_tasks(conn, num_tasks):
    c = conn.cursor()
    for _ in range(num_tasks):
        title = fake.text(max_nb_chars=100)
        description = fake.text()
        status_id = fake.random_int(min=1, max=3)  
        user_id = fake.random_int(min=1, max=20)  
        c.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
                  (title, description, status_id, user_id))
    conn.commit()

def main():
    conn = sqlite3.connect('datab.db')

    num_users = 20  # Кількість користувачів для створення
    num_tasks = 30  # Кількість завдань для створення

    populate_users(conn, num_users)
    populate_tasks(conn, num_tasks)

    conn.close()
    print("Data seeding completed!")

if __name__ == "__main__":
    main()