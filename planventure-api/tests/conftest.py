import pytest
from app import app, db
from models import User, Trip
from datetime import datetime, timedelta


@pytest.fixture
def test_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

# Add this new fixture
@pytest.fixture
def client(test_app):
    return test_app.test_client()

@pytest.fixture
def test_db(test_app):
    with test_app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture
def test_user(test_app, test_db):
    with test_app.app_context():
        # Delete any existing users first
        User.query.delete()
        db.session.commit()
        
        # Create new test user
        user = User(
            email='test@example.com',
            is_verified=True
        )
        user.password = 'password123'
        db.session.add(user)
        db.session.commit()
        
        # Refresh the user object to ensure it's attached to the session
        db.session.refresh(user)
        return user

@pytest.fixture
def test_trip(test_app, test_user):
    with test_app.app_context():
        trip = Trip(
            user_id=test_user.id,
            destination='Paris',
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=5),
            latitude=48.8566,
            longitude=2.3522,
            itinerary={'day1': ['Visit Eiffel Tower']}
        )
        db.session.add(trip)
        db.session.commit()
        db.session.refresh(trip)
        return trip

@pytest.fixture
def auth_headers(test_user):
    token = test_user.generate_auth_token()  # Assuming you have this method
    return {'Authorization': f'Bearer {token}'}