import os
import io
import grpc
import keras
import numpy as np

from PIL import Image
from google.cloud import storage

from core.config import configs
from generated import ml_services_pb2

class ImageService:
    def __init__(self):
        self.model_path = self.download_model()
        self.model = self.load_model()

    def download_model(self):
        client = storage.Client()
        bucket = client.bucket(configs.MODEL_BUCKET)
        blob = bucket.blob(configs.IMAGE_MODEL_PATH)

        local_model_path = os.path.join(os.path.dirname(__file__), 'model/image_model.keras')

        if not os.path.exists(os.path.dirname(local_model_path)):
            os.makedirs(os.path.dirname(local_model_path), exist_ok=True)

            print("Downloading image scan model from GCS...")
            blob.download_to_filename(local_model_path)
            print("Image scan model downloaded successfully.")
        
        
        return local_model_path

    def load_model(self):
        try:
            model = keras.saving.load_model(self.model_path)
            print("Image scan model loaded successfully.")
            return model
        except Exception as e:
            with open(self.model_path, 'rb') as f:
                    print("File contents (first 100 bytes):")
                    print(f.read(100))

            print(f"Error loading model: {e}")
            raise

    def ImageDetection(self, request, context):
        class_mapping = {
            1: 'Ayam',
            2: 'Bakso',
            3: 'Cumi',
            4: 'Gado Gado',
            5: 'Gudeg',
            6: 'Ikan',
            7: 'Nasi',
            8: 'Pempek',
            9: 'Sate',
            10: 'Soto'
        }

        try:
            model = self.load_model()
            confidence_threshold: float = 0.75

            image_bytes = request.image_data
            image = Image.open(io.BytesIO(image_bytes))

            image = image.convert("RGB").resize((224, 224))
            image_array = np.expand_dims(np.array(image) / 255.0, axis=0).astype('float32')

            predictions = model.predict(image_array)  # type: ignore

            predicted_bboxes = predictions[0][0]  
            predicted_labels = predictions[1][0]  

            result = []
            for i in range(predicted_bboxes.shape[0]):
                if np.any(predicted_bboxes[i] != 0):
                    class_id = np.argmax(predicted_labels[i])
                    confidence = np.max(predicted_labels[i])

                    print(f"Predicted class: {class_mapping.get(int(class_id), "unknown")}, Confidence: {confidence}")

                    if confidence >= confidence_threshold:
                        result.append(class_mapping.get(int(class_id), "unknown"))

            if len(result) == 0:
                return ml_services_pb2.ImageResponse(result="unknown")

            return ml_services_pb2.ImageResponse(result=",".join(result))
        
        except Exception as e:
            print(f"Error in ImageDetection: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return ml_services_pb2.ImageResponse(result="error")

        

    
