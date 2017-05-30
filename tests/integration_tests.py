import requests
import app.database as redis_db
import json
from tracker.db import Session
from app import logger
from tracker.models import Item

LOG = logger.get_logger()


def test_1():
    jsonq = {
        "external_id" : 'aaaaaaaa-cccc-cccc-dddd-000000000000',
    }

    resp = requests.post(url='http://127.0.0.1:8000/item', json=jsonq)

    resp = json.loads(resp.content)
    assert (resp['meta']['description'] == 'Not existing external_id')

def test_2():
    jsonq = {
        "external_id" : '00000000-0000-0000-0000-00000000000',
    }

    resp = requests.post(url='http://127.0.0.1:8000/item', json=jsonq)
    assert (resp.status_code == 200)

    return json.loads(resp.content)['cart_id']

def test_3():

    jsonq = {
        "cart_id":      '11111111-0000-0000-0000-000000000000',
        "external_id" : 'aaaaaaaa-cccc-cccc-dddd-000000000000',
        "name" : 'Item_1',
        "value" : 123
    }

    resp = requests.post(url='http://127.0.0.1:8000/item', json=jsonq)

    resp = json.loads(resp.content)
    assert (resp['meta']['description'] == 'Not existing cart_id')

def test_4(cart_id):

    jsonq = {
        "cart_id": cart_id,
        "external_id" : '00000000-0000-0000-0000-00000000000',
        "name" : 'Item_1',
        "value" : 123
    }

    resp = requests.post(url='http://127.0.0.1:8000/item', json=jsonq)
    assert (resp.status_code == 200)

def test_5(cart_id):
    session = Session()
    name_1 = 'Item_51'
    name_2 = 'Item_21'

    value_1 = 1231
    value_2 = 3211

    jsonq = {
        "cart_id": cart_id,
        "external_id" : '00000000-0000-0000-0000-00000000000',
        "name" : name_1,
        "value" : value_1
    }


    resp = requests.post(url='http://127.0.0.1:8000/item', json=jsonq)
    assert (resp.status_code == 200)

    item = session.query(Item).filter_by(external_id='00000000-0000-0000-0000-00000000000', cart_id=cart_id).one()
    assert item.name == name_1
    assert item.value == value_1

    jsonqt = {
        "cart_id": cart_id,
        "external_id" : '00000000-0000-0000-0000-00000000000',
        "name" : name_2,
        "value" : value_2
    }

    resp = requests.post(url='http://127.0.0.1:8000/item', json=jsonqt)
    assert (resp.status_code == 200)
    print(cart_id)
    session = Session()
    item2 = session.query(Item).filter_by(cart_id=cart_id).one()

    print(item2.name)
    assert item2.name == name_2
    assert item2.value == value_2

def put_example_data(r):
    r.set('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa', True)
    r.set('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb', True)
    r.set('00000000-0000-0000-0000-00000000000', True)
    r.set('11111111-0000-0000-0000-00000000000', True)


try:
    db = redis_db.RedisStorageEngine()
    r = db.connection()
except Exception as ex:
    LOG.error("Redis connections fail")


put_example_data(r)

test_1()
cart_id = test_2()
test_3()
test_4(cart_id)
test_5(cart_id)

