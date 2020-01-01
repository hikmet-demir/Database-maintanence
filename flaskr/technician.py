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

    id = [[i[0]] for i in my_requests]
    status = [[i[5]] for i in my_requests]
    
    data = {
        "id" : id,
        "status" : status
    }

    return render_template('technician/technician_welcome.html',data=data, size = len(id))

@bp.route('/get_details')
@login_required
def get_details():
    return render_template('technician/get_details.html')

@bp.route('/write_preliminary_report')
@login_required
def write_preliminary_report():
    db = get_db()
    technician_id = g.user['id']
    repairment_id = request.args["request"]
    repairment =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (repairment_id,)
    ).fetchone()

    product_id = repairment["product_id"]
    product =  db.execute(
        'SELECT * FROM product WHERE id = ?', (product_id,)
    ).fetchone()
    price = product["price"]
    model = product["model"]
    color = product["color"]
    years_of_warranty = product["years_of_warranty"]
    category_id = product["cat_id"]
    #prelim = repairment["prelim"]
    data = {
        "product_id": product_id,
        "price": price,
        "model": model,
        "color": color,
        "warranty": years_of_warranty,
        "category_id": category_id
    }

    return render_template('technician/write_preliminary.html   ', data = data)
    return request.args["request"]
    repairment =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (technician_id,)
    ).fetchone()
    db.commit()
    print("REPAIRMENT =====>>>> ",repairment["product_id"])
    return repairment["product_id"]
    product_id = [[i[2]] for i in repairment]
    return render_template('technician/write_preliminary', data = product_id)
    print( product_id)
    return product_id
    return "asd"


@bp.route('/write_detailed_report')
@login_required
def write_detailed_report():
    return "asd"


    
    




