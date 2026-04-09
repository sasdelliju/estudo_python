# pip install flask
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Python rodando no SAP BTP 🚀"