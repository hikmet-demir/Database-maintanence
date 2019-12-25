from flask import Flask, request, render_template

app = Flask(__name__,static_url_path="/static/")

@app.route('/')

def hello():
    return render_template('index.html', index=1)

if __name__ =="__main__":
    app.run(host="localhost",port="8000",debug=True)