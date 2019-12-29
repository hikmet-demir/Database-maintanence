from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db
import sys
from datetime import date

bp = Blueprint('customer', __name__, url_prefix='/customer')

def diff_dates(date1, date2):
    return abs(date2-date1).days

@bp.route('/welcome',methods =('GET','POST'))
def welcome():
    db = get_db()

    products =  db.execute(
            'SELECT * FROM product WHERE customer_id = ?', (g.user['id'],)
        ).fetchall()
    
    # outer brackets are required, it doesnt work without them somehow
    # thats why id's are shown in the bracets on the website
    data = [[i[0]] for i in products]

    return render_template('customer/customer_welcome.html', data = data, size = len(data))


@bp.route('/get_details',methods =('GET','POST'))
def get_details():
    db = get_db()
    product_id = int(request.args["products"][1])

    product =  db.execute(
            'SELECT * FROM product WHERE id = ?', (product_id,)
        ).fetchone()
    
    id = product["id"]
    price = product["price"]
    model = product['model']
    color = product['color']
    warranty = product['years_of_warranty']
    cat_id = product['cat_id']
    cat_name = db.execute(
            'SELECT * FROM category WHERE id = ?', (cat_id,)
        ).fetchone()['cat_name']
    
    
    return render_template('customer/customer_get_product_details.html'
        ,id=product_id, price=price, model=model, Color=color,
        years_of_warranty=warranty, category_name=cat_name)


@bp.route('/create_request',methods =('GET','POST'))
def create_request():
    db = get_db()
    product_id = request.args["products"][1]

    product =  db.execute(
            'SELECT * FROM product WHERE id = ?', (product_id,)
        ).fetchone()

    id = product["id"]
    model = product['model']
    warranty = product['years_of_warranty']
    today = date.today()
    time_of_buying = product["time_of_buying"]
    difference_year = int(diff_dates(today, time_of_buying)/365)

    if difference_year >= warranty:
        return "Warranty is expired, you cannot create a request for this product!"

    repairments_of_product =  db.execute(
            'SELECT * FROM repairment WHERE product_id = ?', (product_id,)
        ).fetchall()

    if repairments_of_product is not None:
        for row in repairments_of_product:
            if row[5] != "closed":
                return "There is a continuing request for this product, you cannot create a new one!"    
    
    return render_template('customer/create_request.html',
        id=product_id, model=model, years_of_warranty=warranty)
    
@bp.route('/complete_request',methods =('GET','POST'))
def complete_request():
    product_id = request.args['product_id']
    problem = request.args['myTextBox']
    customer_id = g.user['id']
    status = "shippedToTechnician"

    db = get_db()

    # SIMDILIK TEKNISYENI ELIMLE YERLESTIRDIM REPAIRMENT tablosu
    db.execute(
            'INSERT INTO repairment (technician_id, product_id, customer_id, \
                problem,status) VALUES (?, ?, ?, ?, ?)',
            (2, product_id, customer_id, problem, status)
        )

    db.commit()

    repairment =  db.execute(
            'SELECT * FROM repairment WHERE product_id = ?', (product_id,)
        ).fetchone()

    repairment_id = repairment["id"]

    delivery_date = today = date.today()

    db.execute(
            'INSERT INTO shipping (delivery_date, repairment_id, customer_id, \
                technician_id,status) VALUES (?, ?, ?, ?, ?)',
            (delivery_date, repairment_id, customer_id, 1, "onWay")
        )

    db.commit()
    return redirect(url_for('customer.welcome'))

@bp.route('/get_requests',methods =('GET','POST'))
def get_requests():
    # db = get_db()
    user_id = g.user['id']

    db = get_db()
    requests =  db.execute(
        'SELECT * FROM repairment WHERE customer_id = ?', (g.user['id'],)
    ).fetchall()
    data = [[i[0]] for i in requests]

    return render_template('customer/customer_view_requests.html', data = data, size = len(data) )
    
@bp.route('/get_complaints',methods =('GET','POST'))
def get_complaints():
    # db = get_db()
    user_id = g.user['id']
    return render_template('customer/customer_view_complaints.html')

@bp.route('/get_request_details', methods=('GET','POST'))
def get_request_details():
    db = get_db()
    user_id = g.user['id']
    request_id = request.args["requests"][1]
    req =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (request_id,)
    ).fetchone()

    product_id = req["product_id"]
    req_status = req["status"]
    
    product = db.execute(
        'SELECT * FROM product WHERE id = ?', (product_id,)
    ).fetchone()
    product_model = product["model"]
    product_price = product["price"]
    data = {
        "name":product_model,
        "status":req_status,
        "price":product_price
    }
    return render_template('customer/customer_request_details.html', data=data)
    

