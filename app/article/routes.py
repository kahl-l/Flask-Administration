from flask 			import render_template
from flask_login 	import login_required
from app			import db
from app.article 	import bp
from app.models		import User, Article

@bp.route('/<user_id>')
@login_required
def list(user_id):
	user = User.query.filter_by(id=user_id).first_or_404()
	return render_template('article/list.html', title="Articles", user=user.articles)