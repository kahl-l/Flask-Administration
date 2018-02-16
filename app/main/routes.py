from datetime 		import datetime
from flask			import render_template, flash, redirect, url_for, request, current_app
from flask_login 	import current_user, login_required
from app 			import db
from app.main.forms import EditProfileForm
from app.models 	import User
from app.main 		import bp

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	return render_template('index.html', title='Home')

@bp.route('/user/<id>')
@login_required
def user(id):
	user = User.query.filter_by(id=id).first_or_404()
	return render_template('user.html', title="Profile", user=user)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.first_name = form.first_name.data
		current_user.last_name = form.last_name.data
		current_user.title = form.title.data
		db.session.commit()
		flash('Your changes have been saved.', 'success')
		return redirect(url_for('main.edit_profile'))
	elif request.method == 'GET':
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name
		form.title.data = current_user.title
	return render_template('edit_profile.html', title='Edit Profile', form=form)