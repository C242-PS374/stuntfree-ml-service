import joblib
import io
import os
# from google.cloud import storage
from generated import ml_services_pb2

class NutritionService:
    def __init__(self):
        self.model = self.load_model_local()

    def load_model_local(self):
        model_file_path = os.path.join(os.path.dirname(__file__), '..', 'public', 'knn_environment_status_model.pkl')

        if not os.path.exists(model_file_path):
            raise FileNotFoundError(f"Model file not found at {model_file_path}")

        model = joblib.load(model_file_path)
        return model

    # def load_model(self):
    #     client = storage.Client()
    #     bucket_name = ""
    #     model_file_name = ""

    #     bucket = client.bucket(bucket_name)
    #     blob = bucket.blob(model_file_name)
        
    #     model_file = io.BytesIO()
    #     blob.download_to_file(model_file)
    #     model_file.seek(0)

    #     model = joblib.load(model_file)
    #     return model

    def PredictNutrition(self, request, context):
        height = request.height
        weight = request.weight
        age = request.age
        
        input_data = [[height, weight, age]]

        prediction = self.model.predict(input_data)
        
        return ml_services_pb2.NutritionResponse(nutrition_status=str(prediction[0]))
