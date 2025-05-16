from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    response = requests.get("https://rickandmortyapi.com/api/character?page=1")
    data = response.json()
    characters = data['results']

    return render_template('index.html', characters=characters)

@app.route('/character/<int:id>')
def character_detail(id):
    response = requests.get(f"https://rickandmortyapi.com/api/character/{id}")
    character = response.json()
    return render_template('character.html', character=character)

if __name__ == '__main__':
    app.run(debug=True)


#note: limit the number of characters