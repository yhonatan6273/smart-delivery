

def test_get_route_success(client, monkeypatch):
   #we are making a fake response from the google maps api
    fake_directions_result = {
        "distance": "120 km",
        "duration": "1 hour 15 mins",
        "summary": "through Highway 6"
    }

    #this is the function that will replace the real get_directions function
    def mock_get_directions(origin, destination):
        return fake_directions_result

    #to replace the real get_directions function with our mock function 
    #we use monkeypatch.setattr
    monkeypatch.setattr("src.router.maps.get_directions", mock_get_directions)

    #we call the endpoint with test client
    res = client.get("/route?origin=Tel Aviv&destination=Haifa")

    assert res.status_code == 200
    response_data = res.json()
    assert response_data["origin"] == "Tel Aviv"
    assert response_data["destination"] == "Haifa"
    assert response_data["directions"] == fake_directions_result



def test_get_route_failure(client, monkeypatch):
   #we create a mock function that simulates a failure in the get_directions function
    def mock_get_directions_fails(origin, destination):
        raise ValueError("Invalid address provided to Google Maps")

    #we replace the real get_directions function with our mock function
    monkeypatch.setattr("src.router.maps.get_directions", mock_get_directions_fails)

    #we call the endpoint with test client
    res = client.get("/route?origin=InvalidPlace&destination=Nowhere")

    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid address provided to Google Maps"

#for missing required query parameters
def test_get_route_missing_param(client):
    res = client.get("/route?origin=Tel Aviv")
    assert res.status_code == 422