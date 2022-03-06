import pymysql
from dbutils.pooled_db import PooledDB, PooledSharedDBConnection
from movieScrapy.settings import MYSQL_CONFIG


class MysqlUtils:
    PYMYSQL_POOL = PooledDB(
        creator=pymysql,
        maxconnections=50,
        mincached=5,
        maxcached=5,
        maxshared=10,
        blocking=True,
        maxusage=None,
        ping=1,
        autocommit=True,
        host=MYSQL_CONFIG['host'],
        port=MYSQL_CONFIG['port'],
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        database=MYSQL_CONFIG['database'],
        charset=MYSQL_CONFIG['charset']
    )

    @staticmethod
    def get_connection():
        pool = MysqlUtils.PYMYSQL_POOL
        return pool.connection(shareable=True)

    @staticmethod
    def close(connection, cursor):
        cursor.close()
        connection.close()

    @staticmethod
    def upsert(sql, param=()):
        try:
            connection = MysqlUtils.get_connection()
            cursor = connection.cursor()
            if param:
                cursor.execute(sql, param)
            else:
                result = cursor.execute(sql)
        except Exception as e:
            print('exception : ', e)
        finally:
            MysqlUtils.close(connection, cursor)
