import pymysql.cursors

conn = pymysql.connect(host='localhost',
                user='root',
                port=8889,
                password='root',
                db='airport_proj',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)