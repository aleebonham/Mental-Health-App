import unittest
from app import app, db
from models.models import Student, LifestyleFactor

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
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

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student Mental Health Dashboard', response.data)

    def test_students(self):
        response = self.app.get('/students')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Students', response.data)

    def test_student_page(self):
        response = self.app.get('/student/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Male', response.data) 
        self.assertIn(b'London', response.data)
        self.assertIn(b'3.0', response.data)  

    def test_404(self):
        response = self.app.get('/student/999')
        self.assertEqual(response.status_code, 404)

    def test_analysis(self):
        response = self.app.get('/analysis')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Depression by City', response.data)  

if __name__ == '__main__':
    unittest.main()