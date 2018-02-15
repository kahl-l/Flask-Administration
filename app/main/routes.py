from datetime 		import datetime
from flask			import render_template, flash, redirect, url_for, request, current_app
from flask_login 	import current_user, login_required
from app 			import db
from app.main.forms import EditProfileForm, PostForm
from app.models 	import User, Post
from app.main 		import bp

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	form = PostForm()
	if (form.validate_on_submit()):
		post = Post(body=form.post.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post is now live!', 'success')
		return redirect(url_for('main.index'))
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.timestamp.desc()).paginate(
		page, current_app.config['POSTS_PER_PAGE'], False) # or current_user.posts
	next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html', title='Home', form=form, posts=posts.items,
		 next_url=next_url, prev_url=prev_url)

@bp.route('/user/<id>')
@login_required
def user(id):
	user = User.query.filter_by(id=id).first_or_404()
	return render_template('user.html', title="Profile", user=user, posts=user.posts)

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