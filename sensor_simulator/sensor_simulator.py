import paho.mqtt.client as mqtt
import random
import time
import json

# MQTT Server Parameters
MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883

# Predefined Cities with more realistic metrics
CITIES = [
    {"name": "Songdo", "avg_pm2_5": 15, "avg_pm10": 70, "avg_co2": 450, "avg_no2": 10, "avg_temp": -10, "avg_humidity": 50},  # Winter in Korea
    {"name": "Amsterdam", "avg_pm2_5": 25, "avg_pm10": 25, "avg_co2": 400, "avg_no2": 8, "avg_temp": 5, "avg_humidity": 70},  # Cold, damp winter
    {"name": "San Francisco", "avg_pm2_5": 2, "avg_pm10": 40, "avg_co2": 420, "avg_no2": 9, "avg_temp": 12, "avg_humidity": 70},  # Cool and humid
    {"name": "Singapore", "avg_pm2_5": 5, "avg_pm10": 5, "avg_co2": 500, "avg_no2": 15, "avg_temp": 28, "avg_humidity": 75},  # Tropical climate
    {"name": "Copenhagen", "avg_pm2_5": 1, "avg_pm10": 55, "avg_co2": 390, "avg_no2": 7, "avg_temp": 2, "avg_humidity": 60},  # Cold winter
]

# Number of sensors per city
SENSORS_PER_CITY = 5

# Simulate metrics with some variability
def simulate_temperature(city):
    return round(random.gauss(city["avg_temp"], 5), 1) 

def simulate_humidity(city):
    humidity = random.gauss(city["avg_humidity"], 5)  
    return min(max(round(humidity, 1), 0), 100) 

def simulate_pollutant(avg, variation, probability_of_spike):
    if random.random() < probability_of_spike:
        value = avg + random.uniform(3 * variation, 5 * variation)
    else:
        value = random.gauss(avg, variation)
    return max(round(value, 1), 0)  # Ensure no negative values

def simulate_pm2_5(city):
    return simulate_pollutant(city["avg_pm2_5"], 5, 0.3)

def simulate_pm10(city):
    return simulate_pollutant(city["avg_pm10"], 7, 0.5)

def simulate_co2(city):
    return simulate_pollutant(city["avg_co2"], 50, 0.5)

def simulate_no2(city):
    return simulate_pollutant(city["avg_no2"], 3, 0.6)

def simulate_power_consumption():
    return max(round(random.uniform(0.5, 1.5), 2), 0)

# MQTT Client Setup
client = mqtt.Client()
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    exit(1)

# Initialize sensors
sensor_names = {}
for city in CITIES:
    sensor_names[city["name"]] = []
    for sensor_num in range(1, SENSORS_PER_CITY + 1):
        sensor_names[city["name"]].append({
            "sensor_id": f"{city['name']}_sensor_{sensor_num}"
        })

# Main Loop
while True:
    for city in CITIES:
        for sensor in sensor_names[city["name"]]:
            # Generate sensor data
            temperature = simulate_temperature(city)
            humidity = simulate_humidity(city)
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
                topic = f"/smartcities/{city['name'].lower()}/{sensor_type}"
                message = {
                    "sensor_id": sensor["sensor_id"],
                    "city": city["name"],
                    "sensor_type": sensor_type,
                    "value": value,
                    "time": int(time.time() * 1000)
                }

                # Publish to MQTT
                client.publish(topic, json.dumps(message))
                print(f"Published to {topic}: {json.dumps(message)}")
                time.sleep(0.1)  # Short delay between messages

    # Wait before repeating the loop
    time.sleep(1)