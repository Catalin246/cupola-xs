from .. import db, flask_bcrypt

class WifiData(db.Model):
    """ Wifi Data Model for storing details regarding online devices over time """

    __tablename__ = "wifidata"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, nullable=False)
    totalonlinedevices = db.Column(db.Integer, nullable=False)
