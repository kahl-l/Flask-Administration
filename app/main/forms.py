from flask 				import request
from flask_wtf 			import FlaskForm
from wtforms 			import StringField, TextAreaField, SubmitField
from wtforms.validators	import ValidationError, DataRequired, Length
from app.models			import User

class EditProfileForm(FlaskForm):
	first_name 	= StringField('First Name', validators=[DataRequired()])
	last_name 	= StringField('Last Name', validators=[DataRequired()])
	title 		= StringField('Title', validators=[DataRequired()])
	submit 		= SubmitField('Submit')

	def __init__(self, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)

class PostForm(FlaskForm):
	post 	= TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
	submit 	= SubmitField('Submit')