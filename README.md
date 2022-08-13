# Microblog Tutorial
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

## Getting Started

```sh
source venv/bin/activate
```

## Running the Application

```sh
FLASK_APP=microblog.py
FLASK_ENV=development  # optional
flask run
```

Testing Email:
```sh
# before executing flask run:
export MAIL_SERVER=localhost
export MAIL_PORT=8025
# in a separate terminal:
python -m smtpd -n -c DebuggingServer localhost:8025
```
