from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = "YOUR_API_KEY"  # Replace with your actual API key from api-ninjas.com

# Homepage: shows list of cat names
@app.route('/')
def index():
    url = "https://api.api-ninjas.com/v1/cats"
    headers = {'X-Api-Key': API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        cats = response.json()
    else:
        cats = []
    return render_template('index.html', cats=cats)

# Detailed view: fetch full cat data by name
@app.route('/cat/<cat_name>')
def cat_detail(cat_name):
    url = f"https://api.api-ninjas.com/v1/cats?name={cat_name}"
    headers = {'X-Api-Key': API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200 and response.json():
        cat = response.json()[0]  # API returns list
    else:
        cat = {"error": "Cat not found or unavailable."}

    return render_template('cat.html', cat=cat)