"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from app.models import Users
from app.forms import RegisterForm
from app.forms import LoginForm
import re
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.route('/api/register',methods=['POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        fullname = form.fullname.data.strip()
        username = form.username.data
        password = form.password.data
        email = form.email.data
        photo_file = form.photo.data

        names = fullname.split(" ", 1)
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ''

        filename = secure_filename(photo_file.filename)
        photo_path = os.path.join('uploads', filename)
        photo_file.save(photo_path)

        new_user = Users(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
            photo=filename
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'error': False,
            'message': 'User registered successfully',
            'user': {
                'id': new_user.id,
                'name': new_user.name,
                'username': new_user.username,
                'email': new_user.email,
                'date_joined': new_user.date_joined
            }
        }), 201
    else:
        return jsonify({
            'error': True,
            'message': 'Form validation failed',
            'errors': form_errors(form)
        }), 400




@app.route('/api/auth/login',methods=['POST'])
def login():
    return 1





@app.route('/api/auth/logout',methods=['POST'])



@app.route('/api/profiles',methods=['GET','POST'])



@app.route('/api/profiles/{profile_id}',methods=['GET'])



@app.route('/api/profiles/{user_id}/favourite',methods=['POST'])



@app.route('/api/profiles/matches/{profile_id}',methods=['GET'])



@app.route('/api/search',methods=['GET'])



@app.route('/api/users/{user_id}',methods=['GET'])



@app.route('/api/users/{user_id}/favourites',methods=['GET'])



@app.route('/api/users/favourties/{N}',methods=['GET'])




@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404