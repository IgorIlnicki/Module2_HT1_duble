import sqlite3

def get_users_and_task_counts():  # 14 Отримання списку користувачів і кількості їхніх завдань
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит для отримання користувачів і кількості їхніх завдань
    c.execute("""
        SELECT users.fullname, COUNT(tasks.id) AS task_count
        FROM users
        LEFT JOIN tasks ON users.id = tasks.user_id
        GROUP BY users.id
    """)
    users_and_task_counts = c.fetchall()
    conn.close()
    return users_and_task_counts

def get_users_and_tasks_in_progress():  # 13 # Отримання списку користувачів і їхніх завдань, які виконуються
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит для отримання користувачів і їхніх завдань, які виконуються <in progress>
    c.execute("""
        SELECT users.fullname, tasks.title, tasks.description
        FROM users
        INNER JOIN tasks ON users.id = tasks.user_id
        INNER JOIN status ON tasks.status_id = status.id
        WHERE status.name = 'in progress'
    """)
    users_and_tasks = c.fetchall()
    conn.close()
    return users_and_tasks

def get_tasks_without_description():  # 12 Отримання завдань, які не мають опису
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит для отримання завдань, які не мають опису.
    c.execute("""
        SELECT tasks.id, tasks.title, tasks.description, users.fullname, status.name AS status_name
        FROM tasks   
        JOIN users ON tasks.user_id = users.id
        JOIN status ON tasks.status_id = status.id
        WHERE description IS NULL OR description = ''
    """)
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_tasks_for_users_with_domain(domain): # 11 отримання завдань, призначених користувачам із певною доменною частиною електронної пошти
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит для отримання завдань, призначених користувачам із певною доменною частиною електронної пошти
    c.execute("""
        SELECT tasks.id, tasks.title, tasks.description, users.fullname, status.name AS status_name
        FROM tasks   
        JOIN users ON tasks.user_id = users.id
        JOIN status ON tasks.status_id = status.id
        WHERE users.email LIKE ?
    """, ('%@' + domain,))  # Використання % як символу підстановки для відповідності шаблону
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_task_count_by_status():  # 10 Отримати кількість завдань для кожного статусу
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит, щоб отримати кількість завдань для кожного статусу
    c.execute("""
        SELECT status.name, COUNT(tasks.id) AS task_count
        FROM status
        LEFT JOIN tasks ON tasks.status_id = status.id
        GROUP BY status.name
    """)
    task_counts = c.fetchall()
    conn.close()
    return task_counts

def update_username(user_id, new_fullname):  # 9 Оновлення імені (повного імені) певного користувача 
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит для оновлення імені певного користувача
    c.execute("""
        UPDATE users
        SET fullname = ?
        WHERE id = ?
    """, (new_fullname, user_id))
    conn.commit()
    conn.close()

def find_users_by_email(email):  # 8  знайти користувачів із певною електронною поштою
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит, щоб знайти користувачів із певною електронною поштою
    c.execute("""
        SELECT users.fullname
        FROM users
        WHERE email LIKE ?
    """, ('%' + email + '%',))  # Використання % як символу підстановки для відповідності шаблону
    users = c.fetchall()
    conn.close()
    return users

def delete_task(task_id):  #  7  видалення конкретного завдання за його ідентифікатором
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит для видалення конкретного завдання за його ідентифікатором
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def get_tasks_not_completed():  # 6  отримати завдання, статус яких не "виконано"
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит, щоб отримати завдання, статус яких не "виконано"
    c.execute("""
        SELECT tasks.id, tasks.title, tasks.description, users.fullname, status.name AS status_name
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        JOIN status ON tasks.status_id = status.id
        WHERE status_id != (
            SELECT id
            FROM status
            WHERE name = 'completed'
        )
    """)
    tasks = c.fetchall()
    conn.close()
    return tasks

def add_task(title, description, status_id, user_id): # 5 Додати нове завдання для конкретного користувача
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит, щоб вставити нове завдання
    c.execute("""
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES (?, ?, ?, ?)
    """, (title, description, status_id, user_id))
    conn.commit()
    conn.close()


def get_users_without_tasks(): # 4 отримати список користувачів, які не мають жодних завдань.
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит, щоб отримати список користувачів, які не мають жодних завдань.
    c.execute("""
        SELECT id, fullname
        FROM users
        WHERE id NOT IN (
            SELECT DISTINCT user_id
            FROM tasks
        )
    """)
    users = c.fetchall()
    conn.close()
    return users

def update_task_status(task_id, new_status):   # 3 запит для оновлення статусу певного завдання
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит для оновлення статусу певного завдання
    c.execute("""
        UPDATE tasks
        SET status_id = (
            SELECT id
            FROM status
            WHERE name = ?
        )
        WHERE id = ?
    """, (new_status, task_id))
    conn.commit()  # оновлюємо
    conn.close()

def get_tasks_by_status(status_name):  # 2  отримати завдання з певним статусом
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит, щоб отримати завдання з певним статусом
    c.execute("""
        SELECT tasks.id, tasks.title, tasks.description, users.fullname
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        WHERE tasks.status_id = (
            SELECT id
            FROM status
            WHERE name = ?
        )
    """, (status_name,))
    tasks = c.fetchall()
    conn.close()

    return tasks

def get_tasks_by_user_id(user_id):  # 1 отримати завдання певного користувача за його ідентифікатором
    conn = sqlite3.connect('datab.db')
    c = conn.cursor()
    # SQL-запит, щоб отримати завдання певного користувача за його ідентифікатором
    c.execute("""SELECT tasks.id, tasks.title, tasks.description, users.fullname, status.name AS status_name
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        JOIN status ON tasks.status_id = status.id
        WHERE tasks.user_id = ?
    """, (user_id,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def pripe_get_users_and_task_counts():  # 14
    users_and_task_counts = get_users_and_task_counts()
    if users_and_task_counts:
        print("Користувачі та кількість їх завдань:")
        # for user in users_and_task_counts:
        #     print("User: {}, Task Count: {}".format(user[0], user[1]))
        i = 0
        for user in users_and_task_counts:
            print(f"{i+1}.   Ім'я користувача: {user[0]};   Кількість завдань: {user[1]}.")
            i +=1
    else:
        print("No users found with tasks.")


def pripe_get_users_and_tasks_in_progress():  # 13 
    users_and_tasks = get_users_and_tasks_in_progress()
    if users_and_tasks:
        print("Користувачі та їхні завдання зі статусом <in progress>:")
        i = 0
        for task in users_and_tasks:
            print(f"{i+1}.\n   Ім'я користувача: {task[0]}")
            print(f"   Назва завдання: {task[1]} \n   Опис задачі:\n{task[2]}")
            i +=1
    else:
        print("Не знайдено користувачів із незавершеними завданнями.")

def pripe_get_tasks_without_description():  # 12
    tasks = get_tasks_without_description()
    if tasks:
        print("Завдання без опису:")
        i = 0
        for task in tasks:
            print(f"{i+1}.\n   Номер задачі: {task[0]}")
            print(f"   Назва задачі: {task[1]} \n   Опис задачі:\n{task[2]}")
            print(f"Ім'я користувача: {task[3]}\n   Статус: {task[4]}")
            i +=1
    else:
        print("Не знайдено завдань без опису.")

def pripe_get_tasks_for_users_with_domain(args):  # 11
    # domain = 'example.com'
    domain = args[0]
    tasks = get_tasks_for_users_with_domain(domain)
    if tasks:
        print("Завдання, призначені користувачам із доменом електронної пошти '{}':".format(domain))
        i = 0
        for task in tasks:
            print(f"{i+1}.\n   Номер задачі: {task[0]}")
            print(f"   Назва задачі: {task[1]} \n   Опис задачі:\n{task[2]}")
            print(f"Ім'я користувача: {task[3]}\n   Статус: {task[4]}")
            i +=1
    else:
        print("Не знайдено завдань, призначених користувачам із доменом електронної пошти '{}'.".format(domain))

def pripe_get_task_count_by_status():  # 10
    task_counts = get_task_count_by_status()
    if task_counts:
        print("Кількість завдань для кожного статусу:")
        for status, count in task_counts:
            print("Статус: <{}>, кількість завдань: {}".format(status, count))
    else:
        print("No tasks found.")

def pripe_update_username(args):  # 9
    user_id = args[0]
    new_fullname = " ".join([args[1], args[2]])
    update_username(user_id, new_fullname)
    print("Ім’я оновлено для користувача з ідентифікатором {}.".format(user_id))
    print(f"Нове ім’я: {new_fullname}")

def pripe_find_users_by_email(args):  # 8
    email = args[0]
    users = find_users_by_email(email)
    if users:
        print("Користувачі з адресою електронної пошти, яка містить <{}>:".format(email))
        i = 0
        for user in users:
            print(f"{i+1}.  Користувач: {user[0]}")
            i +=1
    else:
        print("Не знайдено користувачів із електронною поштою, що містить <{}>.".format(email))

def pripe_delete_task(args):  # 7
    task_id = args[0] 
    delete_task(task_id)
    print("Завдання з ідентифікатором {} видалено.".format(task_id))

def pripe_get_tasks_not_completed():   # 6
    tasks = get_tasks_not_completed()
    if tasks:
        print("Завдання, статус яких не є <completed>:")
        # for task in tasks:
        #     print(task)
        i = 0
        for task in tasks:
            print(f"{i+1}.\n   Номер задачі: {task[0]}")
            print(f"   Назва задачі: {task[1]} \n   Опис задачі:\n{task[2]}")
            print(f"Ім'я користувача: {task[3]}\n   Статус: {task[4]}")
            i +=1
    else:
        print("Не знайдено завдань зі статусом, відмінним від <completed>.")

def pripe_add_task():  # 5
    title = "Complete project"
    description = "Finish the final report and submit it by Friday."
    status_id = 1  # Тут можна замінити 1 відповідним ідентифікатором статусу
    user_id = 1  # Тут можна замінити 1 ідентифікатором конкретного користувача, для якого призначено завдання
    add_task(title, description, status_id, user_id)
    print("Додано нове завдання для користувача з ID {}.".format(user_id))

def pripe_get_users_without_tasks():   # 4
    users = get_users_without_tasks()
    if users:
        print("Користувачі, які не мають жодних завдань:")
        # for user in users:
        #     print(user)
        i = 0
        for user in users:
            print(f"{i+1}.  Номер користувача: {user[0]}.   Ім'я користувача: {user[1]}")
            i +=1
    else:
        print("У всіх користувачів є завдання.")

def pripe_update_task_status(args):   # 3
    task_id = int(args[0]) 
    if len(args) == 3:
        new_status = "in progress"
    else:
        new_status = args[1]
    print(f"  task_id = {task_id} new_status = {new_status}")
    update_task_status(task_id, new_status)
    print("Статус завдання з ідентифікатором {} змінено на: '{}'.".format(task_id, new_status))

def pripe_execute_by_status(args):  #2
    status_name = args[0]
    tasks = get_tasks_by_status(status_name)
    if tasks:
        print("Вибрати завдання зі статусом: {}: ".format(status_name))  
        i = 0
        for task in tasks:
            #print(f"   task: {task}")
            print(f"{i+1}.\n   Номер задачі: {task[0]}")
            print(f"   Назва задачі: {task[1]} \n   Опис задачі:\n{task[2]} \n   Ім'я користувача: {task[3]}")
            i +=1
    else:
        print("No tasks found for user with ID {}.".format(status_name))

def pripe_get_tasks_by_user_id(args):   #1
    user_id = args[0]   # конкретний ідентифікатор користувача, для якого треба отримати завдання
    tasks = get_tasks_by_user_id(user_id)
    if tasks:
        print("Завдання для користувача з Id: {}: ".format(user_id))  
        i = 0
        for task in tasks:
            if i == 0:
                print(f"Ім'я користувача: {task[3]}")
            print(f"{i+1}.\n   Номер задачі: {task[0]}")
            print(f"   Назва задачі: {task[1]} \n   Опис задачі:\n{task[2]} \n   Статус: {task[4]}")
            i +=1

    else:
        print("No tasks found for user with ID {}.".format(user_id))

def parse_input(user_input): # ввод команди та аргументів
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    print("Ласкаво просимо до Бази Даних! Формат команд:\nclose або exit\nSelect [user_id]\nExecute [status_name]\nUpdate [task_id] [new_status]\nGet") 
    print("Get_users_without_tasks\nAdd_task\nGet_tasks_not_completed\nDelete_task [task_id]\nFind_by_email [email]")
    print("Update_username [user_id] [new_name]\nGet_task_count_by_status\nget_tasks_for_users_with_domain [domain]")
    print("Get_tasks_without_description\nGet_users_and_tasks_in_progress\nGet_users_and_task_counts")
    while True: 
            user_input = input("Введіть команду: ")
            command, *args = parse_input(user_input)
            # print(f"   cmd = {command}    args[0] = {args[0]}")
            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "select":  # 1
               pripe_get_tasks_by_user_id(args)
            elif command == "execute":  # 2
               pripe_execute_by_status(args)
            elif command == "update":  # 3
               pripe_update_task_status(args)
            elif command == "get_users_without_tasks":  # 4
                pripe_get_users_without_tasks()
            elif command == "add_task":  # 5
                pripe_add_task()
            elif command == "get_tasks_not_completed":  # 6
                pripe_get_tasks_not_completed()
            elif command == "delete_task":   # 7
                pripe_delete_task(args)
            elif command == "find_by_email":  # 8
                pripe_find_users_by_email(args)
            elif command == "update_username":  # 9
                pripe_update_username(args)
            elif command == "get_task_count_by_status":  # 10
                pripe_get_task_count_by_status()
            elif command == "get_tasks_for_users_with_domain":  # 11
                pripe_get_tasks_for_users_with_domain(args)
            elif command == "get_tasks_without_description":  # 12
                pripe_get_tasks_without_description()
            elif command == "get_users_and_tasks_in_progress":  # 13
                pripe_get_users_and_tasks_in_progress()
            elif command == "get_users_and_task_counts":  # 14
                pripe_get_users_and_task_counts()

if __name__ == "__main__":
    main()