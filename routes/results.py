from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Patient

results_bp = Blueprint('results_bp', __name__)

@results_bp.route('/results', methods=['GET', 'POST'])
def show_results():
    search_query = request.args.get('search', '')  # Get the search query from the request
    filter_age_min = request.args.get('age_min', type=int)
    filter_age_max = request.args.get('age_max', type=int)
    page = request.args.get('page', 1, type=int)  # Get the page number from the URL
    per_page = 10  # Set how many results to display per page

    # Start with a base query
    patients_query = Patient.query

    # Apply filtering based on the search query
    if search_query:
        patients_query = patients_query.filter(
            Patient.name.ilike(f"%{search_query}%") |
            Patient.contact.ilike(f"%{search_query}%") |
            Patient.gender.ilike(f"%{search_query}%")
        )

    # Apply age filtering
    if filter_age_min is not None:
        patients_query = patients_query.filter(Patient.age >= filter_age_min)

    if filter_age_max is not None:
        patients_query = patients_query.filter(Patient.age <= filter_age_max)

    # Paginate results
    patients = patients_query.paginate(page=page, per_page=per_page, error_out=False)

    total_count = patients_query.count()  # Total number of patients

    return render_template('results.html', patients=patients.items,
                           total_count=total_count, current_page=page,
                           total_pages=patients.pages)


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
