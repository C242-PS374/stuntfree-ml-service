import asyncio
import grpc
import logging
import os
import signal
import platform
from concurrent import futures
from generated import ml_services_pb2_grpc
from controller.health_check import HealthCheck
from controller.predict_nutrition import NutritionService
from controller.predict_stunting import StuntingService
from controller.image_detection import ImageService

class GRPCServer:
    def __init__(self):
        self.logger = logging.getLogger("GRPCServer")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=(os.cpu_count() or 1) * 2)
        )
        self.port = int(os.getenv("GRPC_SERVER_PORT", 50051))
        self._register_services()

    def _register_services(self):
        try:
            ml_services_pb2_grpc.add_MLServiceServicer_to_server(ml_services_pb2_grpc.MLServiceServicer(), self.server)
            self.logger.info("All gRPC services registered successfully.")
        except Exception as e:
            self.logger.error(f"Failed to register services: {str(e)}", exc_info=True)
            raise

    async def start(self):
        try:
            self.server.add_insecure_port(f"[::]:{self.port}")
            self.server.start()
            self.logger.info(f"gRPC Server running on port http://localhost:{self.port}")
            await self._wait_for_termination()
        except Exception as e:
            self.logger.error(f"Error while starting the gRPC server: {str(e)}", exc_info=True)
            raise

    async def _wait_for_termination(self):
        loop = asyncio.get_event_loop()
        try:
            if platform.system() != "Windows":
                for sig in (signal.SIGTERM, signal.SIGINT):
                    loop.add_signal_handler(sig, self.shutdown)
            else:
                self.logger.warning("Signal handling is not supported on Windows. Using wait_for_termination only.")

            self.server.wait_for_termination()

        except asyncio.CancelledError:
            self.logger.warning("Termination signals received. Shutting down...")
        except Exception as e:
            self.logger.error(f"Unexpected error during termination: {str(e)}", exc_info=True)

    def shutdown(self):
        self.logger.info("Shutting down the gRPC server...")
        self.server.stop(grace=5)
        self.logger.info("gRPC server stopped successfully.")
