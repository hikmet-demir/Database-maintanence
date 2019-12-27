import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/welcome',methods =('GET','POST'))
def welcome():
    db = get_db()

    customers =  db.execute(
            'SELECT * FROM user WHERE user_type == "customer"'
        ).fetchall()

    # outer brackets are required, it doesnt work without them somehow
    # thats why id's are shown in the bracets on the website
    data = [i[0] for i in customers]

    return render_template('customer/admin_welcome.html', data = data, size = len(data))
