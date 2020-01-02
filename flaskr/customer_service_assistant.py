import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('customer_service_assistant', __name__, url_prefix='/customer_service_assistant')

@bp.route('/welcome',methods =('GET','POST'))
def welcome(choice = 0):    # (choice == zero) print my complaints : print unassigned complaints
    user_id = g.user['id']

    db = get_db()

    checked_rbs = []

    if choice:
        checked_rbs.append("checked")
        checked_rbs.append("")
        complaints =  db.execute(
                'SELECT * FROM complaint c, repairment r, product p WHERE c.customer_service_asisstant_id IS NULL and c.repairment_id = r.id and r.product_id = p.id'
        ).fetchall()
    else:
        checked_rbs.append("")
        checked_rbs.append("checked")
        complaints =  db.execute(
                'SELECT * FROM complaint c, repairment r, product p WHERE c.customer_service_asisstant_id = ? and c.repairment_id = r.id and r.product_id = p.id', (user_id,)
        ).fetchall()

    # outer brackets are required, it doesnt work without them somehow
    # thats why id's are shown in the bracets on the website
    id = [i["id"] for i in complaints]
    problem = [i["problem"] for i in complaints]
    model = [i["model"] for i in complaints]
    current_status = [i["current_status"] for i in complaints]
    data = {
        "id": id,
        "problem": problem,
        "model": model,
        "current_status": current_status
    }
    #return str(data)
    return render_template('customer_service_assistant/customer_service_assistant_welcome.html', data = data, size = len(id), checked = checked_rbs)

@bp.route('/customer_service_complaint_details',methods =('GET','POST'))
def customer_service_complaint_details(comp_id = None):

    user_id = g.user['id']

    db = get_db()

    if comp_id == None:
        comp_id = int(request.args["comp_id"])

    complaint_infos =  db.execute(
            'SELECT * FROM complaint WHERE id = ?', (comp_id,)
    ).fetchone()

    id = complaint_infos["id"]
    problem = complaint_infos["problem"]
    current_status = complaint_infos["current_status"]
    final_status = complaint_infos["final_status"]
    repairment_id = complaint_infos["repairment_id"]
    customer_service_asisstant_id = complaint_infos["customer_service_asisstant_id"]
    customer_id = complaint_infos["customer_id"]

    # outer brackets are required, it doesnt work without them somehow
    # thats why id's are shown in the bracets on the website
    data = {
        "id": id,
        "problem": problem,
        "current_status": current_status,
        "final_status": final_status,
        "repairment_id": repairment_id,
        "customer_service_asisstant_id": customer_service_asisstant_id,
        "customer_id": customer_id
    }
    return render_template('customer_service_assistant/customer_service_complaint_details.html', data = data)

@bp.route('/customer_service_assistant_chat_page',methods =('GET','POST'))
def customer_service_assistant_chat_page(complaint_MADAFAKA = None):
    if complaint_MADAFAKA == None:
        complaint_id = request.args["comp_id"]
    else:
        complaint_id = complaint_MADAFAKA
    user_id = g.user['id']
    #user_id = 99

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
    return render_template('customer_service_assistant/customer_service_assistant_chat_page.html', data = data, size = len(idd), complaint_id = complaint_id )

@bp.route('/insert_message',methods=['GET','POST'])
def insert_message():
    #return str(g.user['id'])
    comp_id = request.form['subject']
    user_id = g.user['id']

    message = str(request.form['message'])

    db = get_db()

    receiver_id =  db.execute(
        'SELECT customer_id FROM complaint WHERE id = ?', (comp_id,)
    ).fetchone()[0]

    db.execute(
        'INSERT INTO messages (text,complaint_id ,receiver_id, sender_id) VALUES (?, ?, ?, ?)' , (message,comp_id,receiver_id,user_id)
    )

    db.commit()

    return customer_service_assistant_chat_page(comp_id)

@bp.route('/customer_service_finalize',methods=['GET','POST'])
def customer_service_finalize():
    final_status = request.form['final_status']
    comp_id = request.form['complaint_id']

    db = get_db()

    db.execute(
        'UPDATE complaint SET final_status = ? WHERE id= ?', (final_status,comp_id)
    )

    db.commit()

    return customer_service_complaint_details(comp_id)

@bp.route('/write_assigned',methods=['GET','POST'])
def write_assigned():
    #return "assigned"
    return welcome(0)

@bp.route('/write_unassigned',methods=['GET','POST'])
def write_unassigned():
    return welcome(1)

@bp.route('/customer_service_manage',methods=['GET','POST'])
def customer_service_manage():
    comp_id = request.args['comp_id']
    user_id = g.user['id']

    db = get_db()

    db.execute(
        'UPDATE complaint SET customer_service_asisstant_id = ? WHERE id = ? and customer_service_asisstant_id IS NULL', (user_id,comp_id)
    )
    db.commit()

    return welcome(0)
