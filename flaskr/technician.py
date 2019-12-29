import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('technician', __name__, url_prefix='/technician')

@bp.route('/technician_index')
@login_required
def welcome():
    db = get_db()

    my_requests =  db.execute(
            'SELECT * FROM repairment WHERE technician_id = ?', (g.user['id'],)
        ).fetchall()

    return render_template('technician/technician_welcome.html',data=my_requests)


@bp.route('/get_details')
@login_required
def get_details():
    return "asd"


@bp.route('/write_preliminary_report')
@login_required
def write_preliminary_report():
    return "asd"


@bp.route('/write_detailed_report')
@login_required
def write_detailed_report():
    return "asd"


    
    




