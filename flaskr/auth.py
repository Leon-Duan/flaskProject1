import functools, time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user(username, password) VALUES(?,?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except db.InternalError:
                error = f'User {username} is already registered'
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/reset_password', methods=('GET', 'POST'))
def reset_password():
    if request.method == 'POST':
        username = request.form['username']
        db = get_db()  # 连接到数据库
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        error = None

        if user is None:
            error: str = '用户不存在'

        if error is None:
            password = request.form['password']
            db.execute(
                'UPDATE user SET password = ? where username = ?', (generate_password_hash(password),username,)
            )
            db.commit()
            message = '已修改密码,3s后返回登入界面'
            flash(message)
            time.sleep(3)
            return redirect(url_for('auth.login'))
        else:
            flash(error)

    return render_template('auth/reset_password.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = '该用户不存在'
        elif not check_password_hash(user['password'], password):
            error = '密码错误'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
