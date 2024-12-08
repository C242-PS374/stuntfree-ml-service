import joblib
import io
import os
from google.cloud import storage
from generated import ml_services_pb2
from generated import ml_services_pb2_grpc

class NutritionService(ml_services_pb2_grpc.MLServiceServicer):
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
    
    def nutrition_threshold(stage, age):
        if (stage == "pregnancy"):
            if (age >= 1 and age <= 13):
                return 
            elif (age >= 14 and age <= 27):
                return
            elif (age >= 28 and age <= 41):
                return
            else:
                return
        
        if (stage == "infancy"):
            if (age >= 0 and age <= 6):
                return
            elif (age >= 7 and age <= 11):
                return 
            elif (age >= 12 and age <= 36):
                return
            elif (age >= 37 and age <= 72):
                return
            else:
                return

    
    def check_nutrition_pregnancy(age):
        # age on week
        if (age >= 1 and age <= 13):
            pass
        elif (age >= 14 and age <= 27):
            pass
        elif (age >= 28 and age <= 41):
            pass
        else:
            pass

    def check_nutrition_infancy(age):
        # age on month
        if (age >= 0 and age <= 6):
            pass
        elif (age >= 7 and age <= 11):
            pass
        elif (age >= 12 and age <= 36):
            pass
        elif (age >= 37 and age <= 72):
            pass
        else:
            pass

    def PredictNutrition(self, request, context):
        stage = request.stage
        if (stage == "pregnancy"):
            pass
        
        if (stage == "infancy"):
            pass
        
        return 
