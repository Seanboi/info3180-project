from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,FileField,SubmitField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired


class RegisterForm(FlaskForm):
    Fullname = StringField('Title', validators=[InputRequired()])
    username = StringField('Title', validators=[InputRequired()])
    password = StringField('Title', validators=[InputRequired()])
    email = StringField('Title', validators=[InputRequired()])
    photo = FileField('poster', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Register')
    
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])