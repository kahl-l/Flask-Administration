from flask 				import render_template, flash, redirect, url_for
from flask_login 		import login_required, current_user
from app				import db
from app.article 		import bp
from app.article.forms	import AddArticleForm
from app.models			import User, Article

@bp.route('/list')
@login_required
def list():
	return render_template('article/list.html', title="Articles", articles=current_user.articles)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	form = AddArticleForm()
	if form.validate_on_submit():
		article = Article(title=form.title.data, summary=form.summary.data,
			content=form.content.data, author=current_user)
		db.session.add(article)
		db.session.commit()
		flash('Your article is now live!', 'success')
		return redirect(url_for('article.list'))
	return render_template('article/add.html', title='Add article', form=form)

@bp.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
	article = Article.query.filter_by(id=id).first_or_404()
	db.session.delete(article)
	db.session.commit()
	flash('Your article has been removes!', 'success')
	return redirect(url_for('article.list'))