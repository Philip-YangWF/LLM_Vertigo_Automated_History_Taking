from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Patient

results_bp = Blueprint('results_bp', __name__)

@results_bp.route('/results')
def show_results():
    patients = Patient.query.all()
    return render_template('results.html', patients=patients)

@results_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.gender = request.form['gender']
        patient.contact = request.form['contact']
        patient.dizziness_onset = request.form['dizziness_onset']
        patient.dizziness_duration = request.form['dizziness_duration']
        patient.dizziness_trigger = request.form['dizziness_trigger']
        patient.dizziness_character = request.form['dizziness_character']
        patient.hearing_loss = request.form['hearing_loss']
        patient.tinnitus = request.form['tinnitus']
        patient.nausea_vomiting = request.form['nausea_vomiting']
        patient.visual_disturbance = request.form['visual_disturbance']
        patient.neurological_symptoms = request.form['neurological_symptoms']
        patient.headache = request.form['headache']
        patient.chest_pain = request.form['chest_pain']
        patient.frequency_of_episodes = request.form['frequency_of_episodes']
        patient.daily_impact = request.form['daily_impact']
        patient.past_medical_history = request.form['past_medical_history']
        patient.medications = request.form['medications']
        patient.tags = request.form.get('tags', '')  # Store as a comma-separated string
        db.session.commit()
        return redirect(url_for('results_bp.show_results'))

    return render_template('edit.html', patient=patient)

@results_bp.route('/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('results_bp.show_results'))

@results_bp.route('/view/<int:id>', methods=['GET'])
def view_patient(id):
    patient = Patient.query.get_or_404(id)
    return render_template('view.html', patient=patient)
