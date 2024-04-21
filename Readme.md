# python version 3.12.3
pip install -r requirements.txt

run app:
    gunicorn -w 1 "app:create_app()"
