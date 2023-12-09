from flask import Flask, jsonify
from pymongo import MongoClient

# Create a MongoClient to run the MongoDB instance.
client = MongoClient("mongodb://localhost:27017/")

# Create or access a database called 'mydatabase'.
db = client['mydatabase'] 

# Create or access a collection for cars and buses.
car_collection = db['cars']
bus_collection = db['buses']

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register_vehicle():
    data = request.json
    vehicle_id = data.get('vehicle_id')
    vehicle_type = data.get('vehicle_type')
    if not vehicle_id or not vehicle_type:
        return jsonify({"error": "Vehicle ID and type are required"}), 400

    # Add a timestamp to the registration data
    data['timestamp'] = time.time()

    # Insert the registration data into the appropriate MongoDB collection
    if vehicle_type == 'car':
        car_collection.insert_one(data)
    elif vehicle_type == 'bus':
        bus_collection.insert_one(data)
    else:
        return jsonify({"error": "Invalid vehicle type"}), 400

    return jsonify({"message": f"Vehicle {vehicle_id} registered successfully"}), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    current_time = time.time()
    max_age_seconds = 10 * 60  # 10 minutes

    # Retrieve all registrations from the MongoDB collections
    car_documents = car_collection.find()
    bus_documents = bus_collection.find()

    # Filter out any expired registrations
    cars = {doc['_id']: doc for doc in car_documents if current_time - doc['timestamp'] <= max_age_seconds}
    buses = {doc['_id']: doc for doc in bus_documents if current_time - doc['timestamp'] <= max_age_seconds}

    return jsonify({"cars": cars, "buses": buses})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
