from flask_wtf 			import FlaskForm
from wtforms 			import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators	import ValidationError, DataRequired, Email, EqualTo, Length
from app.models 		import User

class LoginForm(FlaskForm):
	email 		= StringField('Email', validators=[DataRequired(), Email()])
	password 	= PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit 		= SubmitField('Sign in')

# class RegistrationForm(FlaskForm):
# 	first_name 	= StringField('First Name', validators=[DataRequired()])
# 	last_name 	= StringField('Last Name', validators=[DataRequired()])
# 	email 		= StringField('Email', validators=[DataRequired(), Email()])
# 	password 	= PasswordField('Password', validators=[DataRequired()])
# 	password2 	= PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
# 	title	 	= StringField('Title', validators=[DataRequired()])
# 	submit 		= SubmitField('Register')

# 	def validate_email(self, email):
# 		user = User.query.filter_by(email=email.data).first()
# 		if user is not None:
# 			raise ValidationError('Please use a different email address.')

class ResetPasswordRequestForm(FlaskForm):
	email 	= StringField('Email', validators=[DataRequired(), Email()])
	submit 	= SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
	password 	= PasswordField('Password', validators=[DataRequired()])
	password2 	= PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit 		= SubmitField('Request Password Reset')

class EditProfileForm(FlaskForm):
	first_name 	= StringField('First Name', validators=[DataRequired(), Length(min=1, max=64)])
	last_name 	= StringField('Last Name', validators=[DataRequired(), Length(min=1, max=64)])
	title 		= StringField('Title', validators=[DataRequired(), Length(min=1, max=64)])
	submit 		= SubmitField('Submit')