#!./venv/bin/python
import os, sys, sqlite3

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
upper_parent_dir_path = os.path.abspath(os.path.join(parent_dir_path, os.pardir))
sys.path.insert(0, upper_parent_dir_path)

from db import App_db, User


user1 = {"username":"rone.castro", "email":"rone.castro@lnls.br", "phone":"+5519997397443", "password":"rone"}

def dict_from_row(row):
    return dict(zip(row.keys(), row))

old_db_name = 'app_bkp.db'
current_folder = os.path.dirname(os.path.realpath(__file__))
database_path_old = os.path.join(current_folder, old_db_name)
conn_old = sqlite3.connect(database_path_old)
conn_old.row_factory = sqlite3.Row
rows_old = conn_old.execute("SELECT * FROM notifications").fetchall()

new_db_name = 'app.db'
database_path_new = os.path.join(current_folder, new_db_name)
print(database_path_new)
conn_new = sqlite3.connect(database_path_new)
conn_new.row_factory = sqlite3.Row
cur = conn_new.cursor()
rows_new = conn_new.execute("SELECT * FROM notifications").fetchall()

def update_notifications():
    for row in rows_old:
        notification_original = (row['notification'])
        notification_new = notification_original.replace('"pv":', '"pv0:"')
        notification_new = notification_new.replace('"rule":', '"rule0"')
        notification_new = notification_new.replace('"limit":', '"limit0"')
        notification_new = notification_new.replace('"limitLL":', '"limitiLL0":')
        notification_new = notification_new.replace('"limitLU":', '"limitLU0"')
        notification_new = notification_new.replace('"subrule":', '"subrule0":')
        print(row.keys())


        # cur.execute('DELETE FROM users (username, email, phone, password_hash)VALUES (?, ?, ?, ?)', (username, email, phone, password_hash))
        # conn_new.commit()


        # ans = dict_from_row(row)
        # print(ans)
        # cur.execute('INSERT INTO users (username, email, phone, password_hash)VALUES (?, ?, ?, ?)', (username, email, phone, password_hash))
        # conn_new.commit()
        # ans = dict_from_row(row)
        # print(ans)

# user_db = App_db('users')
# print('db: ', user_db.get())
# usr = user_db.get(field='id', value=2)
# print(usr.check_password(password='rone'))
# deletedb()
update_notifications()
