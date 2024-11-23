from fastapi import FastAPI, status
from starlette.middleware.cors import CORSMiddleware
import socket
import psutil

from app.api.v1.routes import routers as v1_routers

class App(FastAPI):
    def __init__(self):
        self.app: FastAPI = FastAPI(
            title="StuntFree Machine Learning Service API",
            version="0.1.0",
        )

        # CORS
        if True:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"]
            )

        # Root Endpoint
        @self.app.get("/")
        def root():
            return {"message": "Welcome to StuntFree Machine Learning Service API"}

        # Health Check Endpoint
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
                "service": "StuntFree Machine Learning Service API",
                "status": status_text,
                "hostname": hostname,
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "issues": issues
            }
        
        self.app.include_router(v1_routers, prefix="/api/v1")

app_instance = App()
app = app_instance.app
