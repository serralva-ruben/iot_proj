***IoT Smart Vehicle Tracking System***

**Project Overview**
This IoT Smart Vehicle Tracking System is designed to monitor and track the locations of a smart car and a smart bus within Luxembourg. The system uses a combination of Node-RED for front-end interaction and visualization, Python-based CoAP servers for handling vehicle data, and MQTT for communication between different components.

**Technologies Used**
Node-RED: For creating flow-based applications and handling MQTT communications.
Python: For backend logic and CoAP server implementation.
CoAPthon: Python library for CoAP server functionality.
MongoDB: Database for storing vehicle location data.
MQTT Protocol: For messaging between servers and Node-RED client.

**Solution Description**

*Node-RED Flows*
-Interface 1 (Car and Bus Location Simulation and Display)-
Inject Node (Update_location): Triggers the flow at regular intervals.
Function Node (Random_location): Generates random coordinates for the smart car and bus within Luxembourg's boundaries and prepares data for the world map.
CoAP Request Nodes: Sends the generated location data to the respective CoAP servers for the smart car and bus.
Worldmap Node (Luxembourg_map): Displays the current locations of the smart car and bus, as well as Zone A's boundary.
Debug Nodes: For logging and debugging purposes.
-Interface 2 (App Client for Notifications)-
MQTT In Node (mqtt_notification_from_ResDir): Listens for MQTT messages on vehicles/zone_a, indicating a vehicle has entered Zone A.
Function Node (function_check_if_bus): Checks if the notification is for the smart bus. If yes, it sets a flag to start processing bus location updates.
MQTT In Node (mqtt_app_to_bus): Subscribes to bus13/location to receive location updates of the smart bus.
Function Node (function_process_bus_updates): Processes incoming bus location updates and prepares them for display.
Text Node (Result_text): Displays the smart bus location on the Node-RED dashboard.
Debug Nodes: For logging and debugging purposes.
             
*Backend (CoAP Servers)*
-Car and Bus Servers-
Hosts CoAP resources (SmartCar1Resources and SmartBus13Resources).
Receives location updates from Interface 1.
Registers vehicle data in MongoDB.
Checks if vehicles are within Zone A and updates status.
Notifies ResDir2 server if a vehicle enters Zone A.
-ResDir2 Server-
Registers vehicles entering Zone A.
Sends MQTT notifications to Interface 2, informing it about vehicles entering Zone A.
             
*System Workflow*
Location Simulation: Interface 1 simulates the movement of the smart car and bus, sending their locations to the respective CoAP servers.
Zone Monitoring: The CoAP servers monitor whether the vehicles enter Zone A.
Notification and Tracking: When a vehicle, especially the smart bus, enters Zone A, Interface 2 receives a notification. If the bus enters Zone A, Interface 2 starts displaying its real-time location.
Data Storage: Vehicle locations and statuses are stored in MongoDB, providing a history of vehicle movements and Zone A entries.
