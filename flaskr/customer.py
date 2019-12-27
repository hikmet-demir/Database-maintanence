from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db
import sys
from datetime import date

def diff_dates(date1, date2):
    return abs(date2-date1).days


bp = Blueprint('customer', __name__, url_prefix='/customer')

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
    
    
    return render_template('customer/customer_get_details.html'
        ,id=product_id, price=price, model=model, Color=color,
        years_of_warranty=warranty, category_name=cat_name)


@bp.route('/create_request',methods =('GET','POST'))
def create_request():
    db = get_db()
    product_id = request.args["products"][1]

    product =  db.execute(
            'SELECT * FROM product WHERE id = ?', (product_id,)
        ).fetchone()

    today = date.today()
    time_of_buying = product["time_of_buying"]
    difference_year = int(diff_dates(today, time_of_buying)/365)
    

    print ("{} days between {} and {}".format(result1, today, time_of_buying))   
    

    id = product["id"]
    model = product['model']
    warranty = product['years_of_warranty']
    
    return render_template('customer/create_request.html',
        id=product_id, model=model, years_of_warranty=warranty,
        data=["asd","asdd"])
    
@bp.route('/complete_request',methods =('GET','POST'))
def complete_request():
    product_id = request.args['product_id']
    request_type = request.args['request']
    problem = request.args['myTextBox']
    customer_id = g.user['id']

    print(product_id, file=sys.stderr)
    print(request_type, file=sys.stderr)
    print(problem, file=sys.stderr)

    if request_type == 'repair':
        db = get_db()

        # SIMDILIK TEKNISYENI ELIMLE YERLESTIRDIM
        # DEMAND SILINMELI
        
        db.execute(
                'INSERT INTO repairment (technician_id, product_id, customer_id, \
                    problem, demand) VALUES (?, ?, ?, ?, ?)',
                (1, product_id, customer_id, problem, "repair")
            )

        db.commit()
    else:
        print("ses")
        # we need to handle this case later!!!
    
    return redirect(url_for('customer.welcome'))
    

