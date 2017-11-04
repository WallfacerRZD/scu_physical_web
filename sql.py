# coding=utf-8

import MySQLdb
import MySQLdb.cursors
from datetime import datetime


class DataBase(object):
    def __init__(self):
        self.user = 'root'
        self.pass_word = '85607505rzd?'
        self.db_name = 'test'
        self.db = MySQLdb.connect('localhost', self.user, self.pass_word, self.db_name, charset='utf8')
        self.cursor = self.db.cursor()

    def __del__(self):
        self.close()

    def insert_users(self, account, password, name):
        sql = u"""INSERT INTO USERS(account, password, name)
                            VALUES('%s', '%s', '%s')""" \
              % (account, password, name)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception, e:
            print e
            self.db.rollback()
            # finally:
            #     self.close()

    def insert_datas(self, account, datas, term, assessment, suggestion):
        sql = u"""INSERT INTO TEST_DATAS
                  (account, 身高, 体重, 肺活量, 跳远, 50米, 台阶, 
                   800米, 1000米, 仰卧起坐, 引体向上, 坐位体前屈, 
                   握力, 视力左, 视力右, 学期, 总评, 需要改进)
              VALUES("%s", "%s", "%s", "%s", "%s", "%s", 
                     "%s", "%s", "%s", "%s", "%s", "%s", 
                     "%s", "%s", "%s", "%s", "%s", "%s")""" \
              % (account, datas[0], datas[1], datas[2], datas[3], datas[4],
                 datas[5], datas[6], datas[7], datas[8], datas[9], datas[10],
                 datas[11], datas[12], datas[13], term, assessment, suggestion)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception, e:
            print str(e)
            self.db.rollback()

    def insert_scores(self, account, scores, term):
        sql = u"""INSERT INTO SCORES
                  (account, 身体素质, 肺活量, 跳远, 50米, 台阶, 
                   800米, 1000米, 仰卧起坐, 引体向上, 坐位体前屈, 
                   握力, 视力左, 视力右, 学期)
              VALUES("%s", "%s", "%s", "%s", "%s", "%s", 
                     "%s", "%s", "%s", "%s", "%s", "%s", 
                     "%s", "%s", "%s")""" \
              % (account, scores[0], scores[1], scores[2], scores[3], scores[4],
                 scores[5], scores[6], scores[7], scores[8], scores[9], scores[10],
                 scores[11], scores[12], term)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception, e:
            print str(e)
            self.db.rollback()
            print self.db

    def insert_cancels(self, account, reason):
        sql = '''INSERT INTO cancels (id, reason)
                VALUES("%s", "%s")''' % (account, reason)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception, e:
            print str(e)
            self.db.rollback()

    def insert_reservation(self, account, date, place, test_id):
        sql = """INSERT INTO reservations (id, date, place, test_id)
                 VALUES("%s", "%s", "%s", "%s")""" % (account, date, place, test_id)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception, e:
            print str(e)
            self.db.rollback()

    def delete_reservation(self, account):
        sql = """delete from reservations where id='%s'""" % account
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception, e:
            print str(e)
            self.db.rollback()

    def increase_tests_capacity(self, _id):
        sql = """UPDATE tests SET capacity = capacity + 1, stdNum = stdNum - 1 WHERE id=%s""" % _id
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception, e:
            print str(e)
            self.db.rollback()

    def decrease_tests_capacity(self, _id):
        sql = """UPDATE tests SET capacity = capacity - 1, stdNum = stdNum + 1 WHERE id=%s""" % _id
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception, e:
            print str(e)
            self.db.rollback()

    def query_datas(self, account):
        sql = "SELECT * FROM TEST_DATAS WHERE ACCOUNT=%s" % account
        self.cursor.execute(sql)
        rs = self.cursor.fetchall()
        # rs = ((身高, 体重, 肺活量, 跳远, 50米, 台阶,
        #        800米, 1000米, 仰卧起坐, 引体向上, 坐位体前屈,
        #        握力, 视力左, 视力右, 学期, 总评, 需要改进),
        # (),
        # .....)
        return rs

    def query_scores(self, account):
        sql = "SELECT * FROM SCORES WHERE ACCOUNT=%s" % account
        self.cursor.execute(sql)
        rs = self.cursor.fetchall()
        # rs = ((身高, 体重, 肺活量, 跳远, 50米, 台阶,
        #        800米, 1000米, 仰卧起坐, 引体向上, 坐位体前屈,
        #        握力, 视力左, 视力右, 学期, 总评, 需要改进),
        # (),
        # .....)
        return rs

    #
    def query_user(self, account, password):
        sql = 'SELECT * FROM users where account="%s" and password="%s"' % (account, password)
        self.cursor.execute(sql)
        rs = self.cursor.fetchone()
        return rs

    # ((日期, 地点, 容量, 学生人数), )
    def query_tests(self):
        sql = 'SELECT * FROM TESTS WHERE capacity > stdNum'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def query_tests_by_id(self, _id):
        sql = "SELECT * FROM TESTS WHERE id='%s'" % _id
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    # (日期, 地点)
    def query_reservations(self, account):
        sql = 'SELECT date, place FROM RESERVATIONS WHERE ID="%s"' % account
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        result = result if result else ('无', '无')
        return result

    def query_cancel(self, account):
        sql = 'SELECT * FROM cancels WHERE id="%s"' % account
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def get_tests_id(self, account):
        sql = """SELECT test_id FROM reservations WHERE id=%s""" % account
        self.cursor.execute(sql)
        result = self.cursor.fetchone()[0]
        return result

    def close(self):
        self.db.close()

    def query_has_reserved(self, account):
        sql = """SELECT * FROM reservations WHERE id=%s""" % account
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result


if __name__ == '__main__':
    database = DataBase()
    result = database.get_tests_id('2016141462230')
    print result
