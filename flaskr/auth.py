import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register_customer', methods=('GET', 'POST'))
def register_customer():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        middle_name = request.form['mid_name']
        last_name = request.form['last_name']
        phone = request.form['phone_no']
        gender = request.form['gender']
        national_id = request.form['national_id']
        city = request.form['city']
        street = request.form['street']
        apt_no = request.form['apt_no']
        district = request.form['district']
        zip_code = request.form['zip_code']
        birth_date = request.form['date_of_birth']
        user_type = 'customer'

        db = get_db()
        error = None
        

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'email is required.'
        elif not national_id:
            error = 'National ID is required.'
        elif not first_name:
            error = 'First name is required.'
        elif not last_name:
            error = 'Last name is required.'
        elif not phone:
            error = 'Phone number is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            # First insert into user table, then insert into customer with auto generated id
            db.execute(
                'INSERT INTO user (username, email, password, first_name, \
                middle_name, last_name, phone, gender, user_type ) VALUES \
                (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (username, email,generate_password_hash(password), first_name, middle_name, last_name, phone, gender, user_type)
            )
            db.commit()
            # Get the autogenerated id
            id = db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
            ).fetchone()['id']
            db.commit()
            print("id =>",id)
            db.execute(
                'INSERT INTO customer (id, national_id, city, street, apt_no, district, zip_code, birth_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (id, national_id, city, street, apt_no, district, zip_code, birth_date)
            )
            db.commit()

            return redirect(url_for('auth.login'))
        if error:
            return error

        flash(error)
    if request.method == 'GET':
        return render_template('auth/register_customer.html')

@bp.route('/register_customer_service_assistant', methods=('GET', 'POST'))
def register_customer_service_assistant():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        middle_name = request.form['mid_name']
        last_name = request.form['last_name']
        phone = request.form['phone_no']
        gender = request.form['gender']
        requirement_year = request.form['requirement_year']
        department = request.form['department']
        experience = request.form['years_of_experience']
        user_type = 'asisstant'
        
        db = get_db()
        error = None
        

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'email is required.'
        elif not first_name:
            error = 'First name is required.'
        elif not last_name:
            error = 'Last name is required.'
        elif not phone:
            error = 'Phone number is required.'
        elif not requirement_year:
            error = 'Requirement Year is required.'
        elif not department:
            error = 'Department Year is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            # First insert into user table, then insert into empleyee and asisstant with auto generated id
            db.execute(
                'INSERT INTO user (username, email, password, first_name, \
                    middle_name, last_name, phone, gender, user_type) VALUES \
                        (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (username, email,generate_password_hash(password), first_name, \
                    middle_name, last_name, phone, gender, user_type)
            )
            db.commit()
            # Get the autogenerated id
            id = db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
            ).fetchone()['id']
            db.commit()
            # insert into employee table
            db.execute(
                'INSERT INTO employee (id, requirement_year, department, \
                    years_of_experience) VALUES (?, ?, ?, ?)',
                (id, requirement_year, department, experience)
            )
            db.commit()
            # insert into customer_service_asisstant table
            db.execute(
                'INSERT INTO customer_service_asisstant (id) VALUES (?)',
                (id,)
            )

            db.commit()
        if error:
            return error

        return redirect(url_for('auth.login'))

        flash(error)
    if request.method == 'GET':
        return render_template('auth/register_customer_service_assistant.html')

@bp.route('/register_technician', methods=('GET', 'POST'))
def register_technician():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        middle_name = request.form['mid_name']
        last_name = request.form['last_name']
        phone = request.form['phone_no']
        gender = request.form['gender']
        requirement_year = request.form['requirement_year']
        department = request.form['department']
        experience = request.form['years_of_experince']
        profession = request.form['profession']
        user_type = 'technician'
        
        db = get_db()
        error = None
        

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'email is required.'
        elif not first_name:
            error = 'First name is required.'
        elif not last_name:
            error = 'Last name is required.'
        elif not phone:
            error = 'Phone number is required.'
        elif not requirement_year:
            error = 'Requirement Year is required.'
        elif not department:
            error = 'Department Year is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            # First insert into user table, then insert into empleyee and asisstant with auto generated id
            db.execute(
                'INSERT INTO user (username, email, password, first_name, \
                    middle_name, last_name, phone, gender, user_type ) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (username, email,generate_password_hash(password), \
                    first_name, middle_name, last_name, phone, gender, user_type)
            )
            db.commit()
            # Get the autogenerated id
            id = db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
            ).fetchone()['id']
            db.commit()
            # insert into employee table
            db.execute(
                'INSERT INTO employee (id, requirement_year, \
                    department, years_of_experience) VALUES (?, ?, ?, ?)',
                (id, requirement_year, department, experience)
            )
            db.commit()
            # insert into customer_service_asisstant table
            db.execute(
                'INSERT INTO technician (id, profession) VALUES (?,?)',
                (id,profession)
            )

            db.commit()
        if error:
            return error

        return redirect(url_for('auth.login'))

        flash(error)
    if request.method == 'GET':
        return render_template('auth/register_technician.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            #session.clear()
            session['user_id'] = user['id']
            user_type = db.execute(
                'SELECT user_type FROM user WHERE username = ?', (username,)
                ).fetchone()['user_type']

            if user_type == "customer":
                return render_template('customer/customer_welcome.html',data = ["aaa","bbb","ccc"],size = 3)

            elif user_type == "technician":
                return render_template('technician/technician_welcome.html',data = ["aaa","bbb","ccc"],size = 3)
            elif user_type == "asisstant":
                return render_template('customer/customer_welcome.html',data = ["aaa","bbb","ccc"],size = 3)
            elif user_type == "admin":
                return render_template('customer/admin_welcome.html',data = ["aaa","bbb","ccc"],size = 3)

        flash(error)

    return render_template('index.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view