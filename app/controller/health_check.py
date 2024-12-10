from generated import ml_services_pb2

class HealthCheck:
    def HealthCheck(self, request, context):
        return ml_services_pb2.HealthResponse(status="OK")