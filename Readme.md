pip install flask
pip install gunicorn

run app:
    gunicorn -w 1 "app:create_app()"
