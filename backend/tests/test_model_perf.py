import pytest
import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error
import os
#this test will load the trained ML model and a test dataset and will verify that the model mean absolute error is below a certain threshold.
@pytest.mark.ml
def test_model_mae_below_threshold():
    def get_correct_path(relative_path):
        
        if os.path.exists(f"backend/{relative_path}"):
            return f"backend/{relative_path}"
        #inside the docker
        return relative_path
    model_path = get_correct_path("ML/artifacts/eta_predictor_model.joblib")
    X_path = get_correct_path("ML/data/test_set_X.csv")
    y_path = get_correct_path("ML/data/test_set_y.csv")
    #load the trained model (that the notebook created)
    #change the path accordingly
    try:
        loaded_model = joblib.load(model_path)
    except FileNotFoundError:
        pytest.fail("Model file not found. Did you train it and commit the file?")

    #load the test dataset
    try:
        X_test = pd.read_csv(X_path)
        y_test = pd.read_csv(y_path)
    except FileNotFoundError:
        pytest.fail("Test dataset files (X_test or y_test) not found.")
    #do the predictions on the test set
    y_pred = loaded_model.predict(X_test)
    #calculate the mean absolute error (MAE) between the predicted and actual values
    mae = mean_absolute_error(y_test, y_pred) 
    #define an acceptable error threshold (10 minutes in this case) 
    maximum_error_threshold = 10.0 
    
    #assert that the MAE is below the threshold 
    #if not, the test will fail and print an error message
    assert mae < maximum_error_threshold, f"model MAE ({mae:.3f}) is above the threshold ({maximum_error_threshold})"
