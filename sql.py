# coding=utf-8

import MySQLdb
import MySQLdb.cursors


class DataBase(object):
    def __init__(self):
        self.user = 'root'
        self.pass_word = '85607505rzd?'
        self.db_name = 'test'
        self.db = MySQLdb.connect('localhost', self.user, self.pass_word, self.db_name, charset='utf8',
                                  cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.db.cursor()

    def insert_datas(self, datas):
        sql = u"""INSERT INTO SCORES
                  (account, 身高, 体重, 肺活量, 跳远, 50米, 台阶, 
                   800米, 1000米, 仰卧起坐, 引体向上, 坐位体前屈, 
                   握力, 视力左, 视力右, 学期, 总评, 需要改进)
              VALUES("%s", "%s", "%s", "%s", "%s", "%s", 
                     "%s", "%s", "%s", "%s", "%s", "%s", 
                     "%s", "%s", "%s", "%s", "%s", "%s")""" \
              % ('2016141462307', datas[0], datas[1], datas[2], datas[3], datas[4],
                 datas[5], datas[6], datas[7], datas[8], datas[9], datas[10],
                 datas[11], datas[12], datas[13], '20161', u'合格', u'引体向上')
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception, e:
            print str(e)
            self.db.rollback()

    def query_datas(self, account):
        sql = "SELECT * FROM SCORES WHERE ACCOUNT=%s" % account
        self.cursor.execute(sql)
        rs = self.cursor.fetchall()
        return rs

    def query_user(self, account):
        sql = 'SELECT * FROM users where account="%s"' % account
        self.cursor.execute(sql)
        rs = self.cursor.fetchone()
        self.close()
        return rs

    def close(self):
        self.db.close()


if __name__ == '__main__':
    database = DataBase()
    database.insert_datas([])
