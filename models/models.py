from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100))
    profession = db.Column(db.String(50))
    degree = db.Column(db.String(50))
    cgpa = db.Column(db.Float)
    study_satisfaction = db.Column(db.Float)
    depression = db.Column(db.Boolean, nullable=False)
    suicidal_thoughts = db.Column(db.Boolean, nullable=False)
    family_history = db.Column(db.Boolean, nullable=False)
    lifestyle_factors = db.relationship('LifestyleFactor', backref='student', lazy=True)

class LifestyleFactor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    academic_pressure = db.Column(db.Float)
    work_pressure = db.Column(db.Float)
    job_satisfaction = db.Column(db.Float)
    sleep_duration = db.Column(db.String(50))
    dietary_habits = db.Column(db.String(50))
    work_study_hours = db.Column(db.Float)
    financial_stress = db.Column(db.Float)