from datetime import datetime

from app.main import db

from ..model.wifi_data import WifiData

from typing import Dict
    
def get_all_wifi_data():
    return WifiData.query.all()

def get_wifi_data_by_date(wifi_data_date):
    return WifiData.query.get(wifi_data_date)

def add_wifi_data(data: Dict[str, str]) -> None:
    new_wifi_data = WifiData(
        date = datetime.strptime(data['date'], '%d-%m-%Y'),
        total_online_devices = data['total_online_devices']
    )

    add_to_database(new_wifi_data)

def delete_wifi_data(wifi_data):
    db.session.delete(wifi_data)
    db.session.commit()

def add_to_database(data: WifiData) -> None:
    db.session.add(data)
    db.session.commit()