import csv
from io import StringIO
from app.main import db
from app.main.model.cinemadata import CinemaData
from datetime import date
from datetime import datetime
from typing import Dict, Tuple, Union

    
def get_all_cinema_data(start_date: str = None, end_date: str = None):
    query = CinemaData.query
    if start_date:
        start_date = date.fromisoformat(start_date)
        query = query.filter(CinemaData.date >= start_date)
    if end_date:
        end_date = date.fromisoformat(end_date)
        query = query.filter(CinemaData.date <= end_date)
    return query.all()

def add_cinema_data_from_csv(csv_stream: StringIO) -> Tuple[Dict[str, str], int]:
    try:
        reader = csv.DictReader(csv_stream, delimiter=';')
        for row in reader:
            if not row['Visitor']:
                # If the visitor count is empty, skip this entry or handle it as needed
                continue
                
            new_cinema_data = CinemaData(
                day=row['Day'],
                date=datetime.strptime(row['Date'], '%d/%m/%Y'),
                visitors=int(row['Visitor'])
            )
            save_changes(new_cinema_data)

        response_object = {
            'status': 'success',
            'message': 'Successfully added data from CSV.',
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.',
            'error': str(e)
        }
        return response_object, 400

def save_changes(data: Union[CinemaData, None]) -> None:
    if data:
        db.session.add(data)
        db.session.commit()

def delete_all_cinema_data():
    try:
        # Delete all records from the table
        CinemaData.query.delete()
        db.session.commit()
        return None, 204
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred while deleting data. Please try again.',
            'error': str(e)
        }
        return response_object, 500



