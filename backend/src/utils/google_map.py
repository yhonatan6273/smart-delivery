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
        "mode": "driving",
        "key": GOOGLE_API_KEY
    }
    try:
        #sending the request to the Google Maps API and check if the response is ok
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        # if the response is not ok
        if data["status"] != "OK":
            print(f"google maps api could not find a route for '{origin}' to '{destination}'. Status: {data['status']}")
            return None
        
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
    except requests.exceptions.RequestException as e:
        print(f"a network error occurred: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"error parsing google maps response: {e}")
        return None
        