#coding=utf-8

import MySQLdb
import MySQLdb.cursors

class DataBase(object):
    def __init__(self):
        self.user = 'root'
        self.pass_word = '85607505rzd?'
        self.db_name = 'test'
        self.db = MySQLdb.connect('localhost', self.user, self.pass_word, self.db_name, charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.db.cursor()

    def insert_into_db(self, name, stars):
        sql = 'INSERT INTO DOUBANMOVIES(name, stars)' \
              'VALUES("%s", %f)' % (name, stars)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception, e:
            print str(e)
            self.db.rollback()

    def query_user(self, account, password):
        sql = 'SELECT * FROM users where account="%s"' % account
        self.cursor.execute(sql)
        rs = self.cursor.fetchone()
        return rs

    def close(self):
        self.db.close()

    def create_users_table(self):
        sql = """CREATE TABLE DouBanMovies (
                 id INT UNSIGNED AUTO_INCREMENT,
                 name VARCHAR(25),
                 stars FLOAT(3, 2),
                 PRIMARY KEY(id) )"""
        self.cursor.execute(sql)
        self.db.close()


if __name__ == '__main__':
    database = DataBase()
    rs = database.query_user('2016141462307', '85607505rzd')
    if rs:
        print rs['name']
    else:
        print '账号不存在'
