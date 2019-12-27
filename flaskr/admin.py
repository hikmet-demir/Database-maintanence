from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db
import sys

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/welcome',methods =('GET','POST'))
def welcome():
    db = get_db()

    customers =  db.execute(
            'SELECT customer.id, user.first_name FROM customer, user WHERE customer.id == user.id'
        ).fetchall()
    
    return render_template('admin/admin.html', data = customers) 


@bp.route('/add_product',methods =('GET','POST'))
def add_product():
    customer_id = int(request.args['customer'])
    product_model = str(request.args['model'])
    product_color = str(request.args['color'])
    product_warranty = int(request.args['warranty'])
    product_time_of_buying = request.args['timeofbuying']
    product_price = float(request.args['price'])
    product_cat = int(request.args['cat_id'])


    db = get_db()

    db.execute(
        'INSERT INTO product (customer_id,model,color,years_of_warranty,time_of_buying,price,cat_id)\
        VALUES (?,?,?,?,?,?,?)', (customer_id,product_model,product_color,product_warranty,\
            product_time_of_buying, product_price, product_cat)
    )

    db.commit()
    
    return redirect(url_for('admin.welcome'))