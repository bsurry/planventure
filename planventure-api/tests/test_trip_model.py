import pytest
from models import Trip
from datetime import datetime, timedelta

def test_new_trip(test_app, test_db, test_user):
    """Test creating a new trip"""
    start_date = datetime.now()
    end_date = start_date + timedelta(days=5)
    
    trip = Trip(
        user_id=test_user.id,
        destination='Tokyo',
        start_date=start_date,
        end_date=end_date,
        itinerary={'day1': ['Visit Tokyo Tower']}
    )
    
    assert trip.destination == 'Tokyo'
    assert trip.user_id == test_user.id
    assert trip.start_date == start_date
    assert trip.end_date == end_date
    assert trip.latitude is None
    assert trip.longitude is None
    assert 'day1' in trip.itinerary
    assert len(trip.itinerary['day1']) == 1
    assert trip.itinerary['day1'][0] == 'Visit Tokyo Tower'

def test_trip_to_dict(test_app, test_db, test_trip):
    """Test trip serialization"""
    trip_dict = test_trip.to_dict()
    
    assert trip_dict['destination'] == 'Paris'
    assert 'start_date' in trip_dict
    assert 'end_date' in trip_dict
    assert 'itinerary' in trip_dict

def test_trip_dates_end_before_start_validation(test_app, test_db, test_user):
    """Test trip dates validation"""
    start_date = datetime.now()
    end_date = start_date - timedelta(days=1)  # End date before start date
    
    with pytest.raises(ValueError):
        Trip(
            user_id=test_user.id,
            destination='Berlin',
            start_date=start_date,
            end_date=end_date
        )

def test_trip_dates_not_datetime_validation(test_app, test_db, test_user):
    """Test trip dates validation for non-datetime values"""
    start_date = '2023-10-01'  # Not a datetime object
    end_date = '2023-10-05'  # Not a datetime object
    
    with pytest.raises(ValueError):
        Trip(
            user_id=test_user.id,
            destination='Berlin',
            start_date=start_date,
            end_date=end_date
        )

def test_trip_itinerary_default(test_app, test_db, test_user):
    """Test default itinerary generation"""
    start_date = datetime.strptime('2025-06-01', '%Y-%m-%d')
    end_date = datetime.strptime('2025-06-03', '%Y-%m-%d')
    
    # Generate itinerary
    itinerary = Trip.generate_default_itinerary(start_date, end_date)
    
    
    # Assertions
    assert isinstance(itinerary, dict)
    assert len(itinerary) == 3  # 3 days of activities
    
    # Check first day structure
    assert 'day1' in itinerary
    assert 'date' in itinerary['day1']
    assert 'activities' in itinerary['day1']
    assert len(itinerary['day1']['activities']) == 5  # 5 activities per day
    
    # Verify dates are correct
    assert itinerary['day1']['date'] == '2025-06-01'
    assert itinerary['day2']['date'] == '2025-06-02'
    assert itinerary['day3']['date'] == '2025-06-03'