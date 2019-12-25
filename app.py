from flask import Flask, request, render_template

app = Flask(__name__,static_url_path="/static/")

@app.route('/')

def hello():
    return "SIMKIIII HİKOOO MUROO AHMOO"


if __name__ =="__main__":
    app.run(host="localhost",port="8000",debug=True)