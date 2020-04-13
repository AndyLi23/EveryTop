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
        'SELECT s.id, user_id, sites'
        ' FROM sites s JOIN user u ON s.user_id = u.id'
    ).fetchall()
    sites = {}
    for i in websites.keys():
        sites[i] = get_top(i)
    return render_template('home/index.html', info=info, sites=sites)


@bp.route('/new', methods=('GET', 'POST'))
@login_required
def new():
    if request.method == 'POST':
        t = [0] * len(websites)
        cur = 0
        for i in websites.keys():
            try:
                request.form[i]
                t[cur] = 1
            except:
                pass
            cur += 1
        return redirect(url_for('index'))
    return render_template('home/new.html', sites=websites.keys())
