import os
import unittest
import datetime

from flask_migrate import Migrate

from app import blueprint
from app.main import create_app, db
from app.main.model import user

app = create_app(os.getenv('CUPOLAXS_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=user)