from app.main import db
from app.main.model.cinemadata import CinemaData
from datetime import date
from datetime import datetime
from typing import Dict, Tuple
    
def get_all_cinema_data(start_date: str = None, end_date: str = None):
    query = CinemaData.query
    if start_date:
        start_date = date.fromisoformat(start_date)
        query = query.filter(CinemaData.date >= start_date)
    if end_date:
        end_date = date.fromisoformat(end_date)
        query = query.filter(CinemaData.date <= end_date)
    return query.all()

def add_cinema_data(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        new_cinema_data = CinemaData(
            day = data['day'],
            date  = datetime.strptime(data['date'], '%d-%m-%Y'),
            visitors = data['visitors'],
        )
        
        return save_changes(new_cinema_data)
           
def save_changes(data: CinemaData) -> None:
    db.session.add(data)
    db.session.commit()
    try:
        response_object = {
            'status': 'success',
            'message': 'Successfully added data.',
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401



