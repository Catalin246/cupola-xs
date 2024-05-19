import os
import unittest

from flask_migrate import Migrate
from .main.model import models

from app.main import create_app, db

app = create_app(os.getenv('CUPOLAXS_ENV') or 'dev')

app.app_context().push()


migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
