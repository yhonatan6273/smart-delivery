from fastapi import APIRouter, HTTPException,Query
from src.utils.google_map import get_directions



router = APIRouter(prefix="/route",tags=["Directions"])



@router.get("")
#Function to get directions between two points using Google Maps API
def get_route(
    origin: str = Query(..., description="Starting point"),
    destination: str = Query(..., description="Destination point")
):
    try:
        directions = get_directions(origin, destination)
        return {
            "origin": origin,
            "destination": destination,
            "directions": directions
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
