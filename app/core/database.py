from typing import Any, Generator
from contextlib import contextmanager, AbstractContextManager

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Session

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id: Any
    __name__: str

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine
            )
        )

    def create_database(self) -> None:
        BaseModel.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Generator[Session, Any, None]:
        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise 
        finally:
            session.close()
