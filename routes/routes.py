from flask import Blueprint, render_template, request
from models.models import db, Student, LifestyleFactor
from sqlalchemy import func

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/students')
def students():
    page = request.args.get('page', 1, type=int)
    city = request.args.get('city', None)
    query = Student.query
    if city:
        query = query.filter_by(city=city)
    pagination = query.paginate(page=page, per_page=50, error_out=False)
    return render_template('students.html', pagination=pagination, city=city)

@bp.route('/student/<int:id>')
def student(id):
    student = Student.query.get_or_404(id)
    return render_template('student.html', student=student)

@bp.route('/analysis')
def analysis():
    # Depression rate by city
    city_stats = db.session.query(
        Student.city,
        func.avg(Student.depression.cast(db.Integer)).label('depression_rate')
    ).group_by(Student.city).all()
    # Depression by academic pressure
    pressure_stats = db.session.query(
        LifestyleFactor.academic_pressure,
        func.avg(Student.depression.cast(db.Integer)).label('depression_rate')
    ).join(Student).group_by(LifestyleFactor.academic_pressure).all()
    return render_template('analysis.html', city_stats=city_stats, pressure_stats=pressure_stats)

@bp.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404

@bp.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error), 500