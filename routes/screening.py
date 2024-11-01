from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Patient
import openai  # Assuming you are using OpenAI API or similar service

# Set up your OpenAI API key
openai.api_key = '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'

screening_bp = Blueprint('screening_bp', __name__)


@screening_bp.route('/', methods=['GET', 'POST'])
def screening():
    if request.method == 'POST':
        # Collect form data
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

        # Create a new patient record
        new_patient = Patient(
            name=name, age=age, gender=gender, contact=contact, dizziness_onset=dizziness_onset,
            dizziness_duration=dizziness_duration, dizziness_trigger=dizziness_trigger,
            dizziness_character=dizziness_character,
            hearing_loss=hearing_loss, tinnitus=tinnitus, nausea_vomiting=nausea_vomiting,
            visual_disturbance=visual_disturbance, neurological_symptoms=neurological_symptoms, headache=headache,
            chest_pain=chest_pain, frequency_of_episodes=frequency_of_episodes, daily_impact=daily_impact,
            past_medical_history=past_medical_history, medications=medications
        )
        db.session.add(new_patient)
        db.session.commit()

        # Generate a summary of the subjective information using LLM
        summary = generate_summary({
            'name': name,
            'age': age,
            'gender': gender,
            'dizziness_onset': dizziness_onset,
            'dizziness_duration': dizziness_duration,
            'dizziness_trigger': dizziness_trigger,
            'dizziness_character': dizziness_character,
            'hearing_loss': hearing_loss,
            'tinnitus': tinnitus,
            'nausea_vomiting': nausea_vomiting,
            'visual_disturbance': visual_disturbance,
            'neurological_symptoms': neurological_symptoms,
            'headache': headache,
            'chest_pain': chest_pain,
            'frequency_of_episodes': frequency_of_episodes,
            'daily_impact': daily_impact,
            'past_medical_history': past_medical_history,
            'medications': medications
        })

        # Redirect to a results page that shows the summary
        return render_template('results.html', summary=summary)

    return render_template('screening.html')


def generate_summary(patient_data):
    # Create the prompt with patient's subjective information
    prompt = f"""
    Summarize the following patient's subjective information:

    Name: {patient_data['name']}
    Age: {patient_data['age']}
    Gender: {patient_data['gender']}

    Vertigo Symptoms:
    Dizziness onset: {patient_data['dizziness_onset']}
    Dizziness duration: {patient_data['dizziness_duration']}
    Dizziness trigger: {patient_data['dizziness_trigger']}
    Dizziness character: {patient_data['dizziness_character']}

    Additional Symptoms:
    Hearing loss: {patient_data['hearing_loss']}
    Tinnitus: {patient_data['tinnitus']}
    Nausea/Vomiting: {patient_data['nausea_vomiting']}
    Visual disturbances: {patient_data['visual_disturbance']}
    Neurological symptoms: {patient_data['neurological_symptoms']}
    Headache: {patient_data['headache']}
    Chest pain: {patient_data['chest_pain']}

    Frequency of episodes: {patient_data['frequency_of_episodes']}
    Impact on daily activities: {patient_data['daily_impact']}

    Medical History:
    Past medical history: {patient_data['past_medical_history']}
    Medications: {patient_data['medications']}
    """

    # Send the prompt to the LLM (OpenAI GPT in this case)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    # Extract the generated summary
    summary = response.choices[0].text.strip()
    return summary
