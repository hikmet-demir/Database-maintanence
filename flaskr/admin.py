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


@bp.route('/find_range',methods =('GET','POST'))
def find_range():
    beginning = int(request.args['beginning'])
    end = int(request.args['end'])

    db = get_db()

    technicians = db.execute(
            'SELECT id, number FROM ( \
                SELECT technician_id as id, COUNT(*) as number\
                FROM repairment\
                GROUP BY technician_id)\
            WHERE number >= ? AND number <= ?',(beginning,end)
            ).fetchall()

    id = [[i[0]] for i in technicians]
    number = [[i[1]] for i in technicians]

    data = {
        "id": id,
        "number": number
    }


    return render_template('admin/find_range.html', data = data, size = len(id)) 


@bp.route('/find_customers',methods =('GET','POST'))
def find_customers():
    letters = request.args['letters']

    db = get_db()

    customers = db.execute("select * from user where first_name like ? and\
    user_type = 'customer'", (letters+'%',)
    ).fetchall()

    id = [[i[0]] for i in customers]
    name = [[i[4]] for i in customers]

    data = {
        "id": id,
        "name": name
    }

    return render_template('admin/find_customer_name.html', data = data, size = len(id))


@bp.route('/find_technician',methods =('GET','POST'))
def find_technician():
    db = get_db()

    technicians = db.execute('SELECT * \
            FROM technician_count \
            WHERE number = (\
            SELECT max(number) FROM technician_count GROUP BY id)'
    ).fetchall()

    id = [[i[0]] for i in technicians]
    number = [[i[1]] for i in technicians]

    data = {
        "id": id,
        "number": number
    }

    return render_template('admin/see_max_technician.html', data = data, size = len(id))

@bp.route('/find_assistant',methods =('GET','POST'))
def find_assistant():
    db = get_db()

    assistants = db.execute('SELECT * \
            FROM assistant_count \
            WHERE number = (\
            SELECT max(number) FROM assistant_count GROUP BY id)'
    ).fetchall()

    id = [[i[0]] for i in assistants]
    number = [[i[1]] for i in assistants]

    data = {
        "id": id,
        "number": number
    }

    return render_template('admin/see_max_assistant.html', data = data, size = len(id))


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
        'INSERT INTO product (customer_id,model,color,years_of_warranty,time_of_buying,price,cat_id, status)\
        VALUES (?,?,?,?,?,?,?, "exists")', (customer_id,product_model,product_color,product_warranty,\
            product_time_of_buying, product_price, product_cat)
    )

    db.commit()

    product =  db.execute(
            'SELECT * FROM product WHERE customer_id = ? AND model = ? AND color = ? AND years_of_warranty = ? AND \
                time_of_buying = ? AND price = ? AND cat_id = ? ', (customer_id, product_model, product_color, product_warranty, \
                    product_time_of_buying, product_price, product_cat)
        ).fetchone()

    size =  db.execute(
            'SELECT COUNT(*) FROM parts'
        ).fetchone()[0]

    if product_model == "phone":
        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 1, product[0], "screen")
        )
        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 2, product[0], "battery")
        )

        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 3, product[0], "CPU")
        )

        db.commit()
    elif product_model == "tablet":
        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 1, product[0], "screen")
        )
        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 2, product[0], "battery")
        )

        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 3, product[0], "CPU")
        )

        db.commit()
    elif product_model == "laptop":
        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 1, product[0], "screen")
        )
        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 2, product[0], "battery")
        )

        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 3, product[0], "CPU")
        )

        db.commit()

        db.execute(
            'INSERT INTO parts (id, product_id, name) VALUES (?, ?, ?)',
            (size + 4, product[0], "GPU")
        )

        db.commit()
    else:
        return "Model can be tablet, phone or a laptop!"

    
    return redirect(url_for('admin.welcome'))