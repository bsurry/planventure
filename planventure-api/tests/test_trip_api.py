import pytest
from flask import json
from datetime import datetime, timedelta

def test_create_trip_default_data(client, test_app, auth_headers):
    """Test POST /api/trips endpoint, min data"""
    with test_app.app_context():
        data = {
            'destination': 'Tokyo',
            'start_date': datetime.now().date().isoformat(),
            'end_date': (datetime.now() + timedelta(days=5)).date().isoformat()
        }
        
        response = client.post('/api/trips', 
                             data=json.dumps(data),
                             headers=auth_headers,
                             content_type='application/json')
        
        assert response.status_code == 201
        assert response.json['message'] == 'Trip created'
        assert response.json['destination'] == 'Tokyo'
        assert 'trip_id' in response.json
        assert response.json['start_date'] == data['start_date']
        assert response.json['end_date'] == data['end_date']
        assert 'latitude' not in response.json
        assert 'longitude' not in response.json
        assert 'itinerary' in response.json
        assert 'day1' in response.json['itinerary']
        assert 'day2' in response.json['itinerary']
        assert len(response.json['itinerary']) == 6

def test_create_trip_all_data(client, test_app, auth_headers):
    """Test POST /api/trips endpoint"""
    with test_app.app_context():
        data = {
            'destination': 'Tokyo',
            'start_date': datetime.now().date().isoformat(),
            'end_date': (datetime.now() + timedelta(days=5)).date().isoformat(),
            'latitude': 35.6895,
            'longitude': 139.6917,
            'itinerary': {
                'day1': ['Visit Tokyo Tower'],
                'day2': ['Explore Shibuya']
            }
        }
        
        response = client.post('/api/trips', 
                             data=json.dumps(data),
                             headers=auth_headers,
                             content_type='application/json')
        
        assert response.status_code == 201
        assert response.json['message'] == 'Trip created'
        assert response.json['destination'] == 'Tokyo'
        assert 'trip_id' in response.json
        assert response.json['start_date'] == data['start_date']
        assert response.json['end_date'] == data['end_date']
        assert 'latitude' not in response.json
        assert 'longitude' not in response.json
        assert 'itinerary' in response.json
        assert 'day1' in response.json['itinerary']
        assert 'day2' in response.json['itinerary']
        assert len(response.json['itinerary']['day1']) == 1
        assert response.json['itinerary']['day1'][0] == 'Visit Tokyo Tower'
        assert len(response.json['itinerary']['day2']) == 1
        assert response.json['itinerary']['day2'][0] == 'Explore Shibuya'

def test_create_trip_invalid_dates(client, test_app, auth_headers):
    """Test POST /api/trips endpoint with invalid dates"""
    with test_app.app_context():
        data = {
            'destination': 'Tokyo',
            'start_date': (datetime.now() + timedelta(days=5)).date().isoformat(),
            'end_date': datetime.now().date().isoformat()
        }
        
        response = client.post('/api/trips', 
                             data=json.dumps(data),
                             headers=auth_headers,
                             content_type='application/json')
        
        assert response.status_code == 400
        assert response.json['message'] == 'End date cannot be before start date'
    
def test_create_trip_with_itinerary_invalid_dates(client, test_app, auth_headers):
    """Test POST /api/trips endpoint with invalid dates"""
    with test_app.app_context():
        data = {
            'destination': 'Tokyo',
            'start_date': (datetime.now() + timedelta(days=5)).date().isoformat(),
            'end_date': datetime.now().date().isoformat(),
            'itinerary': {
                'day1': ['Visit Tokyo Tower'],
                'day2': ['Explore Shibuya']
            }
        }
        
        response = client.post('/api/trips', 
                             data=json.dumps(data),
                             headers=auth_headers,
                             content_type='application/json')
        
        assert response.status_code == 400
        assert response.json['message'] == 'End date cannot be before start date'
    
def test_create_trip_invalid_dates_not_datetime(client, test_app, auth_headers):
    """Test POST /api/trips endpoint with invalid dates"""
    with test_app.app_context():
        data = {
            'destination': 'Tokyo',
            'start_date': 'DEC 1 2025',  # Not a datetime object
            'end_date': 'DEC 6 2025'  # Not a datetime object
        }
        
        response = client.post('/api/trips', 
                             data=json.dumps(data),
                             headers=auth_headers,
                             content_type='application/json')
        
        assert response.status_code == 400
        assert response.json['message'] == "time data 'DEC 1 2025' does not match format '%Y-%m-%d'"