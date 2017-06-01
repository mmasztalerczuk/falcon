Install:

1) Create new virtualenv
2) Install packages (pip install -r requirements.txt)
3) Run postgresql database (for example - systemctl start postgresql.service)
4) Run redis (for example - systemctl start redis.service)
5) Run celery (celery -A app.api.update_db worker --loglevel=info &)
6) Run app (gunicorn main:main)
