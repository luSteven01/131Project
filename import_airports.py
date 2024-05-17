import sqlite3
from app import db, Airport, app


def import_airports():
    # Connect to the SQLite database
    conn = sqlite3.connect('airports.db')
    cursor = conn.cursor()

    # Select airport data from the SQLite database
    cursor.execute('SELECT city, airportname, code, country FROM airports')
    airports = cursor.fetchall()
    conn.close()

    # Insert data into the Flask application's database using SQLAlchemy
    with app.appcontext():
        for city, airportname, code, country in airports:
            # Check if the airport already exists
            existing_airport = Airport.query.filter_by(code=code).first()
            if existing_airport:
                # Skip duplicates
                continue
            # Insert new record
            airport = Airport(city=city, airport_name=airport_name, code=code, country=country)
            db.session.add(airport)
        db.session.commit()


if __name__ == '__main':
    import_airports()