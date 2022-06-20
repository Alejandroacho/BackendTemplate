import pymysql

from .celery.worker import app as celery_app


pymysql.install_as_MySQLdb()
__all__ = ('celery_app',)
