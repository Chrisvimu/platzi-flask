from flask import Flask, request, make_response, redirect, render_template, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'SUPER SECRET'

todos = ['Buy stuff', 'Send buy request', 'get product']


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello')
def hello():
    user_ip = session.get('user_ip')
    context = {
        'user_ip': user_ip,
        'todos': todos,
    }
    # two ** before a dictionary expend it automatically
    return render_template('hello.html', **context)
