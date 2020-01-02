import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('customer_service_assistant', __name__, url_prefix='/customer_service_assistant')

@bp.route('/welcome',methods =('GET','POST'))
def welcome():
    #user_id = g.user['id']
    user_id = 99
    db = get_db()

    #return str(user_id)

    complaints =  db.execute(
            'SELECT * FROM complaint c, repairment r, product p WHERE c.customer_service_asisstant_id = ? and c.repairment_id = r.id and r.product_id = p.id', (user_id,)
    ).fetchall()

    # outer brackets are required, it doesnt work without them somehow
    # thats why id's are shown in the bracets on the website
    id = [i["id"] for i in complaints]
    problem = [i["problem"] for i in complaints]
    model = [i["model"] for i in complaints]
    data = {
        "id": id,
        "problem": problem,
        "model": model
    }
    #return str(data)
    return render_template('customer_service_assistant/customer_service_assistant_welcome.html', data = data, size = len(id))

@bp.route('/customer_service_complaint_details',methods =('GET','POST'))
def customer_service_complaint_details():
    #return "selammm"
    #user_id = g.user['id']
    user_id = 99
    db = get_db()

    comp_id = int(request.args["comp_id"])
    #return str(user_id)

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
