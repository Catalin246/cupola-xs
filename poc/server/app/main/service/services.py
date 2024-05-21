from app.main.model import wifidata
from app.main.repository.repositories import WifiDataRepository
from app.main.util.dto import WifiDataDto

class WifiDataService:
    
    @staticmethod
    def get_all_wifi_data():
        return WifiDataRepository.get_all_wifi_data()
    
    @staticmethod
    def get_wifi_data_by_date(wifi_data_date):
        return WifiDataRepository.get_wifi_data_by_date(wifi_data_date)
    
    @staticmethod
    def add_wifi_data(wifi_data_dto: WifiDataDto):
        wifi_data = wifidata(date=wifi_data_dto.date, total_online_devices=wifi_data_dto.total_online_devices)
        WifiDataRepository.add_wifi_data(wifi_data)
        return wifi_data
    
    @staticmethod
    def delete_wifi_data(wifi_data_date):
        wifi_data = WifiDataRepository.get_wifi_data_by_date(wifi_data_date)
        if wifi_data:
            WifiDataRepository.delete_wifi_data(wifi_data)
        return wifi_data