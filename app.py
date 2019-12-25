from flask import Flask, request, render_template

app = Flask(__name__,static_url_path="/static/")

@app.route('/')
def hello():
    return render_template('index.html', index=1)

@app.route('/sign_up_customer',methods = ['GET','POST')
def simki():
    return render_template('sign_up_customer.html') 

@app.route()

if __name__ =="__main__":
    app.run(host="localhost",port="8000",debug=True)