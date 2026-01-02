from flask import Flask, render_template, request
from prediction import predictDiabetes
import pandas as pd
import os

app = Flask(__name__, template_folder='templates')

# Counter file path
COUNTER_FILE = 'form_completions.txt'

def get_completion_count():
    """Read the completion count from file, return 0 if file doesn't exist."""
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, 'r') as f:
                count = int(f.read().strip())
                return count
        except (ValueError, IOError):
            return 0
    return 0

def increment_completion_count():
    """Increment the completion count and save to file."""
    count = get_completion_count()
    count += 1
    try:
        with open(COUNTER_FILE, 'w') as f:
            f.write(str(count))
        return count
    except IOError:
        return count

@app.route('/')
def intro():
    count = get_completion_count()
    return render_template('intro.html', completion_count=count)

@app.route('/form')
def index():
    return render_template('index.html')


@app.route('/response', methods=['POST'])
def response():
    # Create pandas DataFrame with form data
    form_data = pd.DataFrame({
        'HighBP': [int(request.form.get('high_bp'))],
        'HighChol': [int(request.form.get('high_chol'))],
        'BMI': [float(request.form.get('bmi', 0))],
        'Smoker': [int(request.form.get('smoking'))],
        'Stroke': [int(request.form.get('stroke'))],
        'HeartDiseaseorAttack': [int(request.form.get('heart_disease'))],
        'PhysActivity': [int(request.form.get('phys_activity'))],
        'Fruits': [int(request.form.get('fruits'))],
        'HvyAlcoholConsump': [int(request.form.get('heavy_drinker'))],
        'NoDocbcCost': [int(request.form.get('no_docbc_cost'))],
        'GenHlth': [int(request.form.get('gen_hlth'))],
        'MentHlth': [int(request.form.get('ment_hlth'))],
        'PhysHlth': [int(request.form.get('phys_hlth'))],
        'DiffWalk': [int(request.form.get('diff_walk'))],
        'Sex': [int(request.form.get('sex'))],
        'Age': [int(request.form.get('age'))],
        'Income': [int(request.form.get('income'))]
    })
    
    # Make prediction
    result = predictDiabetes(form_data)
    
    # Increment completion counter
    increment_completion_count()
    
    # Render response template with results
    return render_template('response.html', 
                         prediction=result['prediction'],
                         probability=result['probability'])

if __name__ == '__main__':
    app.run(debug=True)