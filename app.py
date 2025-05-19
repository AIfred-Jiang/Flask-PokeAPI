from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    characters = []  # Initialize an empty list

    for page in range(1, 11):
        response = requests.get(f"https://rickandmortyapi.com/api/character?page={page}")
        data = response.json()
        characters.extend(data['results'])  # Add characters from the current page to the list


    return render_template('index.html', characters=characters)


@app.route('/character/<int:id>')
def character_detail(id):
    if id < 1 or id > 200:
        return render_template("error.html", message="Character ID must be between 1 and 200."), 404

    try:
        response = requests.get(f"https://rickandmortyapi.com/api/character/{id}")
        character = response.json()
        return render_template('character.html', character=character)
    except requests.exceptions.RequestException:
        # If API fails or something unexpected happens
        return render_template("error.html", message="Could not load character details."), 500

if __name__ == '__main__':
    app.run(debug=True)