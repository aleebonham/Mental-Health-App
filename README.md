# Student Mental Health Dashboard
**Name**: Alee Bonham
**Date**: May 15, 2025

## Design
Uses MVC pattern: Flask routes, SQLAlchemy models, and Jinja templates.
Has two tables (Students and LifestyleFactors) with a one-to-many relationship. 
UI was designed with CSS to achieve a professional look.

## Development
Developed iteratively with Git. During development UI was enhanced, test assertions were fixed, and database initialization issues were slowly solved.

## Implementation
Built app with Flask, SQLAlchemy (SQLite), and pandas. Loaded 7,000 records from the Student Depression Dataset found on Kaggle.

## Installation (currently contains app.db so you can skip step 3. onnly use step 3 if app.db is absent)
1. Clone: `git clone <repo-url>`
2. Install: `pip install -r requirements.txt`
3. Load data: `python -m utils.load_data data/student_depression_dataset.csv`
4. Run: 'flask run --host=0.0.0.0 --port=5000'

## Usage
You can browse the student data in the Student tab with the option to filer by city
View in-depth details about each student using the view button
Analyze trends surrounding Depression by city and a link between academic pressure and depression in Analysis tab

## Render URL 
https://mental-health-app-d6sf.onrender.com

## Codio URL
https://bridgejames-exhibitbronze-5000.codio-box.uk