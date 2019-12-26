from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('customer', __name__, url_prefix='/customer')

@bp.route('/aa',methods =('GET','POST'))
def ddd():
    return "hikmet"

@bp.route('/get_details',methods =('GET','POST'))
def get_details():
    products = request.args["products"]
    
    render_template('customer/customer_get_details.html'
        ,data = ["aaa","bbb","ccc"],size = 3)
    return "asdasd"


@bp.route('/create_request',methods =('GET','POST'))
def create_request():
    products = request.args["products"]
    
    render_template('customer/customer_get_details.html'
        ,data = ["aaa","bbb","ccc"],size = 3)
    return "asdasd"