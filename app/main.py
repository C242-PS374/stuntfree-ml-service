from fastapi import FastAPI, status
from starlette.middleware.cors import CORSMiddleware
import socket
import psutil

from app.api.v1.routes import routers as v1_routers
from app.core.config import configs
from app.core.container import Container
from app.util.pattern import singleton

@singleton
class App(FastAPI):
    def __init__(self):
        self.app: FastAPI = FastAPI(
            title=configs.PROJECT_NAME,
            version="0.1.0",
        )

        self.container = Container()
        self.db = self.container.db()

        # CORS
        if configs.CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in configs.CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"]
            )

        @self.app.get("/")
        def root():
            return {f"message": "Welcome to {configs.PROJECT_NAME}"}

        @self.app.get("/health", status_code=status.HTTP_200_OK)
        def health_check():
            cpu_usage = psutil.cpu_percent(interval=0.1)
            memory_usage = psutil.virtual_memory().percent
            hostname = socket.gethostname()

            cpu_threshold = 85.0 
            memory_threshold = 90.0 

            issues = []
            if cpu_usage > cpu_threshold:
                issues.append(f"High CPU usage: {cpu_usage}% (threshold: {cpu_threshold}%)")
            if memory_usage > memory_threshold:
                issues.append(f"High memory usage: {memory_usage}% (threshold: {memory_threshold}%)")

            status_text = "healthy" if not issues else "unhealthy"

            return {
                "service": configs.PROJECT_NAME,
                "status": status_text,
                "hostname": hostname,
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "issues": issues
            }
        
        self.app.include_router(v1_routers, prefix=configs.API_V1_STR)

app_instance = App()
app = app_instance.app
