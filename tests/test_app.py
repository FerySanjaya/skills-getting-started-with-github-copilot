import pytest
from fastapi.testclient import TestClient
from src.app import app, activities as original_activities

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities database before each test"""
    # Store original activities
    original = original_activities.copy()
    
    # Clear original activities and set test data
    original_activities.clear()
    original_activities["Test Activity"] = {
        "description": "A test activity",
        "schedule": "Test schedule",
        "max_participants": 10,
        "participants": []
    }
    
    yield
    
    # Restore original activities
    original_activities.clear()
    original_activities.update(original)


def test_read_root():
    """Test that the root endpoint redirects to index.html"""
    response = client.get("/")
    assert response.status_code == 200


def test_get_activities():
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Test Activity" in data
    activity = data["Test Activity"]
    assert isinstance(activity, dict)
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity


def test_signup_for_activity():
    """Test signing up for an activity"""
    activity_name = "Test Activity"
    email = "test@mergington.edu"
    
    # Sign up for activity
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for {activity_name}"
    
    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity_name]["participants"]
    
    # Try to sign up again (should fail)
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity():
    """Test signing up for a non-existent activity"""
    response = client.post("/activities/NonexistentClub/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity():
    """Test unregistering from an activity"""
    activity_name = "Test Activity"
    email = "test_unreg@mergington.edu"
    
    # First sign up for the activity
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200
    
    # Now unregister
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Unregistered {email} from {activity_name}"
    
    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities[activity_name]["participants"]
    
    # Try to unregister again (should fail)
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_unregister_nonexistent_activity():
    """Test unregistering from a non-existent activity"""
    response = client.delete("/activities/NonexistentClub/unregister", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"