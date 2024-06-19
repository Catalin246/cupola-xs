from .. import db
from datetime import datetime

class AIModel(db.Model):
    """ AIModel for storing details regarding models over time """

    __tablename__ = "aimodel"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    model_name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    mean_squared_error = db.Column(db.Float, nullable=False)
    mean_absolute_error = db.Column(db.Float, nullable=False)
    r2_score = db.Column(db.Float, nullable=False)
    model_type = db.Column(db.String(50), nullable=False)

    def __init__(self, model_name, mean_squared_error, mean_absolute_error, r2_score, model_type, is_active=True):
        self.model_name = model_name
        self.mean_squared_error = mean_squared_error
        self.mean_absolute_error = mean_absolute_error
        self.r2_score = r2_score
        self.model_type = model_type
        self.is_active = is_active
        self.date = datetime.utcnow()
