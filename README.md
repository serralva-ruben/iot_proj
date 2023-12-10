# iot_proj

-Adin Suljkanovic

-Eldar Memikj

-Ruben Serralva

-Youngsub Lee

In this file we are going to explain how the project works.

**Lets start from the flow car+bus+map as it should simulate the bus and the car driving around the map.**

First, we have an inject node which injects every second and trigers the function Random_location. The purpose of this function is to place the car and the bus randomly around the center point (in our case we chosed Luxembourg ville) in order to simulate the movement of the bus and the car.
So as a payload this function sends data for the car and the bus (name, coordinates and data for the map such as the icon and iconcolor), then we also send data descriving the zone A to draw it on the map (coordinates of center point, color of the circle, radius).
This Random_location is connected to three nodes, lets start with the world map node, the purpose of this node is to show the map in the ui dashboard so that we can visualize the location of the car and the bus and also the zoneA.
Then there's two other nodes, a filter car data and a filter bus data, because the Random_location node function returns 3 objects (one for the bus, one for the car and one for the zone) and since we only car about the car data to send as a request to the car server and only about the bus data to send as a request to the bus server, the purpose of these nodes is to filter and pick only the data we desire, this is done using the find function in javascript and we search for the object with the wanted name.
Then we have two coap request nodes, these nodes will send a coap request to their respective servers (one for the bus and one for the case), and to finish with this flow, in the end we have two debug nodes for debugging and visualizing sent requests.

**Now we are going to talk about the bus and car server.**

These servers are programmed in python and are coap servers, they were implemented using the coapthon library as asked.
we can address boss servers at the same time since they are very similar besides the fact that the bus server also send maqtt messages.
The coapserver.py launches the server.
Then we have SmartBus13Resources.py and SmartCar1Resources.py, these two files have the resources for the bus and the car respectively.
In these two in the contructor first we try to connect to the mongo database by calling the method initialize_mongo_client from the constructor, then we have a function for a PUT request, in this function first we load the data from the request sent by our node_red flow chart, then we set the name and location of the resource, then we try to insert a document inside the respective mongo collection containing this data (name, location and a timestamp).
Then we check wether the vehicle in question was inside the area, this is done using the is_inside_area function, which will take the location of the vehicle, the center of the zone and the radius of the zone as parameters, then it will calculate there the vehicle is inside by using the Haversine Formula, this way we can know the distance from the vehicle and the center of the area and check wether it is inferior or equal to the radius, and return true or false based on that check.
Then if it is inside the zone a then we set in_zone_a to true and we call update_resdir2 which will send a put request to the resdir2 in order to register the vehicle, otherwise it will set in_zone_a to false.
Then the part that the car server differs from the bus server is that the bus server will always publish a mqtt message with the name and location of the bus to the topic "bus13/location" while the car won't.

**Now we can talk about the resdir2** 

It is also a coap server implemented in python using coapthon, it has a VehicleRegistrationResource stored inside VehiculeRegistrationResource.py.
This resource can receive a put request to register a vehicle, it will first load the data of the request (containing the vehicle to register data), then it will create a timestamp which will be used as the key in our dictionnary, the value of the entry is the vehicle data, after registering the vehicle in the dictionary, the function cleanup_registrations will be called, this function will go over every key in the dictionary and delete those that are older than 10 minutes (600 seconds).
Then it will publish a message over mqtt to the topic "vehicles/zone_a" saying that the vehicle entered the zone A (since in order for the resdir to receive a put request it means that the vehicle entered the zone in first place) and this message will be received by the App client so that it is notified that the vehicle entered the zone A.

**App Client flow chart**

Now we are going to talk about the App client flow chart, first we have a mqtt in node, the purpose of this node is to receive the messages published by the ResDir2, these messages are the notifications saying that a vehicle entered the zoneA, then connected to this node we have a debug node and a function, the purpose of this function is to check wether the message has the vehicle_id "SmartBus13" and we also perform an additional check to see if it contains status of "entered_zone_a", if this is true we set "processBusUpdates" to true.
We also want to make sure that "processBusUpdates" is always set to false in the beginning, this is why we have an inject note that launches a function that sets "processBusUpdates" to false in the beginning.
Then we have a mqtt in node that will listen to the location of the bus that is connected to a function, if the bus entered the zone "processBusUpdates" will be true, so in this function we check "processBusUpdates", and if it is true we take the location received from our mqtt in node and we send as a payload a message containing the latitude and longitude of the bus, otherwise if "processBusUpdates" is false it means the bus hasn't entered the zone A yet and because of this we send a message saying "not subscribed", then this node is connected to a text node, its purpose if to show the location of the bus in the dashboard ui in the event of the bus entering the zone A and we subscribing to its location.

***Bullet points Overview***

**Functionality**

The key functions are:

- Simulate movement of vehicles and generate location data
- Display real-time locations of vehicles on a map 
- Define geofenced Zone A and detect when vehicles enter it
- Send notifications when entries to Zone A occur, especially for the bus
- Start tracking the bus once it enters Zone A
- Store all vehicle location history in a database

**Components**

The main components leveraged are:

- Node-RED: Front-end interface for data visualization and MQTT communication
- Python CoAP Servers: Backend logic to process vehicle data 
- MongoDB: Storage for vehicle location history
- MQTT Protocol: Message passing between interfaces

**Node-RED Workflows**

The Node-RED flows support two key interfaces:

1. Location Simulation and Map Display
    - Randomly generates coordinate locations
    - Sends locations to Python CoAP vehicle servers
    - Displays vehicles on a Luxembourg map
    
2. Zone A Entry Notifications and Bus Tracking
    - Listens for MQTT notifications of Zone A entries 
    - Specifically tracks bus location after Zone A entry
    - Displays real-time bus locations on interface

**Information Flow**

The overall workflow is:

1. Random location generation 
2. CoAP servers save locations, check Zone A, notify on entry
3. MQTT triggers tracking when bus enters Zone A   
4. Node-RED displays real-time bus locations
5. All data saved to MongoDB
