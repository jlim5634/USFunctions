from flask import Flask, request, redirect, url_for, render_template
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    today = datetime.today().date()
    Event.query.filter(Event.date < today).delete()
    db.session.commit()
    events = Event.query.filter(Event.date >= today).order_by(Event.date).all()
    return render_template('index.html', events=events)

@app.route('/add_event', methods=['POST'])
def add_event():
    name = request.form['event_name']
    date = datetime.strptime(request.form['event_date'], '%Y-%m-%d').date()
    time = datetime.strptime(request.form['event_time'], '%H:%M').time()
    location = request.form['event_address']
    description = request.form['event_description']
    new_event = Event(name=name, date=date, time=time, location=location, description=description)
    db.session.add(new_event)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
    
