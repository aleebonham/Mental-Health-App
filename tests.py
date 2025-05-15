import unittest
from flask import Flask
from models.models import db, Student, LifestyleFactor
from routes.routes import bp

class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Create a new Flask app for testing
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Initialize SQLAlchemy with the test app
        db.init_app(self.app)
        self.app.register_blueprint(bp)
        
        # Create a test client
        self.client = self.app.test_client()
        
        # Set up the database
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student Mental Health Dashboard', response.data)

    def test_students(self):
        response = self.client.get('/students')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Students', response.data)

    def test_student_page(self):
        with self.app.app_context():
            student = Student(
                id=1,
                gender='Male',
                age=20,
                city='London',
                profession='Student',
                degree='BSc',
                cgpa=3.5,
                study_satisfaction=4.0,
                depression=True,
                suicidal_thoughts=False,
                family_history=False
            )
            lifestyle = LifestyleFactor(
                student_id=1,
                academic_pressure=3.0,
                work_pressure=0.0,
                job_satisfaction=0.0,
                sleep_duration='5-6 hours',
                dietary_habits='Healthy',
                work_study_hours=6.0,
                financial_stress=2.0
            )
            db.session.add(student)
            db.session.add(lifestyle)
            db.session.commit()
        response = self.client.get('/student/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student 1', response.data)
        self.assertIn(b'London', response.data)
        self.assertIn(b'5-6 hours', response.data)

    def test_404(self):
        response = self.client.get('/student/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 - Page Not Found', response.data)

    def test_analysis(self):
        with self.app.app_context():
            student = Student(
                id=1,
                gender='Male',
                age=20,
                city='London',
                profession='Student',
                degree='BSc',
                cgpa=3.5,
                study_satisfaction=4.0,
                depression=True,
                suicidal_thoughts=False,
                family_history=False
            )
            lifestyle = LifestyleFactor(
                student_id=1,
                academic_pressure=3.0,
                work_pressure=0.0,
                job_satisfaction=0.0,
                sleep_duration='5-6 hours',
                dietary_habits='Healthy',
                work_study_hours=6.0,
                financial_stress=2.0
            )
            db.session.add(student)
            db.session.add(lifestyle)
            db.session.commit()
        response = self.client.get('/analysis')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Analysis', response.data)
        self.assertIn(b'Depression Rate by City', response.data)

if __name__ == '__main__':
    unittest.main()