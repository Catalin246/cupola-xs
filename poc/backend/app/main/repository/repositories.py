from app.main.model import wifidata
from app.main import db

class WifiDataRepository:
    
    @staticmethod
    def get_all_wifi_data():
        return wifidata.query.all()
    
    @staticmethod
    def get_wifi_data_by_date(wifi_data_date):
        return wifidata.query.get(wifi_data_date)
    
    @staticmethod
    def add_wifi_data(wifi_data):
        db.session.add(wifi_data)
        db.session.commit
    
    @staticmethod
    def delete_wifi_data(wifi_data):
        db.session.delete(wifi_data)
        db.session.commit()