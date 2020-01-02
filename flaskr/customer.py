from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db
import sys
from datetime import date
from random import randrange

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
    id = [[i[0]] for i in products]
    model = [[i[2]] for i in products]
    data = {
        "id": id,
        "model": model
    }
    return render_template('customer/customer_welcome.html', data = data, size = len(model))


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
    technicians = db.execute(
            'SELECT id FROM technician'
        ).fetchall()

    ids = []
    for id in technicians:
        ids.append(id[0])
    l = len(ids)
    index = randrange(l)
    db.execute(
            'INSERT INTO repairment (technician_id, product_id, customer_id, \
                problem,status) VALUES (?, ?, ?, ?, ?)',
            (ids[index], product_id, customer_id, problem, status)
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
    idd = [i[0] for i in requests]
    status = [i[5] for i in requests]
    data = {
        "id": idd,
        "status": status
    }
    #return data
    return render_template('customer/customer_view_requests.html', data = data, size = len(status) )

@bp.route('/get_complaints',methods =('GET','POST'))
def get_complaints():
    # db = get_db()
    db = get_db()

    complaints =  db.execute(
            'SELECT c.id, p.model FROM complaint c, repairment r, product p WHERE p.id == r.product_id and c.repairment_id == r.id and c.customer_id = ?', (g.user['id'],)
        ).fetchall()

    return render_template('customer/customer_view_complaints.html', data = complaints)

@bp.route('/get_complaint_details',methods =('GET','POST'))
def get_complaint_details():
    db = get_db()
    complaint_id = request.args["complaints"]

    complaint_info =  db.execute(
            'SELECT c.problem, p.model FROM complaint c, repairment r, product p WHERE p.id == r.product_id and c.repairment_id == r.id and c.customer_id = ?', (g.user['id'],)
        ).fetchone()

    return render_template('customer/customer_complaint_details.html', data = complaint_info)


@bp.route('/get_request_details', methods=('GET','POST'))
def get_request_details():
    db = get_db()
    user_id = g.user['id']
    request_id = request.args["requests"]
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
        "price":product_price,
        "req_id":request_id
    }
    return render_template('customer/customer_request_details.html', data=data)

@bp.route('/make_decision', methods=['GET','POST'])
def make_decision():
    db = get_db()
    user_id = g.user['id']
    request_id = request.args["requests"]
    req =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (request_id,)
    ).fetchone()
    product_id = req["product_id"]
    #prelim = req["prelim"]
    prelim = "This product has been examined and decided to return"
    req =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (request_id,)
    ).fetchone()
    product_id = req["product_id"]
    req_status = req["status"]

    product = db.execute(
        'SELECT * FROM product WHERE id = ?', (product_id,)
    ).fetchone()
    product_model = product["model"]
    data = {
        "name": product_model,
        "prelim":prelim
    }
    return render_template('customer/customer_see_preliminary.html', data=data)

@bp.route('/see_preliminary_report',methods=['GET','POST'])
def see_preliminary_report():
    db = get_db()
    user_id = g.user['id']
    request_id = request.form["req_id"]
    req =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (request_id,)
    ).fetchone()

    product_id = req["product_id"]
    #prelim = req["prelim"]
    prelim = "This product has been examined and decided to return"
    product = db.execute(
        'SELECT * FROM product WHERE id = ?', (product_id,)
    ).fetchone()
    product_model = product["model"]
    data = {
        "name": product_model,
        "prelim":prelim
    }
    return render_template('customer/customer_see_preliminary.html', data=data)

<<<<<<< HEAD
@bp.route('/customer_chat_page',methods=['GET','POST'])
def customer_chat_page(complaint_MADAFAKA = None):
    if complaint_MADAFAKA == None:
        complaint_id = request.args["complaints"]
    else:
        complaint_id = complaint_MADAFAKA
    user_id = g.user['id']

    db = get_db()
    requests =  db.execute(
        'SELECT * FROM messages WHERE complaint_id = ?', (complaint_id,)
    ).fetchall()
    ##id|created|text|complaint_id|receiver_id|sender_id

    idd = [i[0] for i in requests]
    date = [i[1] for i in requests]
    text = [i[2] for i in requests]
    comp_id = [i[3] for i in requests]
    rec_id = [i[4] for i in requests]
    send_id = [i[5] for i in requests]

    data = {
        "id": idd,
        "date": date,
        "text": text,
        "comp_id": comp_id,
        "rec_id": rec_id,
        "send_id": send_id
    }
    #return data
    return render_template('customer/customer_chat_page.html', data = data, size = len(idd), complaint_id = complaint_id )

@bp.route('/insert_message',methods=['GET','POST'])
def insert_message():
    comp_id = request.form['subject']
    user_id = g.user['id']

    message = str(request.form['message'])

    db = get_db()

    #receiver_id =  db.execute(
    #    'SELECT receiver_id FROM messages WHERE complaint_id = ? and sender_id = ?', (comp_id,user_id,)
    #).fetchone()[0]

    receiver_id =  db.execute(
        'SELECT customer_service_asisstant_id FROM complaint WHERE id = ?', (comp_id,)
    ).fetchone()[0]


    requests =  db.execute(
        'INSERT INTO messages (text,complaint_id ,receiver_id, sender_id) VALUES (?, ?, ?, ?)' , (message,comp_id,receiver_id,user_id)
    ).fetchall()

    db.commit()

    return customer_chat_page(comp_id)
=======
@bp.route('/decision_renew', methods = ['GET','POST'])
def decision_renew():
    None

@bp.route('/decision_return', methods = ['GET','POST'])
def decision_return():
    None

@bp.route('decision_repair', methods = ['GET','POST'])
def decision_repair():
    None

>>>>>>> e1e254bfa8593859d4170b5f83da0bc6bb7bb6ba
