from pydantic import BaseModel

#this schema defines the features required for making a delivery time prediction
class DeliveryFeatures(BaseModel):
    distance_km: float
    maps_eta_minutes: float
    hour_of_day: int
    day_of_week: int
