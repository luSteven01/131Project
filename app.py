from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import random
import string
from datetime import datetime, timedelta

from flask_wtf import FlaskForm,Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets_flight_booking.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

#Forms
class LoginForm(FlaskForm, Form):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ViewForm(FlaskForm, Form):
    fn = StringField('Flight Number:',validators=[DataRequired()])
    submit = SubmitField('Search')

#db Class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64))

    posts = db.relationship('Post', backref='author',)

    def __repr__(self):
        return f'[User {self.username} / {self.email}]'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'[User {self.body} / {self.user_id}]'


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(20), nullable=False)
    departure = db.Column(db.String(100), nullable=False)
    arrival = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)


class Airport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    airport_name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(20), nullable=False)
    departure = db.Column(db.String(100), nullable=False)
    arrival = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_name = db.Column(db.String(150), nullable=False)
    user_email = db.Column(db.String(150), nullable=False)
    user_phone = db.Column(db.String(20), nullable=False)
    pet_name = db.Column(db.String(300), nullable=False)  # Adjusted length to store multiple names
    pet_type = db.Column(db.String(50), nullable=False)
    emergency_contact_name = db.Column(db.String(150), nullable=False)
    emergency_contact_phone = db.Column(db.String(20), nullable=False)
    seat_number = db.Column(db.String(5), nullable=True)
    payment_status = db.Column(db.String(20), nullable=True)
    confirmation_number = db.Column(db.String(10), nullable=False, unique=True)


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
#tells flask to execute login() when user goes to /login path of the webpage
def login():
    current_form = LoginForm()
    if current_form.validate_on_submit():
        flash(f'VALID USERNAME {current_form.username.data}')
        flash(f'VALID PASSWORD {current_form.password.data}')

        ############Add a row to database (user table)####################
        user = User(username=current_form.username.data, email = 'test@gmail.com')
        db.session.add(user)
        db.session.commit()

    return render_template("login.html", form=current_form)

@app.route('/search', methods=['GET', 'POST'])
def search_flight():
    airports = Airport.query.all()
    if request.method == 'POST':
        trip_type = request.form.get('trip_type')
        departure = request.form.get('departure')
        arrival = request.form.get('arrival')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date') if trip_type == 'round_trip' else None
        num_pets = request.form.get('num_pets')

        # Generate mock flights based on the search criteria
        mock_flights = generate_mock_flights(departure, arrival, departure_date)

        return render_template('search_results.html', flights=mock_flights, trip_type=trip_type, departure=departure, arrival=arrival, departure_date=departure_date, return_date=return_date, num_pets=num_pets)
    return render_template('search.html', airports=airports)


def generate_mock_flights(departure, arrival, date):
    flight_numbers = ['AA123', 'UA456', 'DL789', 'SW123', 'AA987']
    times = ['08:00 AM', '10:00 AM', '01:00 PM', '03:00 PM', '05:00 PM']
    prices = [150.0, 200.0, 100.0, 180.0, 170.0]
    mock_flights = []

    for i in range(5):
        flight = {
            'id': i + 1,
            'flight_number': flight_numbers[i],
            'departure': departure,
            'arrival': arrival,
            'date': date,
            'time': times[i],
            'price': random.choice(prices)
        }
        mock_flights.append(flight)

    return mock_flights


@app.route('/book_flight', methods=['POST'])
def book_selected_flight():
    selected_flight_id = request.form.get('selected_flight')
    selected_flight = Flight.query.get(selected_flight_id)

    # Store the flight details in the session
    session['selected_flight'] = {
        'flight_number': selected_flight.flight_number,
        'departure': selected_flight.departure,
        'arrival': selected_flight.arrival,
        'date': selected_flight.date,
        'time': selected_flight.time,
        'price': selected_flight.price
    }

    return redirect(url_for('user_info'))


@app.route('/user_info', methods=['GET', 'POST'])
def user_info():
    if request.method == 'POST':
        num_pets = int(request.form.get('num_pets'))
        pet_names = [request.form.get(f'pet_name_{i}') for i in range(1, num_pets + 1)]
        flight_price = session.get('selected_flight')['price']  # Assuming flight price is stored in session
        pet_fee = 100 * num_pets
        tax_rate = 0.075
        tax_amount = flight_price * tax_rate
        total_price = flight_price + pet_fee + tax_amount

        session['user_info'] = {
            'user_name': request.form.get('user_name'),
            'user_email': request.form.get('user_email'),
            'user_phone': request.form.get('user_phone'),
            'num_pets': num_pets,
            'pet_names': pet_names,
            'pet_type': request.form.get('pet_type'),
            'emergency_contact_name': request.form.get('emergency_contact_name'),
            'emergency_contact_phone': request.form.get('emergency_contact_phone'),
            'flight_price': flight_price,
            'pet_fee': pet_fee,
            'tax_amount': tax_amount,
            'total_price': total_price
        }
        return redirect(url_for('seat_selection'))
    return render_template('user_info.html')


@app.route('/seat_selection', methods=['GET', 'POST'])
def seat_selection():
    if request.method == 'POST':
        seat_number = request.form.get('seat_number')
        session['seat_selection'] = seat_number
        return redirect(url_for('payment'))

    occupied_seats = random.sample([f"{row}{seat}" for row in range(1, 21) for seat in ['A', 'B', 'C', 'D']],
                                   k=15)  # Randomly occupy 15 seats
    return render_template('seat_selection.html', occupied_seats=occupied_seats)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        session['payment_status'] = 'Paid'
        return redirect(url_for('booking_confirmation'))

    user_info = session['user_info']
    return render_template('payment.html', user_info=user_info)


@app.route('/confirm_booking', methods=['GET', 'POST'])
def confirm_booking():
    user_info = session.get('user_info')
    booking = session.get('selected_flight')

    if not booking or not user_info:
        return redirect(url_for('home'))

    # Generate a random confirmation number
    confirmation_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # Save booking details to the database
    new_booking = Booking(
        flight_number=booking['flight_number'],
        departure=booking['departure'],
        arrival=booking['arrival'],
        date=booking['date'],
        time=booking['time'],
        price=booking['price'],
        user_name=user_info['user_name'],
        user_email=user_info['user_email'],
        user_phone=user_info['user_phone'],
        pet_name=user_info['pet_name'],
        pet_type=user_info['pet_type'],
        emergency_contact_name=user_info['emergency_contact_name'],
        emergency_contact_phone=user_info['emergency_contact_phone'],
        confirmation_number=confirmation_number
    )
    db.session.add(new_booking)
    db.session.commit()

    # Store the confirmation number in the session
    session['confirmation_number'] = confirmation_number

    return redirect(url_for('booking_confirmation'))


@app.route('/booking_confirmation')
def booking_confirmation():
    booking = session.get('selected_flight')
    user_info = session.get('user_info')
    seat_selection = session.get('seat_selection')
    payment_status = session.get('payment_status')
    confirmation_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    if not booking or not user_info or not seat_selection or not payment_status:
        return redirect(url_for('home'))

    new_booking = Booking(
        flight_number=booking['flight_number'],
        departure=booking['departure'],
        arrival=booking['arrival'],
        date=booking['date'],
        time=booking['time'],
        price=booking['price'],
        user_name=user_info['user_name'],
        user_email=user_info['user_email'],
        user_phone=user_info['user_phone'],
        pet_name=', '.join(user_info['pet_names']),
        pet_type=user_info['pet_type'],
        emergency_contact_name=user_info['emergency_contact_name'],
        emergency_contact_phone=user_info['emergency_contact_phone'],
        seat_number=seat_selection,
        payment_status=payment_status,
        confirmation_number=confirmation_number
    )
    db.session.add(new_booking)
    db.session.commit()

    session['confirmation_number'] = confirmation_number

    return render_template('booking_confirmation.html', booking=booking, user_info=user_info, seat_selection=seat_selection, payment_status=payment_status, confirmation_number=confirmation_number)


@app.route('/view_flight_status', methods=['GET', 'POST'])
def view_flight_status():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        confirmation_number = request.form.get('confirmation_number')

        booking = Booking.query.filter_by(user_name=full_name, confirmation_number=confirmation_number).first()

        if booking:
            # Calculate boarding time (30 minutes before flight time)
            flight_time = datetime.strptime(booking.time, '%I:%M %p')
            boarding_time = (flight_time - timedelta(minutes=30)).strftime('%I:%M %p')

            # Generate random arrival time (flight duration between 1 and 5 hours)
            flight_duration = random.randint(1, 5)
            arrival_time = (flight_time + timedelta(hours=flight_duration)).strftime('%I:%M %p')

            # Randomly generate terminal and gate
            terminal = random.choice(['A', 'B', 'C', 'D'])
            gate = f'H{random.randint(1, 30)}'

            return render_template('flight_status.html', booking=booking, boarding_time=boarding_time,
                                   arrival_time=arrival_time, terminal=terminal, gate=gate)
        else:
            flash('No flight found with the provided information. Please check again.')
            return redirect(url_for('view_flight_status'))

    return render_template('view_flight_status.html')


@app.route('/view_booking', methods=['GET', 'POST'])
def view_booking():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        phone_number = request.form.get('phone_number')
        user_bookings = Booking.query.filter_by(user_name=full_name, user_phone=phone_number).all()
        if user_bookings:
            return render_template('view_booking.html', bookings=user_bookings)
        else:
            flash('No bookings found for the provided information. Please check again.', 'danger')
            return redirect(url_for('view_booking'))
    return render_template('view_booking.html')


@app.route('/cancel_booking', methods=['GET', 'POST'])
def cancel_booking():
    if request.method == 'POST':
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        confirmation_number = request.form.get('confirmation_number')
        booking = Booking.query.filter_by(user_name=last_name, user_phone=phone_number, confirmation_number=confirmation_number).first()
        if booking:
            db.session.delete(booking)
            db.session.commit()
            flash(
                "Booking cancelled successfully. Your refund will be processed and returned to your original payment "
                "method within 7-14 business days", 'success')
        else:
            flash('Booking not found', 'danger')
        return redirect(url_for('cancel_booking'))
    return render_template('cancel_booking.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


if __name__ == '__main__':
    app.run(debug=True)
