from .. import db, flask_bcrypt

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class WifiData(db.Model):
    __tablename__ = "wifidata"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, nullable=False)
    totalonlinedevices = db.Column(db.Integer, nullable=False)