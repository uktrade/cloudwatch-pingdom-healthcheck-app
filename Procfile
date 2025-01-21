# web: uwsgi --ini uwsgi.ini --http :8000
web: gunicorn -w 4 -t 2 -b 0.0.0.0:8080 main:app
