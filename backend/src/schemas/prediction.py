from pydantic import BaseModel


class DeliveryFeatures(BaseModel):
    distance_km: float
    maps_eta_minutes: float
    hour_of_day: int
    day_of_week: int
