from flask import Flask, render_template, request
import requests
from urllib.parse import quote

app = Flask(__name__)

@app.template_filter('urlencode')
def urlencode_filter(s):
    return quote(s)


def get_all_characters():
    characters = []
    for page in range(1, 11):
        response = requests.get(f"https://rickandmortyapi.com/api/character?page={page}")
        data = response.json()
        characters.extend(data['results'])
    return characters

@app.route('/')
def index():
    characters = get_all_characters()
    return render_template('index.html', characters=characters)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    characters = get_all_characters()

    filtered = [
        char for char in characters
        if query in char['name'].lower()                                                                                                 
        or query in char['species'].lower()
        or query in char['status'].lower()
    ]

    if not filtered:
        return render_template('error.html', message=f"No results found for '{query}'."), 404

    return render_template('search.html', characters=filtered, query=query)

@app.route('/character/<int:id>')
def character_detail(id):                                  
    if id < 1 or id > 200:
        return render_template("error.html", message="Character ID must be between 1 and 200."), 404

    try:
        response = requests.get(f"https://rickandmortyapi.com/api/character/{id}")
        character = response.json()
        return render_template('character.html', character=character)
    except requests.exceptions.RequestException:
        return render_template("error.html", message="Could not load character details."), 500

if __name__ == '__main__':
    app.run(debug=True)