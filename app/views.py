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
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
from functools import wraps
from .models import Users
from.models import Favourite
from .models import Profile
from .forms import RegisterForm
from .forms import LoginForm
from .forms import ProfileForm
from flask import Flask, send_from_directory 
import jwt
import os
import datetime

###
# Routing for your application.
###

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory(app.static_folder, path)



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

@app.route('/api/register', methods=['POST'])
def register():
    try:
        # Get fields from request.form
        name = request.form.get('name', '').strip()
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        photo_file = request.files.get('photo')

        if not all([name, username, password, email, photo_file]):
            return jsonify({"error": True, "message": "Missing required fields"}), 400

        names = name.split(" ", 1)
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ''

        # Save the uploaded file
        filename = secure_filename(photo_file.filename)
        upload_folder = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        photo_path = os.path.join(upload_folder, filename)
        photo_file.save(photo_path)

        # Create and add the new user
        new_user = Users(
            name=first_name + " " + last_name,
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

    except Exception as e:
        print("Error during registration:", str(e))
        return jsonify({"error": True, "message": "Server error"}), 500

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@app.route('/api/auth/login',methods=['POST'])
def login():
    form = LoginForm()

    # change this to actually validate the entire form submission
    # and not just one field
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Query the database for the user
        user = db.session.execute(db.select(Users).filter_by(username=username)).scalar()

        # Check if user exists and verify password
        if user and check_password_hash(user.password, password):
            login_user(user)
            
            token_payload = {
                'user_id': user.id,
                'username': user.username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expires in 1 day
            }
            
            # Create the JWT token
            token = jwt.encode(
                token_payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            
            
            return jsonify({
                'error': False,
                'message': 'Login successful',
                'token': token,
                'user_id': user.id,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'username': user.username,
                    'email': user.email,
                    # Include other user fields as needed
                }
            }), 200
        else:
            return jsonify({
                'error': True,
                'message': 'Invalid username or password'
            }), 401
    else:
        # Form validation failed
        errors = form_errors(form)
        return jsonify({
            'error': True,
            'errors': errors
        }), 400




@app.route('/api/auth/logout',methods=['POST'])
@login_required 
def logout():
    logout_user()
    
    return jsonify({
        'error': False,
        'message': 'Logged out successfully'
    }), 200


@app.route('/api/profiles',methods=['GET','POST'])
def profiles():
    # GET request: Return all profiles
    if request.method == 'GET':
        # Get query parameters for filtering/pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        show_latest = request.args.get('latest', '0') == '1'  # New flag
        
        # Optional filtering by parameters
        filters = {}
        for param in ['parish', 'sex', 'race']:
            if param in request.args and request.args[param]:
                filters[param] = request.args[param]
                
        # Apply filters if any exist
        query = Profile.query
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Profile, key) == value)
                
        if show_latest:
            query = query.order_by(Profile.id.desc())
        
        # Execute query with pagination
        profiles_pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        profiles_list = profiles_pagination.items
        
        # Prepare response data
        result = []
        for profile in profiles_list:
            # Get the associated user
            user = Users.query.get(profile.user_id_fk)
            
            # Skip if user doesn't exist
            if not user:
                continue
                
            # Build profile data with user information
            profile_data = {
                'id': profile.id,
                'user_id': profile.user_id_fk,
                'username': user.username,
                'name': user.name,
                'photo': user.photo,
                'description': profile.description,
                'parish': profile.parish,
                'biography': profile.biography,
                'sex': profile.sex,
                'race': profile.race,
                'birth_year': profile.birth_year,
                'height': profile.height,
                'fav_cuisine': profile.fav_cuisine,
                'fav_colour': profile.fav_colour,
                'fav_school_subject': profile.fav_school_subject,
                'political': profile.political,
                'religious': profile.religious,
                'family_oriented':profile.family_oriented,
                'photo': profile.photo
            }
            result.append(profile_data)
        
        # Return paged results
        return jsonify({
            'error': False,
            'profiles': result,
            'pagination': {
                'total': profiles_pagination.total,
                'pages': profiles_pagination.pages,
                'page': page,
                'per_page': per_page,
                'has_next': profiles_pagination.has_next,
                'has_prev': profiles_pagination.has_prev
            }
        }), 200
    
    # POST request: Create a new profile
    elif request.method == 'POST':
        # Ensure user is authenticated for profile creation
        if not current_user.is_authenticated:
            return jsonify({
                'error': True,
                'message': 'You must be logged in to create a profile'
            }), 401
        
        # Check if user already has a profile
        
        # Create and validate form
        form = ProfileForm()
        
        # Handle JSON data from Vue.js
        if request.is_json:
            json_data = request.get_json()
            for field in form._fields:
                if field in json_data:
                    form._fields[field].data = json_data[field]
        
        # Validate form data
        if form.validate_on_submit():
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            upload_folder = os.path.join(os.getcwd(), 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            photo_path = os.path.join(upload_folder, filename)
            photo.save(photo_path)
            # Create new profile
            new_profile = Profile(
                user_id_fk=current_user.id,
                description=form.description.data,
                parish=form.parish.data,
                biography=form.biography.data,
                sex=form.sex.data,
                race=form.race.data,
                birth_year=form.birth_year.data,
                height=form.height.data,
                fav_cuisine=form.fav_cuisine.data,
                fav_colour=form.fav_colour.data, 
                fav_school_subject=form.fav_school_subject.data,
                political=form.political.data,
                religious=form.religious.data,
                family_oriented=form.family_oriented.data,
                photo=filename
            )
            
            # Save to database
            db.session.add(new_profile)
            db.session.commit()
            
            return jsonify({
                'error': False,
                'message': 'Profile created successfully',
                'profile': {
                    'id': new_profile.id,
                    'user_id': new_profile.user_id_fk,
                    'description': new_profile.description,
                    'parish': new_profile.parish,
                    'biography': new_profile.biography,
                    'sex': new_profile.sex,
                    'race': new_profile.race,
                    'birth_year': new_profile.birth_year,
                    'height': new_profile.height,
                    'fav_cuisine': new_profile.fav_cuisine,
                    'fav_colour': new_profile.fav_colour,
                    'fav_school_subject': new_profile.fav_school_subject,
                    'political': new_profile.political,
                    'religious': new_profile.religious,
                    'family_oriented': new_profile.family_oriented,
                    'photo':new_profile.photo
                }
            }), 201
        else:
            # Return validation errors
            errors = form_errors(form)
            return jsonify({
                'error': True,
                'errors': errors
            }), 400




@app.route('/api/profiles/<profile_id>',methods=['GET'])
@login_required
def get_profile(profile_id):
    # Query the database for the profile
    profile = Profile.query.get(profile_id)
    
    # Check if profile exists
    if not profile:
        return jsonify({
            'error': True,
            'message': 'Profile not found'
        }), 404
    
    # Get the associated user
    user = Users.query.get(profile.user_id_fk)
    
    # Check if user exists
    if not user:
        return jsonify({
            'error': True,
            'message': 'Associated user not found'
        }), 404
    
    # Build profile data with user information
    profile_data = {
        'id': profile.id,
        'user_id': profile.user_id_fk,
        'username': user.username,
        'name': user.name,
        'photo': user.photo,
        'description': profile.description,
        'parish': profile.parish,
        'biography': profile.biography,
        'sex': profile.sex,
        'race': profile.race,
        'birth_year': profile.birth_year,
        'height': profile.height,
        'fav_cuisine': profile.fav_cuisine,
        'fav_colour': profile.fav_colour,
        'fav_school_subject': profile.fav_school_subject,
        'political': profile.political,
        'religious': profile.religious,
        'family_oriented':profile.family_oriented,
        'photo':profile.photo
    }
    
    return jsonify({
        'error': False,
        'profile': profile_data
    }), 200



@app.route('/api/profiles/<user_id>/favourite',methods=['POST'])
@login_required
def add_to_favourites(user_id):
    
    # Check if the user to be favorited exists
    user_to_favourite = Users.query.get(user_id)
    if not user_to_favourite:
        return jsonify({
            'error': True,
            'message': 'User not found'
        }), 404
    
    # Check if the user is trying to favorite themselves
    if current_user.id == int(user_id):
        return jsonify({
            'error': True,
            'message': 'You cannot add yourself to favorites'
        }), 400
    
    # Check if this user is already in favorites
    existing_favourite = Favourite.query.filter_by(
        user_id_fk=current_user.id,
        fav_user_id_fk=user_id
    ).first()
    
    if existing_favourite:
        return jsonify({
            'error': True,
            'message': 'This user is already in your favourites'
        }), 409  # Conflict
    
    # Create new favourite relationship
    new_favourite = Favourite(
        user_id_fk=current_user.id,
        fav_user_id_fk=user_id
    )
    
    # Save to database
    db.session.add(new_favourite)
    db.session.commit()
    
    return jsonify({
        'error': False,
        'message': 'User added to favourites successfully',
        'favourite': {
            'id': new_favourite.id,
            'user_id': new_favourite.user_id_fk,
            'favourite_user_id': new_favourite.fav_user_id_fk
        }
    }), 201



@app.route('/api/profiles/matches/<int:profile_id>', methods=['GET'])
@login_required
def get_profile_matches(profile_id):
    # Fetch the source profile
    source_profile = Profile.query.get(profile_id)
    if not source_profile:
        return jsonify({'error': True, 'message': 'Profile not found'}), 404

    # Ensure the user has permission to view this profile's matches
    if source_profile.user_id_fk != current_user.id:
        return jsonify({'error': True, 'message': 'You do not have permission to view matches for this profile'}), 403

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Build the initial query, excluding the source profile
    query = Profile.query.filter(Profile.id != profile_id)

    # Apply "opposite sex" filter if required
    if request.args.get('match_opposite_sex', 'true').lower() == 'true':
        if source_profile.sex == 'Male':
            query = query.filter(Profile.sex == 'Female')
        elif source_profile.sex == 'Female':
            query = query.filter(Profile.sex == 'Male')

    # Paginate the query results
    profiles_pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    profiles_list = profiles_pagination.items

    # List to store matched profiles
    result = []

    # Define match criteria
    criteria = {
        'match_parish': lambda p: p.parish == source_profile.parish,
        'match_age': lambda p: abs(p.birth_year - source_profile.birth_year) <= 5,
        'match_height': lambda p: abs(p.height - source_profile.height) <= 10,
        'match_cuisine': lambda p: p.fav_cuisine == source_profile.fav_cuisine,
        'match_colour': lambda p: p.fav_colour == source_profile.fav_colour,
        'match_subject': lambda p: p.fav_school_subject == source_profile.fav_school_subject,
        'match_political': lambda p: p.political == source_profile.political,
        'match_religious': lambda p: p.religious == source_profile.religious,
        'match_family': lambda p: p.family_oriented == source_profile.family_oriented
    }

    # Process each profile
    for profile in profiles_list:
        user = Users.query.get(profile.user_id_fk)
        if not user:
            continue  # Skip if no user associated with the profile

        match_score = 0
        total_criteria = 0

        # Check each match criterion dynamically
        for criterion, check in criteria.items():
            if request.args.get(criterion, 'true').lower() == 'true':
                total_criteria += 1
                if check(profile):
                    match_score += 1

        # Calculate match percentage
        match_percentage = (match_score / total_criteria * 100) if total_criteria > 0 else 0

        # Create a dictionary with the profile data and match score
        profile_data = {
            'id': profile.id,
            'user_id': profile.user_id_fk,
            'username': user.username,
            'name': user.name,
            'photo': user.photo,
            'description': profile.description,
            'parish': profile.parish,
            'biography': profile.biography,
            'sex': profile.sex,
            'race': profile.race,
            'birth_year': profile.birth_year,
            'height': profile.height,
            'fav_cuisine': profile.fav_cuisine,
            'fav_colour': profile.fav_colour,
            'fav_school_subject': profile.fav_school_subject,
            'political': profile.political,
            'religious': profile.religious,
            'family_oriented': profile.family_oriented,
            'photo': profile.photo,
            'match_score': match_score,
            'match_percentage': round(match_percentage, 1)
        }

        result.append(profile_data)

    # Include the source_profile data in the response
    response_data = {
        'error': False,
        'matches': result,
        'source_profile': {
            'id': source_profile.id,
            'height': source_profile.height,
            'fav_cuisine': source_profile.fav_cuisine,
            'fav_colour': source_profile.fav_colour,
            'fav_school_subject': source_profile.fav_school_subject,
            'political': source_profile.political,
            'religious': source_profile.religious,
            'family_oriented': source_profile.family_oriented
        },
        'pagination': {
            'total': profiles_pagination.total,
            'pages': profiles_pagination.pages,
            'page': page,
            'per_page': per_page,
            'has_next': profiles_pagination.has_next,
            'has_prev': profiles_pagination.has_prev
        }
    }

    return jsonify(response_data), 200






@app.route('/api/search',methods=['GET'])
@login_required
def search_profiles():
    # Get search parameters from query string
    name = request.args.get('name', '').strip()
    birth_year = request.args.get('birth_year', type=int)
    sex = request.args.get('sex', '').strip()
    race = request.args.get('race', '').strip()
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Check if at least one search parameter is provided
    if not any([name, birth_year, sex, race]):
        return jsonify({
            'error': True,
            'message': 'At least one search parameter (name, birth_year, sex, race) must be provided'
        }), 400
    
    # Start with a query that joins User and Profile to search across both tables
    query = db.session.query(Profile, Users).join(Users, Profile.user_id_fk == Users.id)
    
    # Apply filters based on provided parameters
    if name:
        query = query.filter(Users.name.ilike(f'%{name}%'))
    
    if birth_year:
        query = query.filter(Profile.birth_year == birth_year)
    
    if sex:
        query = query.filter(Profile.sex.ilike(f'%{sex}%'))
    
    if race:
        query = query.filter(Profile.race.ilike(f'%{race}%'))
    
    # Count total results for pagination info (before applying pagination)
    total_results = query.count()
    
    # Apply pagination
    paginated_results = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Prepare response data
    result = []
    for profile, user in paginated_results.items:
        profile_data = {
            'id': profile.id,
            'user_id': profile.user_id_fk,
            'username': user.username,
            'name': user.name,
            'photo': user.photo,
            'description': profile.description,
            'parish': profile.parish,
            'biography': profile.biography,
            'sex': profile.sex,
            'race': profile.race,
            'birth_year': profile.birth_year,
            'height': profile.height,
            'fav_cuisine': profile.fav_cuisine,
            'fav_colour': profile.fav_colour,
            'fav_school_subject': profile.fav_school_subject,
            'political': profile.political,
            'religious': profile.religious,
            'family_oriented': profile.family_oriented,
            'photo':profile.photo
        }
        result.append(profile_data)
    
    # Return search results with pagination info
    return jsonify({
        'error': False,
        'message': f'Found {total_results} matching profiles',
        'results': result,
        'pagination': {
            'total': total_results,
            'pages': paginated_results.pages,
            'page': page,
            'per_page': per_page,
            'has_next': paginated_results.has_next,
            'has_prev': paginated_results.has_prev
        }
    }), 200



@app.route('/api/users/<user_id>',methods=['GET'])
@login_required
def get_user_details(user_id):
    # Query the database for the user
    user = Users.query.get(user_id)
    
    
    
    # Check if user exists
    if not user:
        return jsonify({
            'error': True,
            'message': 'User not found'
        }), 404
    
    # Check if the user has a profile
    profiles = Profile.query.filter_by(user_id_fk=user_id).all()
    
    # Create the response data
    user_data = {
    'id': user.id,
    'username': user.username,
    'name': user.name,
    'email': user.email,
    'photo': user.photo,
    'date_joined': user.date_joined.isoformat() if user.date_joined else None,
    'has_profile': len(profiles) > 0,
    'profiles': [{
        'id': p.id,
        'description': p.description,
        'parish': p.parish,
        'biography': p.biography,
        'sex': p.sex,
        'race': p.race,
        'birth_year': p.birth_year,
        'height': p.height,
        'fav_cuisine': p.fav_cuisine,
        'fav_colour': p.fav_colour,
        'fav_school_subject': p.fav_school_subject,
        'political': p.political,
        'religious': p.religious,
        'family_oriented': p.family_oriented,
        'photo': p.photo
    } for p in profiles]
}

    
    # Add favorite count information
    favorite_count = Favourite.query.filter_by(fav_user_id_fk=user_id).count()
    user_data['favorite_count'] = favorite_count
    
    # Check if logged in user has favorited this user
    is_favorited = False
    if current_user.is_authenticated:
        is_favorited = Favourite.query.filter_by(
            user_id_fk=current_user.id,
            fav_user_id_fk=user_id
        ).first() is not None
    
    user_data['is_favorited'] = is_favorited
    
    # Return the user data
    return jsonify({
        'error': False,
        'user': user_data
    }), 200



@app.route('/api/users/<user_id>/favourites',methods=['GET'])
@login_required
def getuserfavourites(user_id):
    # Check if the user exists
    user = Users.query.get(user_id)
    if not user:
        return jsonify({
            'error': True,
            'message': 'User not found'
        }), 404
    
    # Check permissions - either the request is for the current user's favorites,
    # or the current user has admin privileges (if implemented)
    if not current_user.is_authenticated and user_id != current_user.id:
        return jsonify({
            'error': True,
            'message': 'You can only view your own favorites'
        }), 403
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Query for all favorites of this user with pagination
    favourites_query = db.session.query(Favourite, Users, Profile)\
        .join(Users, Favourite.fav_user_id_fk == Users.id)\
        .outerjoin(Profile, Profile.user_id_fk == Users.id)\
        .filter(Favourite.user_id_fk == user_id)
    
    # Apply pagination
    favourites_pagination = favourites_query.paginate(page=page, per_page=per_page, error_out=False)
    favourites_list = favourites_pagination.items
    
    # Prepare response data
    result = []
    for favourite, fav_user, profile in favourites_list:
        # Build user data
        favourite_data = {
            'id': favourite.id,
            'favorited_user': {
                'id': fav_user.id,
                'username': fav_user.username,
                'name': fav_user.name,
                'photo': fav_user.photo
            }
        }
        
        # Include profile information if available
        if profile:
            favourite_data['profile'] = {
                'id': profile.id,
                'description': profile.description,
                'parish': profile.parish,
                'biography': profile.biography,
                'sex': profile.sex,
                'race': profile.race,
                'birth_year': profile.birth_year,
                'height': profile.height,
                'fav_cuisine': profile.fav_cuisine,
                'fav_colour': profile.fav_colour,
                'fav_school_subject': profile.fav_school_subject,
                'political': profile.political,
                'religious': profile.religious,
                'family_oriented': profile.family_oriented,
                'photo': profile.photo
            }
        
        result.append(favourite_data)
    
    # Return the favorites list with pagination info
    return jsonify({
        'error': False,
        'user_id': user_id,
        'username': user.username,
        'favourites': result,
        'pagination': {
            'total': favourites_pagination.total,
            'pages': favourites_pagination.pages,
            'page': page,
            'per_page': per_page,
            'has_next': favourites_pagination.has_next,
            'has_prev': favourites_pagination.has_prev
        }
    }), 200



@app.route('/api/users/favourites/<int:n>',methods=['GET'])
@login_required
def gettop_favourited_users(n):
    # Validate the input parameter
    if n <= 0:
        return jsonify({
            'error': True,
            'message': 'Parameter N must be a positive integer'
        }), 400
    
    # Set a reasonable maximum to prevent excessive queries
    max_limit = 50
    if n > max_limit:
        n = max_limit
    
    # Query for users with the count of times they've been favorited
    # Using a subquery to count favorites and then joining with Users and Profile tables
    favorited_users = db.session.query(
        Users,
        Profile,
        db.func.count(Favourite.id).label('favorite_count')
    ).join(
        Favourite, Users.id == Favourite.fav_user_id_fk
    ).outerjoin(
        Profile, Users.id == Profile.user_id_fk
    ).group_by(
        Users.id, Profile.id
    ).order_by(
        db.desc('favorite_count')
    ).limit(n).all()
    
    # Prepare response data
    result = []
    for user, profile, count in favorited_users:
        # Build user data with favorite count
        user_data = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'photo': user.photo,
            'favorite_count': count
        }
        
        # Include profile information if available
        if profile:
            user_data['profile'] = {
                'id': profile.id,
                'description': profile.description,
                'parish': profile.parish,
                'biography': profile.biography,
                'sex': profile.sex,
                'race': profile.race,
                'birth_year': profile.birth_year,
                'height': profile.height,
                'fav_cuisine': profile.fav_cuisine,
                'fav_colour': profile.fav_colour,
                'fav_school_subject': profile.fav_school_subject,
                'political': profile.political,
                'religious': profile.religious,
                'family_oriented': profile.family_oriented
            }
        
        # Check if current user has favorited this user (if logged in)
        is_favorited = False
        if current_user.is_authenticated:
            is_favorited = Favourite.query.filter_by(
                user_id_fk=current_user.id,
                fav_user_id_fk=user.id
            ).first() is not None
        
        user_data['is_favorited'] = is_favorited
        
        result.append(user_data)
    
    # Return the list of top favorited users
    return jsonify({
        'error': False,
        'top_users': result,
        'count': len(result),
        'limit': n
    }), 200




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
def page_not_found(e):
    return jsonify({"error": "Not Found"}), 404


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if Authorization header exists and has Bearer token
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({
                'error': True,
                'message': 'Authentication token is missing'
            }), 401
        
        try:
            # Decode the token
            data = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            
            # Get the user from the token
            current_user_id = data['user_id']
            current_user = Users.query.get(current_user_id)
            
            if not current_user:
                raise Exception('User not found')
                
        except jwt.ExpiredSignatureError:
            return jsonify({
                'error': True,
                'message': 'Token has expired'
            }), 401
        except (jwt.InvalidTokenError, Exception) as e:
            return jsonify({
                'error': True,
                'message': f'Invalid token: {str(e)}'
            }), 401
            
        # Pass the user to the decorated function
        return f(current_user, *args, **kwargs)
    
    return decorated