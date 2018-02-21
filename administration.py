from app 		import create_app, db
from app.models import User, Article, Image

app = create_app()

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Article': Article, 'Image': Image}