import pytest
from flask import json
from datetime import datetime, timedelta

def test_create_trip(client, test_app, test_db, auth_headers):
    """Test POST /api/trips endpoint"""
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
        assert response.json['destination'] == 'Tokyo'