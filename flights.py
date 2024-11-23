import random

def generate_flights(n=10):
    flights = []
    for _ in range(n):
        flight = {
            'id': f"FL{random.randint(1000, 9999)}",
            'lat': round(random.uniform(-90, 90), 2),
            'lon': round(random.uniform(-180, 180), 2),
            'altitude': random.randint(1000, 40000),
            'speed': random.randint(200, 600)
        }
        flights.append(flight)
    return flights
