import sqlite3
from app import db, Airport, app

def import_airports():
    conn = sqlite3.connect('airports.db')
    cursor = conn.cursor()
    cursor.execute('SELECT city, airport_name, code, country FROM airports')
    airports = cursor.fetchall()
    conn.close()

    with app.app_context():
        for city, airport_name, code, country in airports:
            airport = Airport(city=city, airport_name=airport_name, code=code, country=country)
            db.session.add(airport)
        db.session.commit()

if __name__ == '__main__':
    import_airports()
