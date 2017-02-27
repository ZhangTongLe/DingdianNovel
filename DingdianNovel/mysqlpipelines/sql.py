import mysql.connector
from DingdianNovel import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB
#初始化了一个MySQL操作游标
conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
cursor = conn.cursor(buffered=True)

class SQL:

    #???
    @classmethod
    def insert_dd_name(cls, xs_name, xs_author, category, name_id):
        sql = "INSERT INTO dd_name (`xs_name`, `xs_author`, `category`, `name_id` ) VALUES (%(xs_name)s, %(xs_author)s,%(category)s,%(name_id)s)"
        value = {
            'xs_name':xs_name,
            'xs_author':xs_author,
            'category':category,
            'name_id':name_id
        }
        cursor.execute(sql, value)
        #？？？？？提交事务吗？？
        conn.commit()
    @classmethod
    def select_name(cls, name_id):
        sql = 'SELECT EXISTS(SELECT 1 FROM dd_name WHERE name_id = %(name_id)s)'
        value = {
            'name_id':name_id
        }
        cursor.execute(sql, value)
        return cursor.fetchall()[0]