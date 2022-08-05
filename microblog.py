from app import app
from app import db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    """
    With this function, you can run `flask shell` in terminal and it will
    start a Python interpreter in the context of the application (i.e. with
    the following defined without having to import)
    """
    return {
        'db': db,
        'User': User,
        'Post': Post,
    }
