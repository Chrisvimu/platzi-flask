import unittest
from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import login_required, current_user
from app import create_app
from app.forms import TodoForm
from app.firestore_service import get_users, get_todos, put_todo

app = create_app()

app.config['SECRET_KEY'] = 'SUPER SECRET'

todos = ['Buy stuff', 'Send buy request', 'get product']


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form
    }

    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)

        flash('Task created successfully')

        return redirect(url_for('hello'))

    # two ** before a dictionary expend it automatically
    return render_template('hello.html', **context)
