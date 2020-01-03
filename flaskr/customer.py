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
            "SELECT * FROM product WHERE customer_id = ? AND status != ?", (g.user['id'],"return")
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

    delivery_date = date.today()

    db.execute(
            'INSERT INTO shipping (delivery_date, repairment_id, customer_id, \
                technician_id,status) VALUES (?, ?, ?, ?, ?)',
            (delivery_date, repairment_id, customer_id, 1, "onWay")
        )

    db.commit()
    return redirect(url_for('customer.welcome'))

@bp.route('/get_requests',methods =('GET','POST'))
def get_requests():
    user_id = g.user['id']

    db = get_db()
    requests =  db.execute(
        'SELECT * FROM repairment WHERE customer_id = ?', (g.user['id'],)
    ).fetchall()
    id = [i[0] for i in requests]
    status = [i[5] for i in requests]
    product_ids = [i[2] for i in requests]
    product_names = []
    for i in product_ids:
        product =  db.execute(
        'SELECT * FROM product WHERE id = ?', (i,)
        ).fetchone()
        product_name = product["model"]
        product_names.append(product_name)
    data = {
        "id": id,
        "status": status,
        "product_name": product_names
    }
    return render_template('customer/customer_view_requests.html', data = data, size = len(status) )

@bp.route('/get_complaints',methods =('GET','POST'))
def get_complaints():
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

    status = req["status"]

    if status != "waitingForCustomerDecision":
        return "Current status of the request is not applicable for this action!"

    product_id = req["product_id"]
    prelim = req["prelim"]

    product = db.execute(
        'SELECT * FROM product WHERE id = ?', (product_id,)
    ).fetchone()

    product_model = product["model"]
    data = {
        "name": product_model,
        "prelim" : prelim,
        "req_id" : request_id
    }

    return render_template('customer/customer_see_preliminary.html', data=data)

@bp.route('/customer_evaluate', methods=['GET','POST'])
def customer_evaluate():
    db = get_db()
    user_id = g.user['id']
    request_id = request.args["requests"]
    repairment =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (request_id,)
    ).fetchone()
    product_id = repairment["product_id"]

    parts_repairment = db.execute(
        'SELECT * FROM parts_repairment WHERE product_id = ?', (product_id,)
    ).fetchall()

    product = db.execute(
        'SELECT * FROM product WHERE id = ?', (product_id,)
    ).fetchone()
    product_name = product["model"]
    statuses = [[i[3] for i in parts_repairment]][0]
    part_ids = [[i[1] for i in parts_repairment]][0]

    part_names = []
    for ids in part_ids:
        parts = db.execute(
        'SELECT * FROM parts WHERE id = ?', (ids,)
        ).fetchone()

        part_name = parts["name"]
        part_names.append(part_name)

    length = len(statuses)
    data = {
        "product_id": product_id,
        "status": statuses,
        "part_names": part_names,
        "part_ids": part_ids,
        "len": length,
        "product_name": product_name,
        "repairment_id": request_id
    }
    return render_template('customer/customer_evaluate.html',data=data)
    # Request status closed =>> satisfactory
    #Request status complained ==>>create complaint

@bp.route('/evaluate_satisfactory')
def evaluate_satisfactory():
    db = get_db()
    user_id = g.user['id']
    repairment_id = request.args["repairment_id"]
    db.execute(
    'UPDATE repairment SET status = "closed"\
    WHERE id = ?', (repairment_id,)
    )
    db.commit()
    return redirect(url_for('customer.welcome'))

@bp.route('/create_complaint')
def create_complaint():
    db = get_db()
    user_id = g.user['id']
    repairment_id = request.args["repairment_id"]
    db.execute(
    'UPDATE repairment SET status = "complained"\
    WHERE id = ?', (repairment_id,)
    )
    db.commit()

    data = {
        "repairment_id": repairment_id
    }

    return render_template('customer/complaint.html', data = data)

@bp.route('/submit_complaint')
def submit_complaint():
    db = get_db()
    customer_id = g.user['id']
    repairment_id = request.args["repairment_id"]
    complaint_text = request.args["complaint_text"]
    
    db.execute(
        'INSERT INTO complaint (problem, current_status, repairment_id, \
            customer_id) VALUES (?, ?, ?, ?)',
        (complaint_text, "waiting", repairment_id, customer_id)
    )
    db.commit()
    return redirect(url_for('customer.get_requests'))

@bp.route('/recievedTheProduct',methods=['GET','POST'])
def recievedTheProduct():
    db = get_db()
    user_id = g.user['id']
    request_id = request.args["requests"]
    req =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (request_id,)
    ).fetchone()

    status = req["status"]
    product_id = req["product_id"]
    req_status = req["status"]
    if req_status == "repairedItemShippedToCustomer":
        #statusu waiting for evaluation yapicaz
        # shippingi delivered yapicaz
        # recieve date yi simdiki zaman yapicaz

        db.execute(
            'UPDATE repairment SET status = "waitingForCustomerEvaluation"\
            WHERE id = ?', (request_id,)
        )

        db.commit()

        db.execute(
            'UPDATE shipping SET receive_date = ? ,status = "delivered"\
            WHERE status = "delivered" AND repairment_id = ?', (date.today(), request_id)
        )

        db.commit()

        return redirect(url_for('customer.get_requests'))
    elif req_status == "newItemShippedToCustomer":
        # statusu closed yapicaz
        # shippidi delivered yapciaz
        # delivery datayi bugun yapicaz
        db.execute(
            'UPDATE repairment SET status = "closed"\
            WHERE id = ?', (request_id,)
        )

        db.commit()

        db.execute(
            'UPDATE shipping SET receive_date = ? ,status = "delivered"\
            WHERE status = "delivered" AND repairment_id = ?', (date.today(), request_id)
        )

        db.commit()

        return redirect(url_for('customer.get_requests'))
    else:
        return "Current status of the request is not applicable for this action!"


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


    db.execute(
        'INSERT INTO messages (text,complaint_id ,receiver_id, sender_id) VALUES (?, ?, ?, ?)' , (message,comp_id,receiver_id,user_id)
    )

    db.commit()

    return customer_chat_page(comp_id)

@bp.route('/decision_renew', methods = ['GET','POST'])
def decision_renew():
    # change the old product status to return
    # create a new product with same attributes for user
    # create a shippment for this new product
    # change status of the request
    db = get_db()
    user_id = g.user['id']
    request_id = request.args["id"]

    req =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (request_id,)
    ).fetchone()

    product_id = req["product_id"]
    customer_id = req["customer_id"]
    req_status = req["status"]
    technician_id = req["technician_id"]

    # get the information about old product
    old_product = db.execute(
        'SELECT * FROM product WHERE id = ?', (product_id,)
    ).fetchone()


    # add new product with the same old product attirbutes
    db.execute(
        'INSERT INTO product (customer_id, model, color, \
        years_of_warranty,time_of_buying,price,cat_id,status) VALUES (?, ?, ?, ?, ?, ?, ?,"exists")',\
        (old_product['customer_id'], old_product['model'], old_product['color'],\
        old_product['years_of_warranty'], date.today(), old_product['price'], old_product['cat_id'])
    )

    db.commit()

    # change the status of the old product to return
    db.execute(
            'UPDATE product SET status = "return"\
            WHERE id = ?', (product_id,)
    )

    db.commit()

    # change the status of the request to "newItemShippedToCustomer"
    db.execute(
            'UPDATE repairment SET status = "newItemShippedToCustomer"\
            WHERE id = ?', (request_id,)
    )

    db.commit()

    # create new shipment to from technician to customer
    db.execute(
            'INSERT INTO shipping (delivery_date, repairment_id, customer_id, \
                technician_id, status) VALUES (?, ?, ?, ?, ?)',
            (date.today(), request_id, customer_id, technician_id, "onWay")
        )
    db.commit()

    # get the id of the new product
    new_product =  db.execute(
            'SELECT * FROM product WHERE customer_id = ? AND model = ? AND color = ? AND years_of_warranty = ? AND \
            time_of_buying = ? AND price = ? AND cat_id = ? AND status = "exists"', \
            (old_product['customer_id'], old_product['model'], old_product['color'],\
            old_product['years_of_warranty'], date.today(), old_product['price'], old_product['cat_id'])
        ).fetchone()

    size =  db.execute(
            'SELECT COUNT(*) FROM parts'
        ).fetchone()[0]

    if old_product['model'] == "phone":
        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 1, new_product[0], "screen")
        )
        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 2, new_product[0], "battery")
        )

        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 3, new_product[0], "CPU")
        )

        db.commit()
    elif old_product['model'] == "tablet":
        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 1, new_product[0], "screen")
        )
        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 2, new_product[0], "battery")
        )

        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 3, new_product[0], "CPU")
        )

        db.commit()
    elif old_product['model'] == "laptop":
        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 1, new_product[0], "screen")
        )
        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 2, new_product[0], "battery")
        )

        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 3, new_product[0], "CPU")
        )

        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 4, new_product[0], "GPU")
        )

        db.commit()

    return redirect(url_for('customer.get_requests'))

@bp.route('/decision_return', methods = ['GET','POST'])
def decision_return():
    # change the status of product return
    # change the status of request to repairedItemShippedToCustomer

    db = get_db()
    user_id = g.user['id']
    request_id = request.args["id"]

    req =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (request_id,)
    ).fetchone()

    product_id = req["product_id"]
    customer_id = req["customer_id"]
    req_status = req["status"]
    technician_id = req["technician_id"]

    # update request status
    db.execute(
        'UPDATE repairment SET status = "closed" WHERE id = ?', (request_id,)
    ).fetchone()

    db.commit()

    # update the product status
    db.execute(
        'UPDATE product SET status = "return" WHERE id = ?', (product_id,)
    ).fetchone()

    db.commit()

    return redirect(url_for('customer.get_requests'))


@bp.route('decision_repair', methods = ['GET','POST'])
def decision_repair():
    # change the status of request
    db = get_db()
    user_id = g.user['id']
    request_id = request.args["id"]

    req =  db.execute(
        'SELECT * FROM repairment WHERE id = ?', (request_id,)
    ).fetchone()

    product_id = req["product_id"]
    customer_id = req["customer_id"]
    req_status = req["status"]
    technician_id = req["technician_id"]

    # update request status
    db.execute(
        'UPDATE repairment SET status = "waitingForDetailedReport" WHERE id = ?', (request_id,)
    ).fetchone()

    db.commit()

    return redirect(url_for('customer.get_requests'))
