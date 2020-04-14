from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from everytop.get_top import websites, get_top
from everytop.auth import login_required
from everytop.db import get_db

bp = Blueprint('home', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    info = db.execute(
        'SELECT * FROM user WHERE id = ?', (g.user['id'],)
    ).fetchone()
    sites = {}
    for i in range(len(websites.keys())):
        if info['sites'][i] == '1':
            sites[websites.keys()[i]] = get_top(websites.keys()[i])
    print(info['sites'])
    return render_template('home/index.html', sites=sites)


@bp.route('/new', methods=('GET', 'POST'))
@login_required
def new():
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
        print(t)
        db.execute(
            'UPDATE user SET sites = ? WHERE id = ?',
            ("".join(t), g.user['id'])
        )
        return redirect(url_for('index'))
    return render_template('home/new.html', sites=websites.keys())
