import os
import pymysql
from . import readini


class PyMySQL:
    father_path = os.path.dirname(os.path.dirname(__file__))

    filepath = father_path + "\\config\\testenv.ini"

    def __init__(self,func):
        cf=readini.readini(self.filepath)
        self.conn=pymysql.connect(host=cf.get('test_db','host'),\
                                  port=int(cf.get('test_db','port')),\
                                  user=cf.get('test_db','user'),\
                                  password=cf.get('test_db','password'),\
                                  database=cf.get('test_db','database')
                                  )

        self.__func=func

    def __call__(self,*args,**kwargs):
        sql=self.__func(*args, **kwargs)

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()  # 超时重连，默认300s
            cursor = self.conn.cursor()
            cursor.execute(sql)

        result=None
        if sql.startswith("select"):
            result = cursor.fetchone()[0]  # 获取一条数据

        self.conn.commit()
        self.conn.close()
        return result
        pass




class PyMySQL1():
    father_path = os.path.dirname(os.path.dirname(__file__))

    filepath = father_path + "\\config\\testenv.ini"

    def __init__(self):
        cf=readini.readini(self.filepath)
        self.conn=pymysql.connect(host=cf.get('test_db','host'),\
                                  port=int(cf.get('test_db','port')),\
                                  user=cf.get('test_db','user'),\
                                  password=cf.get('test_db','password'),\
                                  database=cf.get('test_db','database')
                                  )

    def sqlfun(self,func):
            def inner(*args,**kwargs):

                sql=func(*args,**kwargs)

                try:
                    cursor = self.conn.cursor()
                    cursor.execute(sql)
                except:
                    self.conn.ping()  # 超时重连，默认300s
                    cursor = self.conn.cursor()
                    cursor.execute(sql)
                self.conn.commit()
                self.conn.close()

                pass

            return inner



    def mysqldel(self,table,field,value):

        sql="delete from "+table+" where "+ field+" = '"+str(value)+"'"

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()              #超时重连，默认300s
            cursor = self.conn.cursor()
            cursor.execute(sql)
        self.conn.commit()
        self.conn.close()



    def mysqlget(self,sql):

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()              #超时重连，默认300s
            cursor = self.conn.cursor()
            cursor.execute(sql)
        result=cursor.fetchone()[0]       #获取一条数据
        self.conn.close()

        return result


    def mysqlinsert(self, sql):

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()  # 超时重连，默认300s
            cursor = self.conn.cursor()
            cursor.execute(sql)
        self.conn.commit()
        self.conn.close()


    def checkdbok(self,tb,key,value):

        sql="select count(*) from "+ tb +" where "+key+ "='"+value+"'"

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()  # 超时重连，默认300s
            cursor = self.conn.cursor()
            cursor.execute(sql)
        result = cursor.fetchone()[0]  # 获取一条数据
        self.conn.close()
        return result>0
        pass



@PyMySQL
def MysqlGet(sql):

    return sql

@PyMySQL
def MysqlInsert( sql):

    return sql

@PyMySQL
def MysqlDel(table,field,value):
    sql="delete from "+table+" where "+ field+" = '"+str(value)+"'"

    return sql

@PyMySQL
def checkdbok(tb,key,value):
    sql = "select count(*) from " + tb + " where " + key + "='" + value + "'"

    return sql