from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Configurar la conexión a MongoDB
client = MongoClient('mongodb+srv://romerogallegos:12345@cluster0.k3nmtjk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')  # Cambia la URL si tu MongoDB está en otro lugar
db = client['geolocation_db']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location', methods=['POST'])
def location():
    data = request.get_json()
    latitude = round(data.get('latitude'), 5)  # Redondear a 5 decimales
    longitude = round(data.get('longitude'), 5)  # Redondear a 5 decimales

    print(f"Latitud: {latitude}")
    print(f"Longitud: {longitude}")
    
    # Verificar si la colección existe, si no, crearla
    collection_name = 'locations'
    if collection_name not in db.list_collection_names():
        collection = db.create_collection(collection_name)
        print("Colección creada")
    else:
        collection = db[collection_name]
        print("Colección existente")
    
    # Insertar los datos en MongoDB
    location_data = {
        'latitude': latitude,
        'longitude': longitude
    }
    collection.insert_one(location_data)
    
    return jsonify({'status': 'success', 'latitude': latitude, 'longitude': longitude})

if __name__ == '__main__':
    app.run(debug=True)
