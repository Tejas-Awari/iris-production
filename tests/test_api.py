from fastapi.testclient import TestClient
from api.main import app

# Create a test client (like a fake web browser)
client = TestClient(app)

def test_health_check():
    """
    Test if the root endpoint returns status: healthy.
    This ensures the server can start and accept requests.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_predict_endpoint_validation():
    """
    Test that the API correctly rejects bad data.
    We send a string for 'sepal_length' instead of a float.
    """
    bad_payload = {
        "sepal_length": "this is not a number",
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/predict", json=bad_payload)
    
    # We expect a 422 Unprocessable Entity error
    assert response.status_code == 422