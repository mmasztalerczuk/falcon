for i in `seq 1 1 4`; do celery -A app.api.update_db worker --loglevel=info --concurrency=1 -Q q$i -n node$i & done
