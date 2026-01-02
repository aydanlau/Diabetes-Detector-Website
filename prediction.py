import pickle
import numpy as np
import pandas as pd
import os

def predictDiabetes(data):
    """
    Predict diabetes using the trained model and scaler.
    
    Args:
        data: pandas DataFrame with feature columns
        
    Returns:
        prediction: The predicted class (0 or 1) or probability
    """
    # Get the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'best_models', 'logistic_regression_model.pkl')
    scaler_path = os.path.join(base_dir, 'best_models', 'logistic_regression_scaler.pkl')
    
    # Load the scaler
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    # Load the model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    # Convert DataFrame to numpy array
    data_array = data.values
    
    # Scale the data
    scaled_data = scaler.transform(data_array)
    
    # Make prediction
    prediction = model.predict(scaled_data)[0]
    
    # Optionally get prediction probability
    prediction_proba = model.predict_proba(scaled_data)[0]

    print("prediction_proba", prediction_proba)
    
    return {""
        'prediction': int(prediction),
        'probability': {
            'no_diabetes': float(prediction_proba[0]),
            'diabetes': float(prediction_proba[1])
        }
    }
