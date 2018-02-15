from datetime 			import datetime
from hashlib 			import md5
from time 				import time
from flask 				import current_app
from flask_login	 	import UserMixin
from werkzeug.security 	import generate_password_hash, check_password_hash
import jwt
from app 				import db, login

class User(UserMixin, db.Model):
	id 				= db.Column(db.Integer, primary_key=True)
	first_name 		= db.Column(db.String(64))
	last_name		= db.Column(db.String(64))
	email 			= db.Column(db.String(120), index=True, unique=True)
	password_hash 	= db.Column(db.String(128))
	posts 			= db.relationship('Post', backref='author', lazy='dynamic')
	title 			= db.Column(db.String(64))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
				digest, size)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in},
			current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithm=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

	def __repr__(self):
		return '<User {}>'.format(self.id)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))