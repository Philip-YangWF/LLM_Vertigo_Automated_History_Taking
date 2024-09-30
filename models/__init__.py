from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    dizziness_onset = db.Column(db.String(50), nullable=False)
    dizziness_duration = db.Column(db.String(50), nullable=False)
    dizziness_trigger = db.Column(db.String(50), nullable=True)
    dizziness_character = db.Column(db.String(100), nullable=False)
    hearing_loss = db.Column(db.String(50), nullable=True)
    tinnitus = db.Column(db.String(50), nullable=True)
    nausea_vomiting = db.Column(db.String(50), nullable=True)
    visual_disturbance = db.Column(db.String(50), nullable=True)
    neurological_symptoms = db.Column(db.String(50), nullable=True)
    headache = db.Column(db.String(50), nullable=True)
    chest_pain = db.Column(db.String(50), nullable=True)
    frequency_of_episodes = db.Column(db.String(50), nullable=False)
    daily_impact = db.Column(db.Text, nullable=True)
    past_medical_history = db.Column(db.Text, nullable=True)
    medications = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(200), nullable=True)
