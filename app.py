from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and set up SQLite database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models for storing registration and appointments
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.String(10), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    patient = db.relationship('Patient', backref='appointments')

# Routes for each webpage
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        doctor_name = request.form['doctor_name']
        date = request.form['date']
        time = request.form['time']
        patient_id = request.form['patient_id']
        
        new_appointment = Appointment(patient_id=patient_id, doctor_name=doctor_name, date=date, time=time)
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('appointment'))
    
    patients = Patient.query.all()
    return render_template('appointment.html', patients=patients)

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        gender = request.form['gender']
        dob = request.form['dob']
        
        new_patient = Patient(name=name, email=email, phone=phone, address=address, gender=gender, dob=dob)
        db.session.add(new_patient)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('register.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
