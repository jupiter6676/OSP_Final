import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('page.html')

@app.route('/box', methods=['GET'])
def read_url(url1):
    if request.method == 'GET':
        res = requests.args.get("https://github.com/trending/python?since=monthly")

    return render_template('page.html', url1=res)

@app.route('/txt', methods=['POST'])
def read_txt():
    if request.method == 'POST':
        f = request.files['file'].read()

        return f

if __name__ == '__main__':
    app.run(debug=True)
