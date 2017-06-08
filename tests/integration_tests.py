import json
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.database as redis_db

from time import sleep
from app import logger
from tests.data_base_test import create_data_base
from tests.utils import print_function_name, run_celery, kill_celery, \
    run_gunicorn, delete_config, kill_gunicorn
from tracker.models import Item

LOG = logger.get_logger()


@print_function_name
def test_not_existing_id():
    jsonq = {
        "external_id": 'aaaaaaaa-cccc-cccc-dddd-000000000000',
    }

    resp = requests.post(url='http://127.0.0.1:8000/item', json=jsonq)

    resp = json.loads(resp.content)

    assert (resp['meta']['description'] == 'Not existing external_id')


@print_function_name
def test_correct_response():
    jsonq = {
        "external_id": '00000000-0000-0000-0000-00000000000',
    }

    resp = requests.post(url='http://127.0.0.1:8000/item', json=jsonq)
    assert (resp.status_code == 200)

    return json.loads(resp.content)['cart_id']


@print_function_name
def test_not_existing_cart_id():

    jsonq = {
        "cart_id": '11111111-0000-0000-0000-000000000000',
        "external_id": 'aaaaaaaa-cccc-cccc-dddd-00000000000',
        "name": 'Item_1',
        "value": 123
    }

    resp = requests.post(url='http://127.0.0.1:8000/item', json=jsonq)

    resp = json.loads(resp.content)

    assert (resp['meta']['description'] == 'Not existing cart_id')


@print_function_name
def test_correct_response_with_cart_id(cart_id):

    jsonq = {
        "cart_id": cart_id,
        "external_id": '00000000-0000-0000-0000-00000000000',
        "name": 'Item_1',
        "value": 123
    }

    resp = requests.post(url='http://127.0.0.1:8000/item', json=jsonq)
    assert (resp.status_code == 200)


@print_function_name
def test_update_db(cart_id, dbname):

    name_1 = 'Item_51'
    name_2 = 'Item_21'

    value_1 = 1231
    value_2 = 3211

    external_id = '00000000-0000-0000-0000-00000000000'

    jsonq = {
        "cart_id": cart_id,
        "external_id": external_id,
        "name": name_1,
        "value": value_1
    }

    resp = requests.post(url='http://127.0.0.1:8000/item', json=jsonq)
    assert (resp.status_code == 200)

    # This is wrong, but also it is the easiest way
    # to test the update of database
    sleep(2)

    engine = create_engine(dbname)
    Session = sessionmaker(bind=engine)
    session = Session()
    print(external_id, cart_id)
    item = session.query(Item).filter_by(external_id=external_id,
                                         cart_id=cart_id).one()
    assert item.name == name_1
    assert item.value == value_1

    jsonqt = {
        "cart_id": cart_id,
        "external_id": external_id,
        "name": name_2,
        "value": value_2
    }

    resp = requests.post(url='http://127.0.0.1:8000/item', json=jsonqt)
    assert (resp.status_code == 200)

    # This is wrong, but also it is the easiest way
    # to test the update of database
    sleep(2)

    session = Session()
    item2 = session.query(Item).filter_by(cart_id=cart_id).one()
    Session.close_all()
    assert item2.name == name_2
    assert item2.value == value_2


@print_function_name
def put_example_data(redis_instance):
    redis_instance.set('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa', True)
    redis_instance.set('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb', True)
    redis_instance.set('00000000-0000-0000-0000-00000000000', True)
    redis_instance.set('11111111-0000-0000-0000-00000000000', True)
    redis_instance.set('aaaaaaaa-cccc-cccc-dddd-00000000000', True)


try:
    db = redis_db.RedisStorageEngine()
    r = db.connection()
    r.flushall()
    put_example_data(r)
except Exception as ex:
    LOG.error("Redis connections fail")
    # error


dbname, db_dsn = create_data_base()
sleep(5)
print "New database: " + dbname

try:
    run_celery()

    run_gunicorn()

    print 'Tests:'

    test_not_existing_id()

    gen_cart_id = test_correct_response()

    test_not_existing_cart_id()

    test_correct_response_with_cart_id(gen_cart_id)

    test_update_db(gen_cart_id, db_dsn)
    print "Tests OK"

finally:

    kill_celery()
    kill_gunicorn()

    delete_config()
