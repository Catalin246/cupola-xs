from .. import db

class WifiData(db.Model):
    """ Wifi Data Model for storing details regarding online devices over time """

    __tablename__ = "wifidata"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, nullable=False)
    total_online_devices = db.Column(db.Integer, nullable=False)
