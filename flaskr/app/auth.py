import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
# from flaskr.app import routes
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def process_login(matric_number, student_password):
    db = get_db()
    student = db.execute(
        'SELECT * FROM student WHERE matric_number = ?', (matric_number,)
    ).fetchone()

    if student is None:
        return False
    elif not check_password_hash(student['student_password'], student_password):
        return False

    session.clear()
    session['user_id'] = student['student_id']
    return True

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        student_name = request.form['student_name']
        student_password = request.form['student_password']
        matric_number = request.form['matric_number']
        student_level = request.form['student_level']
        student_state = request.form['student_state']
        email = request.form['email']
        programme_type = request.form['programme_type']
        department = request.form['department']
        local_government = request.form['local_government']
        phone_number = request.form['phone_number']
        year_of_admission = request.form['year_of_admission']
        faculty = request.form['faculty']
        programme = request.form['programme']
        db = get_db()
        error = None

        if not student_name:
            error = 'Name is required.'
        elif not student_password:
            error = 'Password is required.'
        elif not matric_number:
            error = 'Matric number is required.'
        elif not student_level:
            error = 'Level is required.'
        elif not student_state:
            error = 'State is required.'
        elif not email:
            error = 'Email is required.'
        elif not programme_type:
            error = 'Programme type is required.'
        elif not department:
            error = 'Department is required.'
        elif not local_government:
            error = 'Local government is required.'
        elif not phone_number:
            error = 'Phone number is required.'
        elif not year_of_admission:
            error = 'Year of admission is required.'
        elif not faculty:
            error = 'Faculty is required.'
        elif not programme:
            error = 'Programme is required.'
        elif db.execute(
            'SELECT student_id FROM student WHERE student_name = ? OR matric_number = ? OR email = ? OR phone_number = ?',
            (student_name, matric_number, email, phone_number)
        ).fetchone() is not None:
            error = 'Student with the same name, matric number, email, or phone number already exists.'

        if error is None:
            db.execute(
                'INSERT INTO student (student_name, student_password, matric_number, student_level, student_state, email, programme_type, department, local_government, phone_number, year_of_admission, faculty, programme) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (student_name, generate_password_hash(student_password), matric_number, student_level, student_state, email, programme_type, department, local_government, phone_number, year_of_admission, faculty, programme)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        matric_number = request.form['matric_number']
        student_password = request.form['student_password']
        db = get_db()
        error = None
        student = db.execute(
            'SELECT * FROM student WHERE matric_number = ?', (matric_number,)
        ).fetchone()

        if student is None:
            error = 'Incorrect matric number.'
        elif not check_password_hash(student['student_password'], student_password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = student['student_id']
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html')

# def process_login(matric_number, student_password, label):
#     db = get_db()
#     error = None
#     student = db.execute(
#         'SELECT * FROM student WHERE matric_number = ?', (matric_number,)
#     ).fetchone()

#     if student is None:
#         error = 'Incorrect matric number.'
#     elif not check_password_hash(student['student_password'], student_password):
#         error = 'Incorrect password.'

#     if error is None:
#         session.clear()
#         session['user_id'] = student['student_id']

#         # Mapping dictionary for post-login redirect
#         label_to_route = {
#             '__label__std': 'index',
#             '__label__biodata': 'biodata',
#             '__label__fees': 'fees',
#             '__label__otherfees': 'otherFees',
#             '__label__coursereg': 'courseReg',
#             '__label__results': 'results',
#             '__label__accommodation': 'accommodation',
#             '__label__cop': 'COP',
#             '__label__docs': 'myDocuments',
#             '__label__settings': 'settings',
#         }

#         route_name = label_to_route.get(label, None)
#         if not route_name:
#             return jsonify({'error': 'No matching route for label'}), 400

#         route_url = url_for(f'main.{route_name}')
#         return redirect(route_url)

#     flash(error)
#     return render_template('auth/login.html')



@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM student WHERE student_id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


