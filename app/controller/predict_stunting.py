import joblib
import io
import os
from google.cloud import storage
from generated import ml_services_pb2

from core.config import configs

class StuntingService:
    def __init__(self):
        self.model_path = self.download_model()
        self.model = self.load_model()

    def download_model(self):
        client = storage.Client()
        bucket = client.bucket(configs.MODEL_BUCKET)
        blob = bucket.blob(configs.STUNTING_MODEL_PATH)

        local_model_path = os.path.join(os.path.dirname(__file__), 'model/stunting_model.joblib')
        if not os.path.exists(local_model_path):
            os.makedirs(os.path.dirname(local_model_path), exist_ok=True)

            print("Downloading predict stunting model from GCS...")
            blob.download_to_filename(local_model_path)
            print("predict stunting model downloaded successfully.")

        return local_model_path

    def load_model(self):
        try:
            model = joblib.load(self.model_path)
            print("Predict stunting model loaded successfully.")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def PredictStunting(self, request, context):
        age = request.age
        birth_weight = request.birth_weight
        birth_length = request.birth_length
        body_weight = request.body_weight
        body_length = request.body_length
        is_sanitized_place = request.is_sanitized_place
        is_healthy_food = request.is_healthy_food
        
        input_data = [[age, birth_weight, birth_length, body_weight, body_length, is_sanitized_place, is_healthy_food]] 
        
        prediction = self.model.predict(input_data)
        
        return ml_services_pb2.StuntingResponse(stunting_status=str(prediction[0]))
