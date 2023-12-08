from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# This dictionary will store the vehicle registrations along with timestamps
vehicle_registrations = {}

@app.route('/register', methods=['PUT'])
def register_vehicle():
    data = request.json
    vehicle_id = data.get('vehicle_id')
    if not vehicle_id:
        return jsonify({"error": "Vehicle ID is required"}), 400

    # Add a timestamp to the registration data
    data['timestamp'] = time.time()
    vehicle_registrations[vehicle_id] = data
    return jsonify({"message": f"Vehicle {vehicle_id} registered successfully"}), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    current_time = time.time()
    max_age_seconds = 10 * 60  # 10 minutes

    # Remove expired registrations
    expired_keys = [key for key, val in vehicle_registrations.items() if current_time - val['timestamp'] > max_age_seconds]
    for key in expired_keys:
        del vehicle_registrations[key]

    return jsonify(vehicle_registrations)

def main():
    app.run(host='127.0.0.1', port=5000, debug=True)

if __name__ == '__main__':
    main()
