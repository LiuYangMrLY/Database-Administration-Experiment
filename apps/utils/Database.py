import pymysql

from db.settings import DATABASE_CONFIG


connection = pymysql.connect(host=DATABASE_CONFIG['HOST'],
                             user=DATABASE_CONFIG['USER'],
                             password=DATABASE_CONFIG['PASSWORD'],
                             database=DATABASE_CONFIG['DATABASE'],
                             port=DATABASE_CONFIG['PORT'])
