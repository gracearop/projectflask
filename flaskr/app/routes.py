from flask import Blueprint, render_template, jsonify, url_for

# mb = Blueprint('main', __name__)
mb = Blueprint('main', __name__, url_prefix='/students')

@mb.route('/std')
def index():
    print("Accessing /std route")
    return render_template('index.html')

@mb.route('/biodata')
def biodata():
    return render_template('biodata.html')

@mb.route('/fees')
def fees():
    return render_template('fees.html')

@mb.route('/otherFees')
def otherFees():
    return render_template('otherFees.html')

@mb.route('/courseReg')
def courseReg():
    return render_template('courseReg.html')

@mb.route('/results')
def results():
    return render_template('results.html')

@mb.route('/accommodation')
def accommodation():
    return render_template('accommodation.html')

@mb.route('/COP')
def COP():
    return render_template('changeOfProgramme.html')

@mb.route('/docs')
def docs():
    return render_template('myDocuments.html')

@mb.route('/settings')
def settings():
    return render_template('settings.html')


from . import auth
mb.register_blueprint(auth.bp)