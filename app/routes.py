from flask import render_template

from app import app

mock_user = {'username': 'dani'}
mock_posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }
]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', user=mock_user, posts=mock_posts)
