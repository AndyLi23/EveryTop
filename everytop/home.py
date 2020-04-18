from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from everytop.get_top import websites, get_top
from everytop.auth import login_required
from everytop.db import get_db

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    if g.user:
        db = get_db()
        info = db.execute(
            'SELECT * FROM user WHERE id = ?', (g.user['id'],)
        ).fetchone()
        s = {}
        for i in range(len(websites.keys())):
            if i < len(info['sites']) and info['sites'][i] == '1':
                s[list(websites.keys())[i]] = get_top(list(websites.keys())[i])
        return render_template('home/index.html', sites=s)
    else:
        sites = {}
        for i in websites.keys():
            sites[i] = get_top(i)
        return render_template('home/index.html', sites=sites)


@bp.route('/new', methods=('GET', 'POST'))
@login_required
def new():
    if g.user:
        db = get_db()
        info = db.execute(
            'SELECT * FROM user WHERE id = ?', (g.user['id'],)
        ).fetchone()
        s, u = {}, {}
        for i in range(len(websites.keys())):
            if i < len(info['sites']) and info['sites'][i] == '1':
                s[list(websites.keys())[i]] = get_top(list(websites.keys())[i])
            else:
                u[list(websites.keys())[i]] = get_top(list(websites.keys())[i])
    else:
        s, u = websites, {}
    if request.method == 'POST':
        t = ['0'] * len(websites)
        cur = 0
        for i in websites.keys():
            try:
                request.form[i]
                t[cur] = '1'
            except:
                pass
            cur += 1
        db = get_db()
        db.execute(
            'UPDATE user SET sites = ? WHERE id = ?',
            ("".join(t), g.user['id'])
        )
        db.commit()
        return redirect(url_for('index'))
    return render_template('home/new.html', s=s, u=u)


@bp.route('/reorder', methods=('GET', 'POST'))
@login_required
def reorder():
    if g.user:
        db = get_db()
        info = db.execute(
            'SELECT * FROM user WHERE id = ?', (g.user['id'],)
        ).fetchone()
        s = []
        for i in range(len(websites.keys())):
            if i < len(info['sites']) and info['sites'][i] == '1':
                s.append(list(websites.keys())[i])
    return render_template('home/reorder.html', sites=s)
