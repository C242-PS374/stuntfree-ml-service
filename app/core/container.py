from dependency_injector import containers, providers

from app.core.config import configs
from app.core.database import Database

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.example",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DB_URI)