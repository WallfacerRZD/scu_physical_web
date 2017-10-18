# coding=utf-8

import MySQLdb
import MySQLdb.cursors


class DataBase(object):
    def __init__(self):
        self.user = 'root'
        self.pass_word = '85607505rzd?'
        self.db_name = 'test'
        self.db = MySQLdb.connect('localhost', self.user, self.pass_word, self.db_name, charset='utf8')
        self.cursor = self.db.cursor()

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
        sql = u"""INSERT INTO SCORES
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
        # finally:
        #     self.close()

    def query_datas(self, account):
        sql = "SELECT * FROM SCORES WHERE ACCOUNT=%s" % account
        self.cursor.execute(sql)
        rs = self.cursor.fetchall()
        # rs = ((身高, 体重, 肺活量, 跳远, 50米, 台阶,
        #        800米, 1000米, 仰卧起坐, 引体向上, 坐位体前屈,
        #        握力, 视力左, 视力右, 学期, 总评, 需要改进),
        # (),
        # .....)
        return rs

    def query_user(self, account, password):
        sql = 'SELECT * FROM users where account="%s" and password="%s"' % (account, password)
        self.cursor.execute(sql)
        rs = self.cursor.fetchone()
        return rs

    def close(self):
        self.db.close()


if __name__ == '__main__':
    database = DataBase()
    database.insert_users('201614146207', '462307', u'冉哲东')
