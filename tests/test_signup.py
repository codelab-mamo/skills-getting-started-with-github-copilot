def test_signup_success_adds_participant_and_returns_message(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})
    body = response.json()
    activities_response = client.get("/activities")
    activities_body = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert body["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities_body[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    endpoint = "/activities/Unknown Activity/signup"

    # Act
    response = client.post(endpoint, params={"email": "student@mergington.edu"})
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": existing_email})
    body = response.json()

    # Assert
    assert response.status_code == 400
    assert body["detail"] == "Student already signed up for this activity"
