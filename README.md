# Mental-Health-App
Flask app to explore student depression trends

#Dataset
-Downloaded from Kaggle, subset to 7,000 records
-Extracted CSV using Python
-Loaded into SQLite with load_data.py 

#Installation
-Install: pip install -r requirements.txt
-Load Data: python -m utils.load_data data/student_depression_subset.csv 
-Run: flask run

#Testing
-Run: python -m unittest tests.py 

#Render URL
https://mental-health-app-d6sf.onrender.com