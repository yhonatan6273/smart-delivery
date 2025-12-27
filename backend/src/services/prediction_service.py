import joblib
import pandas as pd
from src.schemas.prediction import DeliveryFeatures 
import os


#will go to three levels up from the current file location (backend folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#from backend to backend/ML/artifacts/eta_predictor_model.joblib
MODEL_PATH = os.path.join(BASE_DIR, "ML", "artifacts", "eta_predictor_model.joblib")


#Service class for handling predictions
class PredictionService:
    #function to initialize the service and load the model
    def __init__(self):
      
        self.model = joblib.load(MODEL_PATH)
        print("Prediction model loaded successfully.")
        
    #function to make prediction
    def predict(self, delivery_features: DeliveryFeatures) -> float:

        #convert pydantic model to dataframe
        data_df = pd.DataFrame([delivery_features.model_dump()])
        
        #make the prediction
        prediction = self.model.predict(data_df)
        
        return round(prediction[0], 2)

#create a singleton instance of the service to be used throughout the application
prediction_service = PredictionService()