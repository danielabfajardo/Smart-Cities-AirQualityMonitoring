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
    return max(round(random.uniform(30.0, 70.0), 1), 0)

def simulate_pollutant(avg, variation, probability_of_spike):
    if random.random() < probability_of_spike:
        value = avg + random.uniform(3 * variation, 5 * variation)
    else:
        value = random.gauss(avg, variation)
    return max(round(value, 1), 0)  # Ensure no negative values

def simulate_pm2_5(city):
    return simulate_pollutant(city["avg_pm2_5"], 5, 0.9)

def simulate_pm10(city):
    return simulate_pollutant(city["avg_pm10"], 7, 0.8)

def simulate_co2(city):
    return simulate_pollutant(city["avg_co2"], 50, 0.5)

def simulate_no2(city):
    return simulate_pollutant(city["avg_no2"], 3, 0.6)

def simulate_power_consumption():
    return max(round(random.uniform(0.5, 1.5), 2), 0)

# Generate a fixed offset for latitude and longitude
def generate_fixed_offsets():
    return round(random.uniform(-0.01, 0.01), 5)  # Small offset to vary sensor locations

# MQTT Client Setup
client = mqtt.Client()
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    exit(1)

# Initialize sensors with fixed positions
sensor_positions = {}
for city in CITIES:
    sensor_positions[city["name"]] = []
    for sensor_num in range(1, SENSORS_PER_CITY + 1):
        lat_offset = generate_fixed_offsets()
        lon_offset = generate_fixed_offsets()
        sensor_positions[city["name"]].append({
            "sensor_id": f"{city['name']}_sensor_{sensor_num}",
            "latitude": city["latitude"] + lat_offset,
            "longitude": city["longitude"] + lon_offset
        })

# Main Loop
while True:
    for city in CITIES:
        for sensor in sensor_positions[city["name"]]:
            # Generate sensor data
            temperature = simulate_temperature()
            humidity = simulate_humidity()
            pm2_5 = simulate_pm2_5(city)
            pm10 = simulate_pm10(city)
            co2 = simulate_co2(city)
            no2 = simulate_no2(city)
            power_consumption = simulate_power_consumption()

             # Combine latitude and longitude into a location string
            location = f"{sensor['latitude']},{sensor['longitude']}"

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
                    "sensor_id": sensor["sensor_id"],
                    "city": city["name"],
                    "sensor_type": sensor_type,
                    # "latitude": sensor["latitude"],
                    # "longitude": sensor["longitude"],
                    "location": location,  
                    "value": value,
                    "time": int(time.time() * 1000)
                }

                # Publish to MQTT
                client.publish(topic, json.dumps(message))
                print(f"Published to {topic}: {json.dumps(message)}")
                time.sleep(0.1)  # Short delay between messages

    # Wait before repeating the loop
    time.sleep(1)