from flask 			import render_template, flash, redirect, url_for, request
from werkzeug.urls 	import url_parse
from flask_login 	import current_user, login_user, logout_user, login_required
from app			import db
from app.user 		import bp
from app.user.forms	import LoginForm, ResetPasswordRequestForm, ResetPasswordForm, EditProfileForm
from app.models		import User
from app.user.email import send_password_reset_email

@bp.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid email or password', 'error')
			return redirect(url_for('user.login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('main.index')
		return redirect(next_page)
	return render_template('user/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))

# @bp.route('/register', methods=['GET', 'POST'])
# def register():
# 	if current_user.is_authenticated:
# 		return redirect(url_for('main.index'))
# 	form = RegistrationForm()
# 	if form.validate_on_submit():
# 		user = User(first_name=form.first_name.data, last_name=form.last_name.data,
# 			email=form.email.data, title=form.title.data)
# 		user.set_password(form.password.data)
# 		db.session.add(user)
# 		db.session.commit()
# 		flash('Congratulations, you are now a registered user!', 'success')
# 		return redirect(url_for('user.login'))
# 	return render_template('user/register.html', title='Register', form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash('Check your email for the instructions to reset your password')
		return redirect(url_for('user.login'))
	return render_template('user/reset_password_request.html', title='Reset Passsword', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('main.index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been reset.', 'success')
		return redirect(url_for('user.login'))
	return render_template('user/reset_password.html', form=form)

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
		return redirect(url_for('user.edit_profile'))
	elif request.method == 'GET':
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name
		form.title.data = current_user.title
	return render_template('user/edit_profile.html', title='Edit Profile', form=form)

@bp.route('/profile')
@login_required
def profile(id):
	return render_template('user/profile.html', title="Profile")