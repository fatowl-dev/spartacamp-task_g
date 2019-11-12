import sqlite3
from db_controller import DBController


def main():
    db = DBController('data.db')
    check_db(db)

    display_welcome_message()

    while True:
        cmd = input('Your command > ')
        cmd = cmd.upper()
        if cmd == 'S':
            show_all_users_info(db)
        elif cmd == 'A':
            add_new_user(db)
        elif cmd == 'Q':
            break
        else:
            display_help()

    print('Bye!')


def create_table(db: DBController):
    with db.open():
        db.execute('create table users(name text, age int)')
        db.commit()


def check_db(db):
    with db.open():
        try:
            db.execute('select * from users')
        except sqlite3.OperationalError:
            print('Creating new DB')
            create_table(db)


def show_all_users_info(db):
    with db.open():
        sql = 'select * from users'
        db.execute(sql)
        user_records = db.fetchall()
        db.close()
        for row in user_records:
            print(f'Name: {row[0]} Age: {row[1]}')


def add_new_user(db):
    name = input('New user name > ')
    age = int(input('New user age > '))
    with db.open():
        sql = 'insert into users(name, age) values(?, ?)'
        db.execute(sql, (name, age))
        db.commit()


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

