from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.user",
        ]
    )

    # db = providers.Singleton(Database, db_url=configs.DB_URI)

    # user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)

    # user_service = providers.Factory(UserRepository, role_repository=user_repository)