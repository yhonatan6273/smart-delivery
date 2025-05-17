from fastapi import APIRouter, HTTPException,Query
from backend.utils.google_map import get_directions



router = APIRouter(prefix="/route",tags=["maps"])



@router.get("")

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
