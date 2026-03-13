 Project Survival Analysis System

This project is part of our B.Tech CSE group project. The main idea of this system is to predict the risk of student project failure before it actually happens.

In many cases teachers only realize that a project is failing near the deadline. By that time it is already too late to fix things. Our system tries to detect early warning signals such as inactivity, missed milestones, and low engagement.

Using these signals, the system estimates the probability that a project might fail in the coming weeks.

 What problem are we solving?

Most academic project tracking systems only store data like attendance or submission status. They do not analyze patterns in the data.

For example:

A team stops working for several weeks

Milestones are repeatedly missed

Lab attendance drops

These signals usually appear before a project fails, but they are rarely analyzed.

Our system tries to analyze these patterns and provide risk estimation using machine learning.

🔬 Methodology

We use a Cox Proportional Hazards model, which is commonly used in survival analysis.

Instead of predicting only yes or no failure, survival models estimate how risk changes over time.

The model uses weekly project data such as:

days worked

inactivity streak

milestones missed

lab attendance

The model then estimates how these factors influence the probability of project failure.

Example idea:

Risk = f(days_worked, inactivity_streak, milestones_missed, lab_attendance)

If the hazard ratio of a variable is greater than 1, it means that the variable increases the risk of failure.

⚙️ Features

Our system includes a few basic features:

Student View
Students can view only their own project information and progress.

Teacher View
Teachers can access a dashboard that shows all project data.

Weekly Activity Tracking
Tracks engagement indicators such as working days, milestone completion, and inactivity.

Risk Prediction
The survival model estimates failure risk using the collected data.

Two Interfaces
We implemented two interfaces:

Streamlit dashboard

HTML / Flask interface

🗂 Dataset Structure

The system stores project activity data in an Excel file.

Example structure:

project_id
student_id
week_number
days_worked_this_week
days_since_last_work
lab_attended_this_week
milestones_completed_till_week
milestones_missed_till_week
inactivity_streak
event
time_to_event

Each row represents the weekly progress of a project.

🧠 Technologies Used

Programming Language
Python

Libraries
Pandas
NumPy
Lifelines (for survival analysis)
Streamlit
Flask

Frontend
HTML
CSS
JavaScript

📂 Project Structure
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
🚀 How to Run the Project

Install the required libraries:

pip install -r requirements.txt

Run the backend server:

cd backend
python app.py

Run the Streamlit interface:

cd frontend-streamlit
streamlit run frontend.py

Open the HTML interface:

cd frontend-html
open index.html
📈 Expected Outcome

The system identifies key behavioral signals that indicate project failure risk.

For example, during testing we observed that long inactivity streaks strongly increase failure risk.

This type of information can help teachers intervene earlier and guide students before the project collapses.

🎓 Academic Context

This project is developed as part of our B.Tech Computer Science semester project.

It combines concepts from:

Educational Data Mining

Survival Analysis

Predictive Analytics

The goal is to explore how data-driven approaches can help improve academic project monitoring.
