from flask_wtf 			import FlaskForm
from flask_wtf.file 	import FileField, FileRequired, FileAllowed
from wtforms 			import StringField, TextAreaField, SubmitField
from wtforms.validators	import ValidationError, DataRequired, Length
from app.models			import Article

class ArticleForm(FlaskForm):
	title 	= StringField('Title', validators=[DataRequired(), Length(min=1, max=64)])
	summary = TextAreaField('Summary', validators=[DataRequired(), Length(min=1, max=800)])
	content = TextAreaField('Content', validators=[DataRequired(), Length(min=1, max=4800)])
	image	= FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images')])
	submit 	= SubmitField('Submit')

	def validate_title(self, title):
		article = Article.query.filter_by(title=title.data).first()
		if article is not None:
			raise ValidationError('Please use a different title.')