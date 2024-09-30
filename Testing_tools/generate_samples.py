from app import app, db
from models import Patient
from faker import Faker
import random

# Initialize Faker
fake = Faker()

def generate_sample_patients(num_samples=30):
    # Sample dizziness characteristics
    dizziness_onset_options = ['Sudden', 'Gradual']
    dizziness_duration_options = ['Seconds', 'Minutes', 'Hours']
    dizziness_trigger_options = ['Movement', 'Position change', 'No trigger']
    dizziness_character_options = ['Spinning', 'Lightheaded', 'Floating', 'Unbalanced']
    frequency_of_episodes_options = ['Daily', 'Weekly', 'Monthly', 'Rarely']

    patients = []
    for _ in range(num_samples):
        patient = Patient(
            name=fake.name(),
            age=random.randint(18, 80),  # Age between 18 and 80
            gender=random.choice(['Male', 'Female', 'Other']),
            contact=fake.phone_number(),
            dizziness_onset=random.choice(dizziness_onset_options),
            dizziness_duration=random.choice(dizziness_duration_options),
            dizziness_trigger=random.choice(dizziness_trigger_options),
            dizziness_character=random.choice(dizziness_character_options),
            hearing_loss=random.choice(['Yes', 'No']),
            tinnitus=random.choice(['Yes', 'No']),
            nausea_vomiting=random.choice(['Yes', 'No']),
            visual_disturbance=random.choice(['Yes', 'No']),
            neurological_symptoms=random.choice(['Yes', 'No']),
            headache=random.choice(['Yes', 'No']),
            chest_pain=random.choice(['Yes', 'No']),
            frequency_of_episodes=random.choice(frequency_of_episodes_options),
            daily_impact=fake.text(max_nb_chars=100),
            past_medical_history=fake.text(max_nb_chars=100),
            medications=fake.text(max_nb_chars=100),
            tags=', '.join(fake.words(nb=3))  # Generate some random tags
        )
        patients.append(patient)

    return patients

def add_samples_to_db():
    with app.app_context():
        db.create_all()  # Ensure tables are created
        samples = generate_sample_patients()
        db.session.bulk_save_objects(samples)
        db.session.commit()

if __name__ == '__main__':
    add_samples_to_db()
    print("Generated and added 30 random patient samples to the database.")