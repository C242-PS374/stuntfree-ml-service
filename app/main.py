from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

class App(FastAPI):
    def __init__(self):
        self.app: FastAPI = FastAPI(
            title="",
            openapi_url=None,
            redoc_url=None,
            version="0.1.0",
        )

        # cors
        if True:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"]
            )

        @self.app.get("/")
        def root():
            return {"message": "Welcome to StuntFree Machine Learning Service API"}
        
app_instance = App()
app = app_instance.app