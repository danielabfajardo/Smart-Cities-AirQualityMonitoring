import network
import time
import urequests
from machine import Pin, ADC, I2C
import ssd1306
import dht
import ujson
import urandom
from umqtt.simple import MQTTClient

# MQTT Server Parameters
MQTT_CLIENT_ID = "wokwi_sensor"
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "/smartcities/amsterdam/temperature"

# Initial GPS Coordinates
INITIAL_LAT = 42.411567
INITIAL_LONG = 13.397309
MOVE_AMOUNT = 0.001

# ESP32 Pin assignment
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# OLED screen setup
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# DHT22 sensor for temperature and humidity
weatherSensor = dht.DHT22(Pin(15))

# Analog sensors for PM2.5, PM10, CO2, NO2
pm25Sensor = ADC(Pin(34))
pm25Sensor.atten(ADC.ATTN_11DB)
pm10Sensor = ADC(Pin(35)) 
pm10Sensor.atten(ADC.ATTN_11DB)
co2Sensor = ADC(Pin(33))
co2Sensor.atten(ADC.ATTN_11DB)
no2Sensor = ADC(Pin(32))
no2Sensor.atten(ADC.ATTN_11DB)

# Simulated power consumption sensor
powerConsumptionSensor = ADC(Pin(39))
powerConsumptionSensor.atten(ADC.ATTN_11DB)

# Mapping ADC values
def map_adc(raw, min_adc, max_adc, min_val, max_val):
    return round((raw - min_adc) * (max_val - min_val) / (max_adc - min_adc) + min_val, 1)

# Get randomized GPS coordinates
def get_coordinates(lat, long):
    variation_lat = urandom.uniform(-MOVE_AMOUNT, MOVE_AMOUNT)
    variation_long = urandom.uniform(-MOVE_AMOUNT, MOVE_AMOUNT)
    return lat + variation_lat, long + variation_long

print("Connecting to WiFi...")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    time.sleep(0.1)
print("Connected!")

try:
    print("Connecting to MQTT server...")
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("MQTT Connected!")
except Exception as e:
    print("Failed to connect to MQTT server:", e)

# Main loop
prev_lat, prev_long = INITIAL_LAT, INITIAL_LONG
while True:
    # Update GPS coordinates
    lat, long = get_coordinates(prev_lat, prev_long)

    # Read temperature and humidity
    weatherSensor.measure()
    temperature = weatherSensor.temperature()
    humidity = weatherSensor.humidity()

    # Read air quality data
    pm2_5 = map_adc(pm25Sensor.read(), 0, 4095, 0, 500)  # PM2.5 range
    pm10 = map_adc(pm10Sensor.read(), 0, 4095, 0, 500)  # PM10 range
    co2 = map_adc(co2Sensor.read(), 0, 4095, 400, 1000)  # CO2 range (ppm)
    no2 = map_adc(no2Sensor.read(), 0, 4095, 0, 500)     # NO2 range (µg/m3)

    # Simulate power consumption (in Watts)
    power_consumption = map_adc(powerConsumptionSensor.read(), 0, 4095, 50, 300)

    # Prepare MQTT message
    message = ujson.dumps({
        "sensorId": MQTT_CLIENT_ID,
        "latitude": lat,
        "longitude": long,
        "temperature": temperature,
        "humidity": humidity,
        "pm2_5": pm2_5,
        "pm10": pm10,
        "co2": co2,
        "no2": no2,
        "power_consumption": power_consumption
    })

    # Publish to MQTT topic and log
    try:
        print("Publishing to MQTT...")
        client.publish(MQTT_TOPIC, message)
        print(f"Message published: {message}")
    except Exception as e:
        print("Failed to publish:", e)

    # Display data on OLED
    oled.fill(0)
    oled.text(f"Temp: {temperature}C", 0, 0)
    oled.text(f"Humidity: {humidity}%", 0, 10)
    oled.text(f"PM2.5: {pm2_5}ug/m3", 0, 20)
    oled.text(f"PM10: {pm10}ug/m3", 0, 30)
    oled.text(f"CO2: {co2}ppm", 0, 40)
    oled.text(f"NO2: {no2}ug/m3", 0, 50)
    oled.text(f"Power: {power_consumption}W", 0, 60)
    oled.show()

    # Update previous coordinates
    prev_lat, prev_long = lat, long
    time.sleep(5)