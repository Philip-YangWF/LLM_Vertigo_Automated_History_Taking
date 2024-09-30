from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Patient

screening_bp = Blueprint('screening_bp', __name__)

@screening_bp.route('/', methods=['GET', 'POST'])
def screening():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        dizziness_onset = request.form['dizziness_onset']
        dizziness_duration = request.form['dizziness_duration']
        dizziness_trigger = request.form['dizziness_trigger']
        dizziness_character = request.form['dizziness_character']
        hearing_loss = request.form['hearing_loss']
        tinnitus = request.form['tinnitus']
        nausea_vomiting = request.form['nausea_vomiting']
        visual_disturbance = request.form['visual_disturbance']
        neurological_symptoms = request.form['neurological_symptoms']
        headache = request.form['headache']
        chest_pain = request.form['chest_pain']
        frequency_of_episodes = request.form['frequency_of_episodes']
        daily_impact = request.form['daily_impact']
        past_medical_history = request.form['past_medical_history']
        medications = request.form['medications']

        new_patient = Patient(
            name=name, age=age, gender=gender, contact=contact, dizziness_onset=dizziness_onset,
            dizziness_duration=dizziness_duration, dizziness_trigger=dizziness_trigger, dizziness_character=dizziness_character,
            hearing_loss=hearing_loss, tinnitus=tinnitus, nausea_vomiting=nausea_vomiting,
            visual_disturbance=visual_disturbance, neurological_symptoms=neurological_symptoms, headache=headache,
            chest_pain=chest_pain, frequency_of_episodes=frequency_of_episodes, daily_impact=daily_impact,
            past_medical_history=past_medical_history, medications=medications
        )
        db.session.add(new_patient)
        db.session.commit()

        return redirect(url_for('results_bp.show_results'))

    return render_template('screening.html')
