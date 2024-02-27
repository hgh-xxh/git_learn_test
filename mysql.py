
from datetime import datetime

import pymysql

# 建立与MySQL服务器的连接
conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='test')
cursor = conn.cursor()

# 创建测试表
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (id INT PRIMARY KEY, username VARCHAR(50), email VARCHAR(100), created_at TIMESTAMP)")

# 插入 20000 条数据
start_time = datetime.now()
for i in range(1, 20001):
    username = f'user{i}'
    email = f'user{i}@example.com'
    cursor.execute("INSERT INTO users (id, username, email, created_at) VALUES (%s, %s, %s, NOW())", (i, username, email))
conn.commit()
end_time = datetime.now()
insert_time = end_time - start_time
print("Data insertion time:", insert_time)

start_time = datetime.now()
for i in range(1000):
    cursor.execute("SELECT * FROM users WHERE username = 'user1'")
end_time = datetime.now()
query_time_not_with_index = end_time - start_time
print("Query time not with index:", query_time_not_with_index)


# 创建索引
cursor.execute("CREATE INDEX idx_username ON users (username)")
cursor.execute("CREATE INDEX idx_email ON users (email)")

# 查询示例：使用索引加速查询
start_time = datetime.now()
for i in range(1000):
    cursor.execute("SELECT * FROM users WHERE username = 'user1'")
end_time = datetime.now()
query_time_with_index = end_time - start_time
print("Query time with index:", query_time_with_index)

print("倍数",query_time_not_with_index/query_time_with_index)

# 关闭连接
cursor.close()
conn.close()
