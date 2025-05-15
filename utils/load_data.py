import pandas as pd
from models.models import db, Student, LifestyleFactor
import traceback

def load_data(file_path):
    try:
        print(f"Loading CSV from {file_path}")
        data = pd.read_csv(file_path)
        print(f"CSV loaded, total rows: {len(data)}")
        data = data.sample(n=7000, random_state=42)  # Subset to 7,000
        print(f"Sampled 7,000 rows")
        for i, (_, row) in enumerate(data.iterrows()):
            student = Student(
                id=row['id'],
                gender=row['Gender'],
                age=int(row['Age']) if pd.notna(row['Age']) else 0,
                city=row['City'],
                profession=row['Profession'],
                degree=row['Degree'],
                cgpa=row['CGPA'] if pd.notna(row['CGPA']) else 0.0,
                study_satisfaction=row['Study Satisfaction'] if pd.notna(row['Study Satisfaction']) else 0.0,
                depression=row['Depression'] == 1,
                suicidal_thoughts=row['Have you ever had suicidal thoughts ?'] == 'Yes',
                family_history=row['Family History of Mental Illness'] == 'Yes'
            )
            db.session.add(student)
            db.session.flush()
            lifestyle = LifestyleFactor(
                student_id=student.id,
                academic_pressure=row['Academic Pressure'] if pd.notna(row['Academic Pressure']) else 0.0,
                work_pressure=row['Work Pressure'] if pd.notna(row['Work Pressure']) else 0.0,
                job_satisfaction=row['Job Satisfaction'] if pd.notna(row['Job Satisfaction']) else 0.0,
                sleep_duration=row['Sleep Duration'],
                dietary_habits=row['Dietary Habits'],
                work_study_hours=row['Work/Study Hours'] if pd.notna(row['Work/Study Hours']) else 0.0,
                financial_stress=row['Financial Stress'] if pd.notna(row['Financial Stress']) else 0.0
            )
            db.session.add(lifestyle)
            if (i + 1) % 1000 == 0:
                print(f"Processed {i + 1} records")
        db.session.commit()
        print("Data loaded successfully")
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        traceback.print_exc()
        db.session.rollback()

if __name__ == '__main__':
    from app import app
    with app.app_context():
        db.create_all()
        load_data('data/student_depression_dataset.csv')