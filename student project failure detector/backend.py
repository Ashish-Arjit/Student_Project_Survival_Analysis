from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import numpy as np
from lifelines import CoxPHFitter
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
CORS(app)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
FILE_NAME = os.path.join(DATA_DIR, "project_survival_data.xlsx")

COLUMNS = ["project_id", "student_id_or_team_id", "week_number", "days_worked_this_week",
           "days_since_last_work", "lab_attended_this_week", "milestones_completed_till_week",
           "milestones_missed_till_week", "inactivity_streak", "event", "time_to_event"]

def create_new_file():
    df = pd.DataFrame(columns=COLUMNS)
    df.to_excel(FILE_NAME, index=False)
    return True

def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_excel(FILE_NAME)
    return pd.DataFrame(columns=COLUMNS)

def validate_entry(df, data_dict):
    project_id = data_dict["project_id"]
    week_number = data_dict["week_number"]
    time_to_event = data_dict["time_to_event"]
    event = data_dict["event"]
    
    project_data = df[df["project_id"] == project_id]
    if not project_data.empty:
        max_week = project_data["week_number"].max()
        if week_number <= max_week:
            return False, f"Week {week_number} <= max {max_week}"
    
    if event == 1 and week_number != time_to_event:
        return False, "Event=1 only at time_to_event"
    
    if not project_data.empty:
        existing_time = project_data["time_to_event"].iloc[0]
        if time_to_event != existing_time:
            return False, "time_to_event must match"
    
    return True, "Valid"

def add_entry(data_dict):
    df = load_data()
    required = ["project_id", "week_number", "time_to_event", "event"]
    if not all(col in data_dict for col in required):
        return False, "Missing required columns"
    
    valid, msg = validate_entry(df, data_dict)
    if not valid:
        return False, msg
    
    for col in ["days_worked_this_week", "days_since_last_work", "lab_attended_this_week",
                "milestones_completed_till_week", "milestones_missed_till_week", "inactivity_streak"]:
        data_dict.setdefault(col, 0)
    
    new_row = pd.DataFrame([data_dict])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(FILE_NAME, index=False)
    return True, "Entry added"

def train_survival_model():
    df = load_data()
    if len(df) < 10:
        return None, "Need 10+ rows", False
    
    model_data = []
    for project_id, group in df.groupby('project_id'):
        max_week = group['week_number'].max()
        time_to_event = group['time_to_event'].iloc[0]
        event = 1 if max_week >= time_to_event else 0
        
        for week in range(1, max_week + 1):
            week_data = group[group['week_number'] == week]
            if not week_data.empty:
                row = week_data.iloc[0].copy()
                row['event'] = event
                row['time_to_event'] = time_to_event
                model_data.append(row)
    
    df_model = pd.DataFrame(model_data)
    predictors = ["days_worked_this_week", "days_since_last_work", "lab_attended_this_week",
                  "milestones_completed_till_week", "milestones_missed_till_week", "inactivity_streak"]
    df_model = df_model[predictors + ["time_to_event", "event"]].fillna(0)
    
    cph = CoxPHFitter()
    cph.fit(df_model, duration_col='time_to_event', event_col='event')
    return cph, cph.summary, True

# API ENDPOINTS
@app.route('/create_dataset', methods=['POST'])
def create_dataset():
    create_new_file()
    return jsonify({'message': 'Dataset created'})

@app.route('/add_entry', methods=['POST'])
def add_entry_api():
    data = request.json
    success, msg = add_entry(data)
    return jsonify({'success': success, 'message': msg})

@app.route('/get_preview', methods=['GET'])
def get_preview():
    df = load_data()
    preview = df.tail(5)[['project_id', 'week_number', 'days_worked_this_week', 
                          'milestones_missed_till_week', 'event']].to_dict('records')
    return jsonify(preview)

@app.route('/get_data', methods=['GET'])
def get_data():
    role = request.args.get('role', 'teacher')
    student_id = request.args.get('student_id')
    df = load_data()
    
    if role == 'student' and student_id:
        df = df[df['student_id_or_team_id'] == student_id]
    
    return jsonify(df.to_dict('records'))

@app.route('/get_projects', methods=['GET'])
def get_projects():
    student_id = request.args.get('student_id')
    df = load_data()
    
    if student_id:
        df = df[df['student_id_or_team_id'] == student_id]
    
    projects = df['project_id'].unique().tolist()
    return jsonify({'projects': projects})

@app.route('/train_model', methods=['POST'])
def train_model_api():
    _, summary, success = train_survival_model()
    if not success:
        return jsonify({'error': summary})
    
    plt.figure(figsize=(10, 6))
    cph, _, _ = train_survival_model()
    cph.plot()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return jsonify({
        'summary': summary.to_dict(),
        'plot_url': f'data:image/png;base64,{plot_url}',
        'message': 'Model trained'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
