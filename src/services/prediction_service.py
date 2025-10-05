import joblib
import pandas as pd
from src.schemas.prediction import DeliveryFeatures 


MODEL_PATH = "ML/artifacts/eta_predictor_model.joblib"

class PredictionService:
    def __init__(self):
       #load the model that we trained
        self.model = joblib.load(MODEL_PATH)
        print("Prediction model loaded successfully.")

    def predict(self, delivery_features: DeliveryFeatures) -> float:

        #convert pydantic model to dataframe
        data_df = pd.DataFrame([delivery_features.model_dump()])
        
        #make the prediction
        prediction = self.model.predict(data_df)
        
        return round(prediction[0], 2)

#create a singleton instance of the service to be used throughout the application
prediction_service = PredictionService()