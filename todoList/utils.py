import sqlite3
from datetime import datetime


class SQLiteDB(object):

    def __init__(self, db):
        try:
            self.client = sqlite3.connect(db, isolation_level=None, check_same_thread=False)
            self.cur = self.client.cursor()
        except Exception as e:
            raise Exception(e.args)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(SQLiteDB, cls).__new__(cls)
        return cls._instance

    def __del__(self):
        try:
            self.cur.close()
            self.client.close()
        except Exception as e:
            raise Exception(e.args)

    def fetch_all(self, table, is_delete):
        try:
            self.cur.execute("select id, content from {} where is_delete={}".format(table, is_delete))
        except Exception as e:
            raise Exception(e.args)

        yield from self.cur.fetchall()

    def fetch_one(self, table, id):
        try:
            self.cur.execute("select is_delete from {} where id={}".format(table, id))
        except Exception as e:
            raise Exception(e.args)

        return self.cur.fetchone()

    def update(self, table, id, is_delete):
        try:
            self.cur.execute("update {} set is_delete={} where id={}".format(table, is_delete, id))
            self.client.commit()
        except Exception as e:
            raise Exception(e.args)

        return "200"

    def insert(self, table, content, is_delete=False):
        try:
            now = datetime.now()
            self.cur.execute(
                """insert into {} (content, is_delete, create_time) values ('{}',{}, '{}')""".format(table, content,
                                                                                                     is_delete, now))
            self.client.commit()
        except Exception as e:
            raise Exception(e.args)

        return "200"

    def raw(self, sql):
        try:
            self.cur.execute(sql)
            if 'select' in sql:
                return self.cur.fetchall()
            else:
                self.client.commit()
                return '200'
            
        except Exception as e:
            print(e.args)
