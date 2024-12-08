import joblib
import io
import os
from google.cloud import storage
from generated import ml_services_pb2
from generated import ml_services_pb2_grpc

class StuntingService(ml_services_pb2_grpc.MLServiceServicer):
    def __init__(self):
        self.model = self.load_model_local()

    def load_model_local(self):
        model_file_path = os.path.join(os.path.dirname(__file__), '..', 'public', 'knn_environment_status_model.pkl')

        if not os.path.exists(model_file_path):
            raise FileNotFoundError(f"Model file not found at {model_file_path}")

        model = joblib.load(model_file_path)
        return model

    def load_model_bucket(self):
        client = storage.Client()
        bucket_name = "model_buckets_ps374"
        model_file_name = ""

        bucket = client.bucket(bucket_name)
        blob = bucket.blob(model_file_name)
        
        model_file = io.BytesIO()
        blob.download_to_file(model_file)
        model_file.seek(0)

        model = joblib.load(model_file)
        return model

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
