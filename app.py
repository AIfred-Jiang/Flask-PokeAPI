from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    # Fetch the list of dog breeds
    response = requests.get('https://dogapi.dog/api-v2/breeds/list')
    data = response.json()
    breed_list = data['result']
    
    breeds = []

    for breed in breed_list:
        # Construct the breed details URL
        breed_url = f'https://dogapi.dog/api-v2/breeds/{breed["slug"]}'
        breed_response = requests.get(breed_url)
        breed_data = breed_response.json()['result']
        
        breeds.append({
            'id': breed_data['id'],
            'name': breed_data['name'],
            'image': breed_data['image']['url'],
            'description': breed_data.get('description', 'No description available'),
            'temperament': breed_data.get('temperament', 'Temperament not specified'),
            'life_span': breed_data.get('life_span', 'Life span not specified'),
            'weight': breed_data.get('weight', 'Weight not specified'),
            'height': breed_data.get('height', 'Height not specified'),
            'bred_for': breed_data.get('bred_for', 'Purpose not specified'),
            'breed_group': breed_data.get('breed_group', 'Group not specified')
        })

    return render_template("index.html", breeds=breeds)

@app.route("/breed/<int:id>")
def breed_detail(id):
    breed = next((b for b in breeds if b['id'] == id), None)
    if breed:
        return render_template("breed.html", breed=breed)
    return "Breed not found", 404

if __name__ == "__main__":
    app.run(debug=True)