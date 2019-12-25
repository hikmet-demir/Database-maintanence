import os

from flask import Flask, request, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True,
    static_url_path="/static/")
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        return render_template('index.html', index=1)

    @app.route('/sign_up_customer',methods = ['GET','POST'])
    def sign_up_customer():
        return render_template('sign_up_customer.html') 

    @app.route('/sign_up_customer_service_assistant',methods = ['GET','POST'])
    def sign_up_customer_service_assistant():
        return render_template('sign_up_customer_service_assistant.html') 

    @app.route('/sign_up_technician',methods = ['GET','POST'])
    def sign_up_technician():
        return render_template('sign_up_technician.html') 
    from . import db
    db.init_app(app)

    return app

