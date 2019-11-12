import sqlite3

DB_NAME = 'data.db'


def main():
    check_db()

    display_welcome_message()

    while True:
        cmd = input('Your command > ')
        cmd = cmd.upper()
        if cmd == 'S':
            show_all_users_info()
        elif cmd == 'A':
            add_new_user()
        elif cmd == 'Q':
            break
        else:
            display_help()

    print('Bye!')


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    sql = 'create table users(name text, age int)'
    cur.execute(sql)
    conn.commit()
    conn.close()


def check_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute('select * from users')
    except sqlite3.OperationalError:
        print('Creating new DB')
        create_table()
    finally:
        conn.close()


def show_all_users_info():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    sql = 'select * from users'
    cur.execute(sql)
    user_records = cur.fetchall()
    conn.close()
    for row in user_records:
        print(f'Name: {row[0]} Age: {row[1]}')


def add_new_user():
    name = input('New user name > ')
    age = int(input('New user age > '))
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    sql = f'insert into users(name, age) values(?, ?)'
    cur.execute(sql, (name, age))
    conn.commit()
    conn.close()


def display_welcome_message():
    message = """===== Welcome to CRM Application =====
[S]how: Show all users info
[A]dd: Add new user
[Q]uit: Quit this app
======================================"""
    print(message)


def display_help():
    print('[S]: Show all users info  [A]: Add new user  [Q]: Quit this app')


if __name__ == '__main__':
    main()

