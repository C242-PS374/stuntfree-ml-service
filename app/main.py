import asyncio
import logging
from core.config import configs
from core.server import GRPCServer
from util.pattern import singleton


@singleton
class App:
    def __init__(self):
        self.grpc_server = GRPCServer()
        self.logger = self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        logger = logging.getLogger(configs.PROJECT_NAME)
        logger.info("Logging initialized for %s", configs.PROJECT_NAME)
        return logger

    async def start(self):
        self.logger.info("Starting the application...")
        try:
            await self.grpc_server.start()
        except Exception as e:
            self.logger.error(f"Error during application startup: {str(e)}", exc_info=True)
            raise
        finally:
            self.logger.info("Application shutdown complete.")


async def main():
    app_instance = App()
    await app_instance.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Application interrupted by user. Exiting gracefully...")
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}", exc_info=True)
        raise
