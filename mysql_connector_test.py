import mysql.connector

conn = mysql.connector.connect(user='root', password='yg19940916', database='mysql_connector_test')

'''cursor = conn.cursor()
#创建user表
cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
#插入一行记录
cursor.execute('insert into user (id, name) values (%s, %s)', ['1', 'yangguang'])
print(cursor.rowcount)
#提交事务
conn.commit()
conn.close()
'''

#连在一起使用会出现问题
#raise errors.OperationalError("MySQL Connection not available.")
#如果你打开了一个cursor，但是没有把里面的结果集都read一遍就把它close掉了，以后就悲剧了。
#You must fetch all rows before being able to execute new queries using the same connection.

#运行查询
cursor = conn.cursor()
cursor.execute('select * from user where id = %s', ('1',))
values = cursor.fetchall()
print(values)

#关闭cursor and connection
cursor.close()
conn.close()


