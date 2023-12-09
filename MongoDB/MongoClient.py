from flask import Flask, jsonify
from pymongo import MongoClient

# Create a MongoClient to run the MongoDB instance.
client = MongoClient("mongodb://localhost:27017/")

# Create or access a database called 'mydatabase'.
db = client['mydatabase'] 

# Create or access a collection called 'mycollection'.
collection = db['mycollection']

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register_vehicle():
    data = request.json
    vehicle_id = data.get('vehicle_id')
    if not vehicle_id:
        return jsonify({"error": "Vehicle ID is required"}), 400

    # Add a timestamp to the registration data
    data['timestamp'] = time.time()

    # Insert the registration data into the MongoDB collection
    collection.insert_one(data)

    return jsonify({"message": f"Vehicle {vehicle_id} registered successfully"}), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    current_time = time.time()
    max_age_seconds = 10 * 60  # 10 minutes

    # Retrieve all registrations from the MongoDB collection
    documents = collection.find()

    # Filter out any expired registrations
    vehicles = {doc['_id']: doc for doc in documents if current_time - doc['timestamp'] <= max_age_seconds}

    return jsonify(vehicles)
