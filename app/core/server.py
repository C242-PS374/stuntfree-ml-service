import asyncio
import logging
import os
import signal
import grpc
from concurrent import futures
from app.generated import ml_service_pb2_grpc
from app.controller import MLService
from app.core.config import configs

class GRPCServer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=os.cpu_count() * 2) 
        )
        self.register_services()

    def register_services(self):
        ml_service_pb2_grpc.add_MLServiceServicer_to_server(MLService(), self.server)

    async def serve(self):
        port = os.getenv("GRPC_SERVER_PORT", 50051)
        self.server.add_insecure_port(f"[::]:{port}")

        try:
            self.server.start()
            self.logger.info(f"gRPC Server is running on port {port}")
            await self.graceful_shutdown()
        except Exception as e:
            self.logger.error(f"Error starting gRPC server: {str(e)}", exc_info=True)
            raise

    async def graceful_shutdown(self):
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, self.shutdown_server)
        loop.add_signal_handler(signal.SIGINT, self.shutdown_server)
        await asyncio.Future()

    def shutdown_server(self):
        self.logger.info("Shutting down gRPC server...")
        self.server.stop(grace=5)
        self.logger.info("gRPC Server stopped successfully.")
