from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for

from app import app
from app.forms import LoginForm

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # runs validation when browser sends POST on user submit
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', login_form=form)
