import pymysql.cursors

conn = pymysql.connect(host='localhost',
                user='root',
                port=3306,
                password='',
                db='airport_proj',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)