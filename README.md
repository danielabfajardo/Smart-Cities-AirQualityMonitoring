# Smart Cities: Air Quality Monitoring System

This project is an IoT-based Real-Time Air Quality Monitoring and Alert System designed to simulate and manage air quality data for urban environments. By leveraging IoT technologies, real-time data processing, and visual dashboards, the system empowers users to make informed decisions to improve urban health and sustainability.

## Introduction

The Smart Cities Air Quality Monitoring System monitors and analyzes air quality parameters such as PM2.5, PM10, CO2, NO2, temperature, and humidity. Simulated sensors generate realistic environmental data, which is processed using Node-RED, stored in InfluxDB, and visualized in Grafana. The system includes real-time alerting via Telegram bots and features dynamic threshold management for key metrics.

Additionally, this project includes a simulation in Wokwi, an online platform for Arduino and IoT projects, to demonstrate how the system can integrate real-world sensors with minimal changes.

## How to Run the Project

### Clone the repository:
```bash
git clone https://github.com/danielabfajardo/Smart-Cities-AirQualityMonitoring.git
cd Smart-Cities-AirQualityMonitoring
```

### Check .env File:
•	The project includes a pre-filled .env file for educational purposes. Ensure it exists in the root directory.

### Start the Docker Containers:
Ensure Docker and Docker Compose are installed.
	•	Run the following command to start all services:
  ```bash
  docker-compose up -d --build 
  ```

1.	Access Grafana:
•	Open http://localhost:3000 in your browser.
•	Login with the credentials:
  •	Username: admin
  •	Password: admin123

2.	Access InfluxDB:
•	Open http://localhost:8086 in your browser.
•	Login with the credentials:
  •	Username: admin
  •	Password: admin123
 
### Stopping the containers
```bash
docker-compose down
```

## Wokwi Simulation

Wokwi Link: [Wokwi Simulation](https://wokwi.com/projects/418538359529169921)

This project includes a Wokwi simulation as a proof of concept for integrating real-world sensors. While the main project uses a Python-based data simulation, the Wokwi setup demonstrates how hardware like Arduino can be seamlessly connected. The Wokwi simulation is not directly integrated into the project but showcases the readiness of the system for real sensor deployment.

## Educational Purpose Disclaimer

This project is intended for educational purposes only. The included .env file contains pre-configured credentials for demonstration. Do not use these credentials in a production environment. Update usernames, passwords, and tokens to secure values for any real deployment.

## Contact

For questions or contributions, feel free to open an issue or reach out!
GitHub: @danielabfajardo
