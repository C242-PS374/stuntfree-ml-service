from generated import ml_services_pb2, ml_services_pb2_grpc

class HealthCheck(ml_services_pb2_grpc.MLServiceServicer):
    def HealthCheck(self, request, context):
        return ml_services_pb2.HealthResponse(status="OK")