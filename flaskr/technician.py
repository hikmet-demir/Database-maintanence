import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('technician', __name__, url_prefix='/technician')

@bp.route('/technician_index', methods =('GET'))
@login_required
def technician_index():


@bp.route('/get_details', methods =('GET'))
@login_required
def get_details():


@bp.route('/write_preliminary_report', methods =('GET, POST'))
@login_required
def write_preliminary_report():


@bp.route('/write_detailed_report', methods =('GET, POST'))
@login_required
def write_preliminary_report():


    
    




