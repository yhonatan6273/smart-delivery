import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Function to check if the address is valid
# Using google maps API
def validate_address(address: str):
    #Google Geocoding API
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_API_KEY,
        #validate address only in israel
        "components": "country:IL"
    }
    try:
        response = requests.get(endpoint, params=params)
        # make the respone as json
        data = response.json()
        # The address is not valid
        if data["status"] != "OK":
            return None
        # The full address 
        result = data['results'][0]
        result_types = result.get('types', [])
        # Check if Google returned the whole country instead of a specific address
        if "country" in result_types and "political" in result_types and len(result_types) == 2:
            return None
        return result['formatted_address']
        
    except Exception as e:
        print(f"error checking address {e}")
        return None
    
def get_lat_long(address: str):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_API_KEY
    }
    try:
        response = requests.get(endpoint, params=params)
        data = response.json()

        if data["status"] != "OK":
            return None, None

        # Extract lat and lng from the geometry section
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']

    except Exception as e:
        print(f"Error getting coordinates: {e}")
        return None, None

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
            return None


        route = data["routes"][0]
        leg = data["routes"][0]["legs"][0]
        #getting the steps we need to take to get to the destination
        steps= []
        for step in leg["steps"]:
             steps.append(step["html_instructions"])
        #getting the distance between the two locations,duration of the trip and the steps we need to take
        #and how the path will look
        result = {
            "distance": leg["distance"]["text"],
            "duration": leg["duration"]["text"],
            "steps": steps,
            "polyline": route["overview_polyline"]["points"]
        }

        return result
    except requests.exceptions.RequestException as e:
        print(f"a network error occurred: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"error parsing google maps response: {e}")
        return None

