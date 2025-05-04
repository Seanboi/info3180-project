from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,FileField,SubmitField,PasswordField,SelectField,BooleanField,IntegerField,FloatField
from wtforms.validators import InputRequired, Optional, Length, NumberRange, ValidationError
import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired


class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = StringField('password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Register')
    
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
    
class ProfileForm(FlaskForm):
    description = StringField('Description', validators=[InputRequired(),Length(max=160, message="Description must be 160 characters or less")])
    
    parish = StringField('Parish', validators=[
        InputRequired(),
        Length(max=20, message="Parish must be 20 characters or less")
    ])
    
    biography = TextAreaField('Biography', validators=[
        InputRequired(),
        Length(max=300, message="Biography must be 300 characters or less")
    ])
    
    sex = SelectField('Sex', choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ], validators=[InputRequired()])
    
    race = StringField('Race', validators=[
        InputRequired(),
        Length(max=30, message="Race must be 30 characters or less")
    ])
    
    birth_year = IntegerField('Birth Year', validators=[
        InputRequired(),
        NumberRange(min=1900, max=datetime.datetime.now().year, 
                   message="Birth year must be between 1900 and the current year")
    ])
    
    height = FloatField('Height (in cm)', validators=[
        InputRequired(),
        NumberRange(min=50, max=250, message="Height must be between 50cm and 250cm")
    ])
    
    fav_cuisine = StringField('Favorite Cuisine', validators=[
        InputRequired(),
        Length(max=80, message="Favorite cuisine must be 80 characters or less")
    ])
    
    fav_colour = StringField('Favorite Color', validators=[
        InputRequired(),
        Length(max=80, message="Favorite color must be 80 characters or less")
    ])
    
    fav_school_subject = StringField('Favorite School Subject', validators=[
        InputRequired(),
        Length(max=80, message="Favorite school subject must be 80 characters or less")
    ])
    
    political = BooleanField('Political', default=False)
    
    religious = BooleanField('Religious', default=False)
    
    family_oriented = BooleanField('Family Oriented', default=False)
    
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    
    def validate_birth_year(self, field):
        current_year = datetime.datetime.now().year
        age = current_year - field.data
        if age < 18:
            raise ValidationError('You must be at least 18 years old to create a profile.')