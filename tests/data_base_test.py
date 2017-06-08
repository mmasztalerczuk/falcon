import random
import string

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine

from tests.utils import print_function_name, create_config
from tracker.models import Base

USER = 'mariusz'
HOST = '127.0.0.1'
DBNAME = 'postgres'


@print_function_name
def create_data_base():
    con = connect(dbname=DBNAME, user=USER, host=HOST)

    dbname = 't_' + ''.join(random.choice(string.ascii_lowercase
                                          + string.digits) for _ in range(7))

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('CREATE DATABASE ' + dbname)
    cur.close()
    con.close()

    db_dsn = 'postgresql://%s:password@%s/%s' % (USER, HOST, dbname)
    engine = create_engine(db_dsn)
    Base.metadata.create_all(engine)

    create_config(user=USER, host=HOST, dbname=dbname)

    return dbname, db_dsn


@print_function_name
def destroy_data_base(dbname):
    con = connect(dbname=DBNAME, user=USER, host=HOST)

    con.set_isolation_level(0)
    cur = con.cursor()
    cur.execute('DROP DATABASE ' + dbname)
    cur.close()
    con.close()
