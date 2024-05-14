from app import db, Flight, app


def create_mock_flights():
    flights = [
        {"flight_number": "AA123", "departure": "LAX", "arrival": "JFK", "date": "2024-06-01", "time": "10:00 AM",
         "price": 150.0},
        {"flight_number": "UA456", "departure": "LAX", "arrival": "ORD", "date": "2024-06-01", "time": "1:00 PM",
         "price": 200.0},
        {"flight_number": "DL789", "departure": "LAX", "arrival": "SFO", "date": "2024-06-01", "time": "3:00 PM",
         "price": 100.0},
        {"flight_number": "SW123", "departure": "JFK", "arrival": "LAX", "date": "2024-06-01", "time": "5:00 PM",
         "price": 180.0},
        {"flight_number": "AA987", "departure": "ORD", "arrival": "LAX", "date": "2024-06-01", "time": "8:00 AM",
         "price": 170.0}
    ]

    with app.app_context():
        for flight in flights:
            new_flight = Flight(**flight)
            db.session.add(new_flight)
        db.session.commit()


if __name__ == '__main__':
    create_mock_flights()
