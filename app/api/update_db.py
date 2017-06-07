import celery

from sqlalchemy.orm.exc import NoResultFound
from tracker.db import Session
from tracker.models import Item, Cart

app = celery.Celery('update_db', broker='redis://localhost:6379/0',
                    backend='redis://localhost:6379/0')

app.conf.update(CELERY_CREATE_MISSING_QUEUES=True)


@app.task
def add_new_cart(data):
    session = Session()
    new_cart = Cart(id=data['cart_id'])

    session.add(new_cart)
    session.commit()


@app.task
def update_item(data):
    session = Session()
    try:
        item = session.query(Item).filter_by(external_id=data['external_id'],
                                             cart_id=data['cart_id']).one()
        item.name = data['name']
        item.value = data['value']

    except NoResultFound:
        obj = Item(**data)
        session.add(obj)

    session.commit()
