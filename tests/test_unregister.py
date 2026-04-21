def test_unregister_success_removes_participant_and_returns_message(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.delete(endpoint, params={"email": email})
    body = response.json()
    activities_response = client.get("/activities")
    activities_body = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert body["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities_body[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    endpoint = "/activities/Unknown Activity/signup"

    # Act
    response = client.delete(endpoint, params={"email": "student@mergington.edu"})
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    endpoint = "/activities/Chess Club/signup"

    # Act
    response = client.delete(endpoint, params={"email": "notenrolled@mergington.edu"})
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == "Student is not signed up for this activity"
