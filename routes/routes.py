from flask import Blueprint, render_template, request, abort
from models.models import db, Student, LifestyleFactor
from sqlalchemy import select, func, cast, Integer
import sqlalchemy.exc

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
        query = query.filter(Student.city == city)
    students = query.paginate(page=page, per_page=10)
    print(f"Students found: {students.total}")  # Debug
    return render_template('students.html', students=students)

@bp.route('/student/<int:id>')
def student(id):
    try:
        student = Student.query.get_or_404(id)
        lifestyle = LifestyleFactor.query.filter_by(student_id=id).first()
        return render_template('student.html', student=student, lifestyle=lifestyle)
    except sqlalchemy.exc.OperationalError:
        abort(404)

@bp.route('/analysis')
def analysis():
    try:
        city_depression = db.session.execute(
            select(
                Student.city,
                func.avg(cast(Student.depression, Integer)).label('depression_rate')
            ).group_by(Student.city)
        ).all()
        pressure_depression = db.session.execute(
            select(
                LifestyleFactor.academic_pressure,
                func.avg(cast(Student.depression, Integer)).label('depression_rate')
            ).join(Student, Student.id == LifestyleFactor.student_id).group_by(LifestyleFactor.academic_pressure)
        ).all()
        print(f"City depression data: {city_depression}")  # Debug
        print(f"Pressure depression data: {pressure_depression}")  # Debug
        return render_template('analysis.html', city_depression=city_depression, pressure_depression=pressure_depression)
    except sqlalchemy.exc.OperationalError as e:
        print(f"Analysis error: {str(e)}")
        return render_template('analysis.html', city_depression=[], pressure_depression=[])

@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500