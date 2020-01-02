import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db
from _datetime import date

bp = Blueprint('technician', __name__, url_prefix='/technician')

@bp.route('/technician_index')
@login_required
def welcome():
    db = get_db()

    my_requests =  db.execute(
            'SELECT * FROM repairment WHERE technician_id = ? AND status <> "closed"', (g.user['id'],)
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
    db = get_db()
    technician_id = g.user['id']
    repairment_id = request.args["request"]
    repairment =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (repairment_id,)
    ).fetchone()
    product_id = repairment["product_id"]
    product =  db.execute(
        'SELECT * FROM product WHERE id = ? ', (product_id,)
    ).fetchone()
    product_price = product["price"]
    product_color = product["color"]
    product_model = product["model"]
    warranty = product["years_of_warranty"]
    cat_id = product["cat_id"]
    
    data = {
        "product_id": product_id,
        "price":product_price,
        "model": product_model,
        "color": product_color,
        "warranty": warranty,
        "cat_id": cat_id
    }
    return render_template('technician/get_details.html', data=data)

@bp.route('/write_preliminary_report',methods =('GET','POST'))
@login_required
def write_preliminary_report():
    db = get_db()
    technician_id = g.user['id']
    repairment_id = request.args["request"]
    repairment =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (repairment_id,)
    ).fetchone()

    if repairment["status"] != "waitingForPrelim":
        return "Current status of the request is not applicable for this action"

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
        "category_id": category_id,
        "repairment_id": repairment_id
        }
    
    return render_template('technician/write_preliminary.html', data = data)


@bp.route('/submit_preliminary',methods =('GET','POST'))
def submit_preliminary():
    preliminary_text =  request.args["preliminary_text"]
    repairment_id = request.args["repairment_id"]
    db = get_db()

    db.execute("UPDATE repairment set prelim = ?, status = 'waitingForCustomerDecision' where id = ?", 
    (preliminary_text, repairment_id))
    db.commit()

    return redirect(url_for("technician.welcome"))


@bp.route('/write_detailed_report')
@login_required
def write_detailed_report():
    db = get_db()
    technician_id = g.user['id']
    repairment_id = request.args["request"]
    repairment =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (repairment_id,)
    ).fetchone()
    product_id = repairment["product_id"]
    print("PRODUCT ID ====", product_id)
    product =  db.execute(
        'SELECT * FROM product WHERE id = ?', (product_id,)
    ).fetchone()
    parts_database = db.execute(
        'SELECT * FROM parts WHERE product_id = ?', (product_id,)
    ).fetchall()
    parts = [[i[2] for i in parts_database]][0]
    part_ids = [[i[0] for i in parts_database]][0]
    print(parts)
    length = len(parts)
    price = product["price"]
    model = product["model"]
    color = product["color"]
    years_of_warranty = product["years_of_warranty"]
    category_id = product["cat_id"]
    data = {
        "product_id": product_id,
        "price": price,
        "model": model,
        "color": color,
        "warranty": years_of_warranty,
        "category_id": category_id,
        "repairment_id": repairment_id,
        "parts": parts,
        "part_ids": part_ids,
        "len": length
        }
    return render_template('technician/detailed_report.html',data=data)

@bp.route('/item_received_report')
@login_required
def item_received_report():
    db = get_db()
    repairment_id = request.args["request"]

    db.execute("UPDATE repairment set status = 'waitingForPrelim' where id = ?", 
    (repairment_id,))
    db.commit()

    return redirect(url_for("technician.welcome"))

@bp.route('/fix_db')
def fix_db():
    db = get_db()
    db.commit()
    return "true"

@bp.route('/detailed_report_submit')
@login_required
def detailed_report_submit():
    product_id = request.args["product_id"]
    repairment_id = request.args["repairment_id"]
    dd = dict(request.args)
    del dd["product_id"]
    del dd["repairment_id"]
    db = get_db()
    for key in dd:
        if type(dd[key]) == type([]):    
            value = dd[key][0]
        else:
            value = dd[key]
        if value =="Fixed":
            value = "fixed"
        elif value == "Changed":
            value = "changed"
        elif value == "Not Changed":
            value = "notChanged"

        db.execute("INSERT into parts_repairment (repairment_id, part_id,product_id,status) values (?,?,?,?)",
        (repairment_id, key, product_id, value))
        db.commit()

    db.execute("UPDATE repairment set status = 'repairedItemShippedToCustomer' where id = ?", 
    ( repairment_id,))
    db.commit()

    repairment =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (repairment_id,)
    ).fetchone()
    customer_id = repairment["customer_id"]

    delivery_date = date.today()
    db.execute(
        'INSERT INTO shipping (delivery_date, repairment_id, customer_id, \
            technician_id,status) VALUES (?, ?, ?, ?, ?)',
        (delivery_date, repairment_id, customer_id, 1, "onWay")
    )

    db.commit()

    return redirect(url_for("technician.welcome"))
