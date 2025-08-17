import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#function to check if the address is valid
#using google maps API
def validate_address(address: str):
    #Google Geocoding API
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_API_KEY
    }
    response = requests.get(endpoint, params=params)
    #make the respone as json
    data = response.json()
    # the address is not valid
    if data["status"] != "OK":
        return False
    # the address is valid
    return True



## Function to get directions between two locations
## using google maps API
def get_directions(origin: str, destination: str):
    endpoint = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": GOOGLE_API_KEY
    }
    #sending the request to the Google Maps API and check if the response is ok
    response = requests.get(endpoint, params=params)
    data = response.json()
    # if the response is not ok
    if data["status"] != "OK":
        raise Exception(f"Error from Google Maps API: {data['status']}")
    
    leg = data["routes"][0]["legs"][0]
    #getting the steps we need to take to get to the destination
    steps = [step["html_instructions"] for step in leg["steps"]]
    #getting the distance between the two locations,duration of the trip and the steps we need to take
    result = {
        "distance": leg["distance"]["text"],
        "duration": leg["duration"]["text"],
        "steps": steps
    }

    return result
    