# -*- coding: UTF-8 -*-
import cx_Oracle


class DB_oracle(object):
    def __init__(self,username,password,database):
        self.username=username
        self.password=password
        self.database=database
    def connect(self):
        conn = cx_Oracle.connect(self.username+'/'+''+self.password+'@'+self.database)
        cr = conn.cursor()
        return conn,cr
    def select_one(self,sql):
        conn, cr=self.connect()
        cr.execute(sql)
        rs =cr.fetchone()
        conn.close()
        return rs
    def select_all(self,sql):
        conn, cr = self.connect()
        cr.execute(sql)
        rs = cr.fetchall()
        conn.close()
        return rs
    def update_inser_sql(self,sql):
        conn, cr = self.connect()
        cr.execute(sql)
        conn.commit()
        conn.close()
if __name__=='__main__':
    username = 'xxd_stage'
    password = 'Bb919189'
    database = '192.168.31.225:1521/oragbst'
    db=DB_oracle(username,password,database)
    sql="SELECT *  FROM xxd_borrow_collection where borrowid='BW201710273043'"
    a= db.select_one(sql)
    b = db.select_all(sql)
    print a
    print b