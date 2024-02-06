#!./venv/bin/python

import sqlite3, iofunctions, requests, urllib3
from os import path
from app.models import User, Notification, Rule
from app import db
from flask import jsonify
from datetime import datetime
from symbols import *


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class App_db:
    def __init__(self, database):
        self.database = database

    def connect(self, database):
        current_folder = path.dirname(path.realpath(__file__))
        database_path = path.join(current_folder, "app/db/" + database)
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        self.database = database
        return connection

    def get(self, field='all', value=None):
        databases = [users, notifications, rules]
        database = self.database
        if database not in databases:
            raise ValueError("Invalid model. Expected one of: %s" % databases)
        result=""
        if database == users:
            try:
                if field == id:
                    result = User.query.filter_by(id=value).first()
                if field == username:
                    result = User.query.filter_by(username=value).first()
                if field == email:
                    result = User.query.filter_by(email=value).first()
                if field == phone:
                    result = User.query.filter_by(phone=value).first()
                if field == 'all':
                    result = User.query.all()
            except Exception as e:
                result = e

        if database == notifications:
            try:
                if field == id:
                    result = Notification.query.filter_by(id=value).first()
                if field == user_id:
                    result = Notification.query.filter_by(user_id=value).all()
                if field == 'all':
                    result = Notification.query.all()
            except Exception as e:
                result = e

        if database == rules:
            try:
                if field == id:
                    result = Rule.query.filter_by(id=value).first()
            except Exception as e:
                result = e

        return result

    def update(self, id=None, key=None, value=None):
        try:
            if self.database == notifications:
                db.session.query(Notification).filter_by(id=id).update({key: value})
                db.session.commit()
            if self.database == users:
                db.session.query(User).filter_by(id=id).update({key: value})
                db.session.commit()
            if self.database == rules:
                db.session.query(Rule).filter_by(id=id).update({key: value})
                db.session.commit()
            ans = 'ok'
        except Exception as e:
            return e
        return ans

class FullPVList:
    def __init__(self):
        pass

    def __get_connection(self):
        database_path = iofunctions.fromcfg('FULLPVLIST', 'db')
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def getlist(self):
        connection = self.__get_connection()
        db = connection.execute('SELECT pv FROM fullpvlist_db').fetchall()
        fullpvlist = []
        for row in db:
            for i in row:
                fullpvlist.append(i)
        return fullpvlist

    def update(self):
        try:
            current_folder = iofunctions.current_path()
            schema = iofunctions.fromcfg('FULLPVLIST', 'schema')
            schema_path = path.join(current_folder, schema)

            url = iofunctions.fromcfg('EPICS_SERVER','getallpvs')
            r = requests.get(url, allow_redirects=True, verify=False)

            if r.status_code == 503:
                raise Exception('Error, could not get PVs from server.')
            else:
                connection = self.__get_connection()

                with open(schema_path) as f:
                    connection.executescript(f.read())

                cur = connection.cursor()

                fullpvlist = r.text.replace('"','').replace('[','').replace(']','').split(',')

                for pv in fullpvlist:
                    cur.execute("INSERT INTO fullpvlist_db (pv) VALUES (?)", (pv,))
                connection.commit()
                connection.close()
        except Exception as e:
            return e


# ls = datetime.strptime('2023-12-31 22:00', '%Y-%m-%d %H:%M')
# notification_db = App_db(notification_db)
# print(notification_db.get(id, 28))
# users_db = App_db(users)
# print(users_db.get(id, 2))
# user_db = App_db(users)
# user_db.update(2, email, 'rone.castro@lnls.br')
# print(db.session.query(User).all())
# f = FullPVList()
# print(f.update())
