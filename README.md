Project Survival Analysis System

This project is a B.Tech CSE group project designed to predict the risk of student project failure using survival analysis techniques. The system analyzes weekly activity data and estimates the probability that a project may fail before completion.

The main objective is to help mentors identify at-risk projects early so that timely intervention can be made.

Problem Statement

In many academic environments, student project progress is monitored only through milestone submissions or final evaluations. This makes it difficult for instructors to identify struggling teams early.

This system attempts to solve that problem by analyzing behavioral indicators such as:

Number of days worked per week

Milestones completed or missed

Lab attendance

Inactivity streak

Using these signals, the system estimates failure risk over time.

Methodology

The project uses the Cox Proportional Hazards model, a survival analysis technique that predicts the time until a specific event occurs.

In this project, the event represents project failure or dropout.

The model analyzes weekly project activity data and estimates how different factors influence the probability of failure.

Example model relationship:

Risk = f(days_worked, inactivity_streak, milestones_missed, lab_attendance)

A hazard ratio greater than 1 indicates that the variable increases the risk of project failure.

System Architecture

The project is divided into three main components:

Backend
Handles dataset processing, model training, and API communication.

Frontend (Streamlit)
Provides an interactive dashboard for visualizing project data and risk predictions.

Frontend (HTML Interface)
A lightweight web interface that allows basic interaction with the system.

The dataset is stored using an Excel file for simplicity and easy modification.

Dataset Structure

The system uses a weekly project monitoring dataset with the following fields:

project_id
student_id / team_id
week_number
days_worked_this_week
days_since_last_work
lab_attended_this_week
milestones_completed_till_week
milestones_missed_till_week
inactivity_streak
event
time_to_event

Each row represents the weekly activity record of a project.

Features

Student View
Students can view only their own project information and progress data.

Teacher View
Teachers can access a dashboard that displays all project records and risk predictions.

Weekly Tracking
Tracks engagement indicators such as working days, milestone completion, and inactivity.

Risk Estimation
Uses the Cox Proportional Hazards model to estimate the probability of project failure.

Dual Interface
The system includes both a Streamlit-based interface and a basic HTML interface.

Technology Stack

Programming Language
Python

Libraries
Pandas
NumPy
Lifelines (Survival Analysis)
Streamlit
Flask
OpenPyXL

Frontend
HTML
CSS
JavaScript

Project Structure
project-survival-analysis/
│
├── backend/
│   └── app.py
│
├── frontend-streamlit/
│   └── frontend.py
│
├── frontend-html/
│   └── index.html
│
├── dataset/
│   └── project_survival_data.xlsx
│
├── requirements.txt
└── README.md
How to Run the Project

Install dependencies

pip install -r requirements.txt

Run the backend server

cd backend
python app.py

Run the Streamlit interface

cd frontend-streamlit
streamlit run frontend.py

Open the HTML interface

cd frontend-html
open index.html
Expected Results

The system produces survival analysis outputs that indicate which behavioral factors significantly affect project failure risk.

Example interpretation:

If the hazard ratio for inactivity_streak is greater than 1, it means that increasing inactivity significantly increases the probability of project failure.

This allows mentors to identify students who may require guidance or support earlier in the semester.

Academic Context

This project was developed as part of a Design Thinking and Innovation / Data Analytics based academic project in the B.Tech Computer Science program.

The work combines concepts from:

Educational Data Mining

Survival Analysis

Predictive Analytics

Student Performance Monitoring

License

This project is developed for academic and research purposes.
