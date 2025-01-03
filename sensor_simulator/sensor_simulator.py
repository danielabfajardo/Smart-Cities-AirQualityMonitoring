import paho.mqtt.client as mqtt
import random
import time
import json

# MQTT Server Parameters
#MQTT_CLIENT_ID = "simulated_python_sensor"
MQTT_BROKER = "mosquitto" 
MQTT_PORT = 1883
MQTT_TOPIC = "/smartcities/airquality"

# Predefined Cities with GPS Coordinates
CITIES = [
    {"name": "Songdo", "latitude": 37.3879, "longitude": 126.6503},
    {"name": "Amsterdam", "latitude": 52.3676, "longitude": 4.9041},
    {"name": "San Francisco", "latitude": 37.7749, "longitude": -122.4194},
    {"name": "Singapore", "latitude": 1.3521, "longitude": 103.8198},
    {"name": "Copenhagen", "latitude": 55.6761, "longitude": 12.5683},
]

# Sensor measurement range constants
MIN_PM2_5 = 0
MAX_PM2_5 = 500
MIN_PM10 = 0
MAX_PM10 = 500
MIN_CO2 = 400
MAX_CO2 = 1000
MIN_NO2 = 0
MAX_NO2 = 500

# Simulate temperature and humidity
def simulate_temperature():
    return round(random.uniform(20.0, 30.0), 1)

def simulate_humidity():
    return round(random.uniform(40.0, 60.0), 1)

# Simulate PM2.5, PM10, CO2, NO2
def simulate_pm2_5():
    return round(random.uniform(MIN_PM2_5, MAX_PM2_5), 1)

def simulate_pm10():
    return round(random.uniform(MIN_PM10, MAX_PM10), 1)

def simulate_co2():
    return round(random.uniform(MIN_CO2, MAX_CO2), 1)

def simulate_no2():
    return round(random.uniform(MIN_NO2, MAX_NO2), 1)

# Simulate Air Quality Index based on PM2.5
def calculate_aqi(pm2_5):
    if pm2_5 <= 12:
        return "Good"
    elif pm2_5 <= 35.4:
        return "Moderate"
    elif pm2_5 <= 55.4:
        return "Unhealthy for Sensitive Groups"
    elif pm2_5 <= 150.4:
        return "Unhealthy"
    elif pm2_5 <= 250.4:
        return "Very Unhealthy"
    else:
        return "Hazardous"

# MQTT Client Setup
client = mqtt.Client()
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)  # Connect to the MQTT broker
    print(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    exit(1)

# Main Loop
while True:
    for city in CITIES:
        # Generate sensor data for each city
        temperature = simulate_temperature()
        humidity = simulate_humidity()
        pm2_5 = simulate_pm2_5()
        pm10 = simulate_pm10()
        co2 = simulate_co2()
        no2 = simulate_no2()
        aqi = calculate_aqi(pm2_5)

        # Create a JSON message
        message = {
            "sensorId": city["name"].replace(" ", "_") + "_sensor",
            "city": city["name"],
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "temperature": temperature,
            "humidity": humidity,
            "pm2_5": pm2_5,
            "pm10": pm10,
            "co2": co2,
            "no2": no2,
            "aqi": aqi
        }

        # Publish the message to the MQTT topic
        try:
            client.publish(MQTT_TOPIC, json.dumps(message))
            print(f"Published for {city['name']}: {json.dumps(message)}")
        except Exception as e:
            print(f"Failed to publish message for {city['name']}: {e}")

        # Wait before sending data for the next city
        time.sleep(1)

    # Wait before repeating the loop
    time.sleep(1)