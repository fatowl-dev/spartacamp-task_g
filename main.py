import sqlite3
from db_controller import DBController


def main():
    db = DBController('data.db')

    check_db(db)    # データベースが初期化されてなかったら初期化

    display_welcome_message()

    while True:
        cmd = input('Your command > ')
        cmd = cmd.upper()
        if cmd == 'S':
            show_all_users_info(db)
            print()
        elif cmd == 'A':
            add_new_user(db)
            print()
        elif cmd == 'F':
            find_user(db)
            print()
        elif cmd == 'D':
            delete_user(db)
            print()
        elif cmd == 'E':
            edit_user(db)
            print()
        elif cmd == 'Q':
            break
        else:
            display_help()
            print()

    print('Bye!')


# ユーザー名入力 エラーでNoneを返す
def input_user_name(suffix=''):
    name = input(f'New user name ({suffix})> ')
    if len(name) == 0:
        print("User name can't be blank")
        return None

    if len(name) > 20:
        print('User name is too long(maximun is 20 characters)')
        return None

    return name


# ユーザー年齢入力 エラーでNoneを返す
def input_user_age(suffix=''):
    str_age = input(f'New user age ({suffix}) > ')

    if not str_age.isdigit():
        print('Age is not positive integer')
        return None

    age = int(str_age)
    if age < 0:
        print('Age is not positive integer')
        return None

    if age > 120:
        print('Age is grater than 120')
        return None

    return age


def create_table(db: DBController):
    with db.open():
        db.execute('create table users(name text, age integer)')
        db.commit()


# データベースが初期化されているかしらべて
# 必要なら初期化する
def check_db(db):
    with db.open():
        try:
            db.execute('select * from users')
        except sqlite3.OperationalError:
            print('Creating new DB')
            create_table(db)


# ユーザーが存在するか調べる
def user_is_exist(db: DBController, user_name: str):
    sql = "select name from users where name = ?"
    with db.open():
        db.execute(sql, [user_name])
        result = db.fetchall()

    return len(result) != 0


def display_user_record(row: tuple):
    print(f'Name: {row[0]} Age: {row[1]}')


def show_all_users_info(db):
    with db.open():
        sql = 'select * from users'
        db.execute(sql)
        user_records = db.fetchall()
        for row in user_records:
            display_user_record(row)


def add_new_user(db):
    name = input_user_name()
    if name is None:
        return

    age = input_user_age()
    if age is None:
        return

    if user_is_exist(db, name):
        print(f'Duplicated user name {name}')
        return

    with db.open():
        sql = 'insert into users(name, age) values(?, ?)'
        db.execute(sql, (name, age))
        db.commit()

    print(f'Add new user: {name}')


def find_user(db):
    user_name = input('User name > ')
    sql = 'select * from users where name = ?'
    with db.open():
        db.execute(sql, (user_name,))
        user_records = db.fetchall()
    if len(user_records) == 0:
        print(f'Sorry, {user_name} is not found')
        return
    for row in user_records:
        display_user_record(row)


def delete_user(db):
    user_name = input('User name > ')
    find_sql = 'select * from users where name = ?'
    delete_sql = 'delete from users where name = ?'
    with db.open():
        db.execute(find_sql, (user_name,))
        user_records = db.fetchall()

        if len(user_records) == 0:
            print(f'Sorry, {user_name} is not found')
            return

        db.execute(delete_sql, (user_name,))
        db.commit()
        print(f'User {user_name} is deleted')


def edit_user(db: DBController):
    user_name = input('User name > ')
    find_sql = 'select * from users where name = ?'
    edit_sql = 'update users set name = ?, age = ? where name = ?'
    with db.open():
        db.execute(find_sql, (user_name,))
        user_records = db.fetchall()

        if len(user_records) == 0:
            print(f'Sorry, {user_name} is not found')
            return

        age = user_records[0][1]

    new_user_name = input_user_name(user_name)
    if new_user_name is None:
        return
    new_age = input_user_age(str(age))
    if new_age is None:
        return

    with db.open():
        db.execute(edit_sql, [new_user_name, new_age, user_name])
        db.commit()

    print(f'Update user: {new_user_name}')


def display_welcome_message():
    message = """===== Welcome to CRM Application =====
[S]how: Show all users info
[A]dd: Add new user
[F]ind: Find user
[D]elete: Delete user
[E]dit: Edit user
[Q]uit: Quit this app
======================================"""
    print(message)


def display_help():
    print('[S]: Show all users info  [A]: Add new user  [F]: Find user\n'
          '[D]: Delete user  [E]: Edit user  [Q]: Quit this app')


if __name__ == '__main__':
    main()
