import paho.mqtt.client as mqtt
import random
import time
import json

# MQTT Server Parameters
MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883

# Predefined Cities with GPS Coordinates and average air quality profiles
CITIES = [
    {"name": "Songdo", "latitude": 37.3879, "longitude": 126.6503, "avg_pm2_5": 15, "avg_pm10": 20, "avg_co2": 450, "avg_no2": 10},
    {"name": "Amsterdam", "latitude": 52.3676, "longitude": 4.9041, "avg_pm2_5": 10, "avg_pm10": 15, "avg_co2": 400, "avg_no2": 8},
    {"name": "San Francisco", "latitude": 37.7749, "longitude": -122.4194, "avg_pm2_5": 12, "avg_pm10": 18, "avg_co2": 420, "avg_no2": 9},
    {"name": "Singapore", "latitude": 1.3521, "longitude": 103.8198, "avg_pm2_5": 20, "avg_pm10": 25, "avg_co2": 500, "avg_no2": 15},
    {"name": "Copenhagen", "latitude": 55.6761, "longitude": 12.5683, "avg_pm2_5": 8, "avg_pm10": 12, "avg_co2": 390, "avg_no2": 7},
]

# Number of sensors per city
SENSORS_PER_CITY = 3

# Simulate temperature and humidity
def simulate_temperature():
    return round(random.uniform(18.0, 35.0), 1)

def simulate_humidity():
    return round(random.uniform(30.0, 70.0), 1)

# Simulate pollutants with realistic ranges and probabilities
def simulate_pollutant(avg, variation, probability_of_spike):
    if random.random() < probability_of_spike:
        return round(avg + random.uniform(3 * variation, 5 * variation), 1)
    else:
        return round(random.gauss(avg, variation), 1)

def simulate_pm2_5(city):
    return simulate_pollutant(city["avg_pm2_5"], 5, 0.9)

def simulate_pm10(city):
    return simulate_pollutant(city["avg_pm10"], 7, 0.8)

def simulate_co2(city):
    return simulate_pollutant(city["avg_co2"], 50, 0.5)

def simulate_no2(city):
    return simulate_pollutant(city["avg_no2"], 3, 0.6)

def simulate_power_consumption():
    return round(random.uniform(0.5, 1.5), 2)

# Generate a random offset for latitude and longitude
def random_offset():
    return round(random.uniform(-0.01, 0.01), 5)  # Small offset to vary sensor locations

# MQTT Client Setup
client = mqtt.Client()
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    exit(1)

# Main Loop
sensor_count_per_city = {city["name"]: random.randint(1, 3) for city in CITIES}  # Random 1–3 sensors per city

while True:
    for city in CITIES:
        for sensor_num in range(1, sensor_count_per_city[city["name"]] + 1):
            # Generate unique latitude and longitude for the sensor
            sensor_latitude = city["latitude"] + random_offset()
            sensor_longitude = city["longitude"] + random_offset()

            # Generate sensor data
            temperature = simulate_temperature()
            humidity = simulate_humidity()
            pm2_5 = simulate_pm2_5(city)
            pm10 = simulate_pm10(city)
            co2 = simulate_co2(city)
            no2 = simulate_no2(city)
            power_consumption = simulate_power_consumption()

            # Publish each sensor type to a separate topic
            topics_data = {
                "temperature": temperature,
                "humidity": humidity,
                "pm2_5": pm2_5,
                "pm10": pm10,
                "co2": co2,
                "no2": no2,
                "power_consumption": power_consumption
            }

            for sensor_type, value in topics_data.items():
                # Create the topic and message
                topic = f"/smartcities/{city['name'].lower()}/{sensor_type}"
                message = {
                    "sensor_id": f"{city['name']}_sensor_{sensor_num}",
                    "city": city["name"],
                    "sensor_type": sensor_type,
                    "latitude": sensor_latitude,
                    "longitude": sensor_longitude,
                    "value": value,
                    "time": int(time.time() * 1000)
                }

                # Publish to MQTT
                client.publish(topic, json.dumps(message))
                print(f"Published to {topic}: {json.dumps(message)}")
                time.sleep(0.1)  # Short delay between messages

    # Wait before repeating the loop
    time.sleep(1)