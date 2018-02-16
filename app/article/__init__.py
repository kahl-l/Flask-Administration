from flask 		import Blueprint

bp = Blueprint('article', __name__)

from app.article import routes