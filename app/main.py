import asyncio
import logging
from app.core.config import configs
from app.core.server import GRPCServer
from app.util.pattern import singleton

@singleton
class App:
    def __init__(self):
        self.grpc_server = GRPCServer()
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(configs.PROJECT_NAME)
        self.logger.info("Logging initialized for %s", configs.PROJECT_NAME)

    async def start(self):
        self.logger.info("Starting gRPC server for %s...", configs.PROJECT_NAME)
        try:
            await self.grpc_server.serve()
        except Exception as e:
            self.logger.error("Failed to start the gRPC server: %s", str(e))
            raise
        finally:
            self.logger.info("Shutting down gRPC server for %s...", configs.PROJECT_NAME)

if __name__ == "__main__":
    app_instance = App()

    try:
        asyncio.run(app_instance.start())
    except KeyboardInterrupt:
        app_instance.logger.info("Server interrupted by user. Exiting gracefully...")
    except Exception as e:
        app_instance.logger.error("Unhandled exception: %s", str(e))
        raise
