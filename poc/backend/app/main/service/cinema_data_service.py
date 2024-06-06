import csv
from io import StringIO
from app.main import db
from app.main.model.cinemadata import CinemaData
from datetime import date
from datetime import datetime
from typing import Dict, Tuple, Union

    
def get_all_cinema_data():
    return CinemaData.query.all()

def add_cinema_data_from_csv(csv_stream: StringIO) -> Tuple[Dict[str, str], int]:
    try:
        reader = csv.DictReader(csv_stream, delimiter=';')
        for row in reader:
            if not row['Visitor']:
                # If the visitor count is empty, skip this entry or handle it as needed
                continue

            parsed_date = datetime.strptime(row['Date'], '%d/%m/%Y').date()
            existing_record = CinemaData.query.filter_by(date=parsed_date).first()
            if existing_record:
                existing_record.day = row['Day']
                existing_record.visitors = int(row['Visitor'])
                save_changes(existing_record)
            else:
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



