import csv
from io import StringIO
from datetime import datetime
from app.main import db
from ..model.wifi_data import WifiData
from typing import Dict, Tuple, Union
import re
from flask import jsonify

def get_all_wifi_data():
    return WifiData.query.all()

def get_wifi_data_by_date(wifi_data_date):
    return WifiData.query.get(wifi_data_date)

def get_earliest_wifi_data():
    return WifiData.query.order_by(WifiData.date).first()

def add_wifi_data(data: Dict[str, str]) -> None:
    new_wifi_data = WifiData(
        date = datetime.strptime(data['date'], '%d-%m-%Y'),
        total_online_devices = data['total_online_devices']
    )


def add_wifi_data_from_csv(csv_stream: StringIO) -> Tuple[Dict[str, str], int]:
    try:
        reader = csv.DictReader(csv_stream, delimiter=',')
        for row in reader:
            cleaned_value = re.sub(r'\D', '', row['Total Online Devices'])
            # Check if the cleaned value can be converted to an integer
            if cleaned_value.isdigit():
                total_online_devices = int(cleaned_value)
                # Extract the start date and time from 'Date Time'
                date_time_str = row["Date Time"].split(' - ')[0]
                try:
                    date_time_obj = datetime.strptime(date_time_str, '%d-%m-%Y %H:%M:%S')
                except ValueError:
                    # Handle date parsing error, skip this entry
                    continue
                existing_record = WifiData.query.filter_by(date=date_time_obj).first()
                if existing_record:
                     existing_record.total_online_devices = total_online_devices
                     add_to_database(existing_record)
                else:
                     new_wifi_data = WifiData(
                    date=date_time_obj,
                    total_online_devices=total_online_devices
                )
                     add_to_database(new_wifi_data)    

            else:
                # Skip the entry if it cannot be converted to an integer
                continue

        return ({"message": "Data added successfully"}), 201

    except Exception as e:
        # Handle exceptions
        return ({"message": str(e)}), 500


def delete_wifi_data():
  try:
        # Delete all records from the table
        WifiData.query.delete()
        db.session.commit()
        return None, 204
  except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred while deleting data. Please try again.',
            'error': str(e)
        }
        return response_object, 500

def add_to_database(data: WifiData) -> None:
    db.session.add(data)
    db.session.commit()