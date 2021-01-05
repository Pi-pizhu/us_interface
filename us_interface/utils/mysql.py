import pymysql
from ..config.global_config import GlobalConfig


class Mysql:

    def __init__(self):
        gl_config = GlobalConfig()
        host = gl_config.get_global_variable("mysql", "host")
        user = gl_config.get_global_variable("mysql", "user")
        password = gl_config.get_global_variable("mysql", "password")
        database = gl_config.get_global_variable("mysql", "database")
        port = gl_config.get_global_variable("mysql", "port")
        self.db = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
        # 创建游标
        self.cursor = self.db.cursor()

    def select_all_exec(self, sql_statement):
        select_ex = sql_statement
        try:
            self.cursor.execute(select_ex)
            return self.cursor.fetchall()
        except Exception as error:
            raise error

    def select_exec(self, sql_statement):
        select_ex = sql_statement
        try:
            self.cursor.execute(select_ex)
            return self.cursor.fetchone()
        except Exception as error:
            raise error

    def inster_exec(self, sql_statement):
        inster_ex = sql_statement
        try:
            self.cursor.execute(inster_ex)
            self.db.commit()
            return self.cursor.fetchone()
        except Exception as error:
            self.db.rollback()
            raise error

    def update_exec(self, sql_statement):
        update_ex = sql_statement
        try:
            self.cursor.execute(update_ex)
            self.db.commit()
            return self.cursor.fetchone()
        except Exception as error:
            self.db.rollback()
            raise error