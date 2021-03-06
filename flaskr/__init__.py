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

    @app.route('/')
    def index():
        return render_template('index.html', index=1)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import customer
    app.register_blueprint(customer.bp)

    from . import technician
    app.register_blueprint(technician.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import customer_service_assistant
    app.register_blueprint(customer_service_assistant.bp)

    return app
