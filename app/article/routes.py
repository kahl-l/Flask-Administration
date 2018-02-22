import os
from flask 				import render_template, flash, redirect, url_for, request, current_app
from flask_login 		import login_required, current_user
from app				import db
from app.article 		import bp
from app.article.forms	import AddArticleForm, EditArticleForm, AddImageForm, DeleteImageForm
from app.models			import User, Article, Image
from werkzeug.utils		import secure_filename

@bp.route('/list')
@login_required
def list():
	return render_template('article/list.html', title="Articles", articles=current_user.articles)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	form = AddArticleForm()
	if form.validate_on_submit():
		image = form.image.data
		filename = secure_filename(image.filename)
		image.save(os.path.join(current_app.root_path, 'static/images', filename))
		article = Article(title=form.title.data, summary=form.summary.data,
			content=form.content.data, image=filename, author=current_user)
		db.session.add(article)
		db.session.commit()
		flash('Your article is now live!', 'success')
		return redirect(url_for('article.list'))
	return render_template('article/add.html', title='Add article', form=form)

@bp.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
	article = Article.query.filter_by(id=id).first_or_404()
	if article.image is not None:
		os.remove(os.path.join(current_app.root_path, 'static/images', article.image))
	db.session.delete(article)
	db.session.commit()
	flash('Your article has been removed!', 'success')
	return redirect(url_for('article.list'))


@bp.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
	article = Article.query.filter_by(id=id).first_or_404()
	form = EditArticleForm(article.title)
	if form.validate_on_submit():
		article.title = form.title.data
		article.summary = form.summary.data
		article.content = form.content.data

		image = form.image.data
		if image is not None:
			filename = secure_filename(image.filename)
			if filename != article.image:
				os.remove(os.path.join(current_app.root_path, 'static/images', article.image))
				image.save(os.path.join(current_app.root_path, 'static/images', filename))
				article.image = filename
		db.session.commit()
		flash('Your changes have been saved.', 'success')
		return redirect(url_for('article.list'))
	elif request.method == 'GET':
		form.title.data = article.title
		form.summary.data = article.summary
		form.content.data = article.content
	return render_template('article/edit.html', title='Edit article', form=form, article=article)

@bp.route('/images', methods=['GET', 'POST'])
@login_required
def images():
	images = Image.query.all()
	form = AddImageForm()
	form2 = DeleteImageForm()
	form2.image.choices = [(row.id, "#" + str(row.id) + " " + row.name) for row in Image.query.all()]
	if form.image.data is not None and form.validate_on_submit():
		image = form.image.data
		filename = secure_filename(image.filename)
		image.save(os.path.join(current_app.root_path, 'static/images/', filename))
		image = Image(name=filename)
		db.session.add(image)
		db.session.commit()
		flash('Your image has been uploaded!', 'success')
		return redirect(url_for('article.images'))
	if form2.validate_on_submit():
		flash(form2.image.data, 'success')
		image = Image.query.filter_by(id=form2.image.data).first_or_404()
		os.remove(os.path.join(current_app.root_path, 'static/images', image.name))
		db.session.delete(image)
		flash('Your changes have been saved.', 'success')
		return redirect(url_for('article.images'))
	return render_template('article/images.html', title="Images", images=images, form=form, form2=form2)