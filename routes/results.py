from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Patient
import openai

results_bp = Blueprint('results_bp', __name__)

@results_bp.route('/results', methods=['GET', 'POST'])
def show_results():
    search_query = request.args.get('search', '')
    filter_age_min = request.args.get('age_min', type=int)
    filter_age_max = request.args.get('age_max', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 10

    patients_query = Patient.query

    if search_query:
        patients_query = patients_query.filter(
            Patient.name.ilike(f"%{search_query}%") |
            Patient.contact.ilike(f"%{search_query}%") |
            Patient.gender.ilike(f"%{search_query}%")
        )

    if filter_age_min is not None:
        patients_query = patients_query.filter(Patient.age >= filter_age_min)

    if filter_age_max is not None:
        patients_query = patients_query.filter(Patient.age <= filter_age_max)

    patients = patients_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('results.html', patients=patients.items, total_count=patients.total, current_page=page, total_pages=patients.pages)



@results_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':
        # Update patient details from the form
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
        patient.tags = request.form.get('tags', '')  # Store tags

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

@results_bp.route('/mass_action', methods=['POST'])
def mass_action():
    action = request.form.get('action')
    selected_ids = request.form.getlist('selected_patients')  # Get selected patient IDs

    if action == 'delete':
        for patient_id in selected_ids:
            patient = Patient.query.get(patient_id)
            if patient:
                db.session.delete(patient)
        db.session.commit()
    elif action == 'tag':
        tags = request.form.get('tags')  # Get tags from the modal
        for patient_id in selected_ids:
            patient = Patient.query.get(patient_id)
            if patient:
                # Assuming tags are stored as a string, update your model accordingly
                if patient.tags:
                    patient.tags += f", {tags}"  # Append new tags
                else:
                    patient.tags = tags  # Set tags
        db.session.commit()

    return redirect(url_for('results_bp.show_results'))


@results_bp.route('/summarize_patient/<int:id>', methods=['POST'])
def summarize_patient(id):
    try:
        patient = Patient.query.get_or_404(id)

        # Get additional info from the request
        additional_info = request.json.get('additional_info', '')

        # Prepare patient data for GPT
        patient_data = {
            'name': patient.name,
            'age': patient.age,
            'gender': patient.gender,
            'dizziness_onset': patient.dizziness_onset,
            'dizziness_duration': patient.dizziness_duration,
            'dizziness_trigger': patient.dizziness_trigger,
            'dizziness_character': patient.dizziness_character,
            'hearing_loss': patient.hearing_loss,
            'tinnitus': patient.tinnitus,
            'nausea_vomiting': patient.nausea_vomiting,
            'visual_disturbance': patient.visual_disturbance,
            'neurological_symptoms': patient.neurological_symptoms,
            'headache': patient.headache,
            'chest_pain': patient.chest_pain,
            'frequency_of_episodes': patient.frequency_of_episodes,
            'daily_impact': patient.daily_impact,
            'past_medical_history': patient.past_medical_history,
            'medications': patient.medications
        }

        # Create a prompt based on patient data
        prompt = f"""
        Summarize the following patient's medical information:
        Name: {patient_data['name']}, Age: {patient_data['age']}, Gender: {patient_data['gender']}
        Dizziness onset: {patient_data['dizziness_onset']}
        Dizziness duration: {patient_data['dizziness_duration']}
        Dizziness trigger: {patient_data['dizziness_trigger']}
        Dizziness character: {patient_data['dizziness_character']}
        Hearing loss: {patient_data['hearing_loss']}
        Tinnitus: {patient_data['tinnitus']}
        Nausea/vomiting: {patient_data['nausea_vomiting']}
        Visual disturbance: {patient_data['visual_disturbance']}
        Neurological symptoms: {patient_data['neurological_symptoms']}
        Headache: {patient_data['headache']}
        Chest pain: {patient_data['chest_pain']}
        Frequency of episodes: {patient_data['frequency_of_episodes']}
        Impact on daily activities: {patient_data['daily_impact']}
        Past medical history: {patient_data['past_medical_history']}
        Medications: {patient_data['medications']}

        Additional information provided by the doctor:
        {additional_info}
        """

        # Use the ChatCompletion endpoint for generating a summary
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        summary = response['choices'][0]['message']['content'].strip()

        return jsonify({'summary': summary})

    except Exception as e:
        logging.error(f"Error generating AI summary: {e}")
        return jsonify({'error': 'Failed to generate summary'}), 500