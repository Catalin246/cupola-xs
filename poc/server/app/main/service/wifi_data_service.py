from app.main import db

from ..model.wifi_data import WifiData
from app.main.util.dto import WifiDataDto
    
def get_all_wifi_data():
    return WifiData.query.all()

def get_wifi_data_by_date(wifi_data_date):
    return WifiData.query.get(wifi_data_date)

def add_wifi_data(wifi_data):
    db.session.add(wifi_data)
    db.session.commit

def delete_wifi_data(wifi_data):
    db.session.delete(wifi_data)
    db.session.commit()