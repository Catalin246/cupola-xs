from .. import db, flask_bcrypt

class CinemaData(db.Model):
    """ Cinema Data Model for storing details regarding cinema visitors over time """

    __tablename__ = "cinemadata"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    visitors = db.Column(db.Integer, nullable=False)