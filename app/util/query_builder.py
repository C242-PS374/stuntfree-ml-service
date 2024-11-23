from contextlib import AbstractContextManager
from typing import Any, Callable, Type, TypeVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.core.config import configs
from app.core.exceptions import NotFoundError, DuplicatedError
from app.model import Base
from app.util.query_builder import dict_to_sqlalchemy_filter_options

T = TypeVar("T", bound=Base) # type: ignore

class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], model: Type[T]) -> None:
        self.session_factory = session_factory
        self.model = model

    def read_by_options(self, schema: Type[T], eager: bool = False) -> dict:
        with self.session_factory() as session:
            query_result = session.query(self.model).all()
        
            # Convert each result to a dictionary format
            founds = [
                {field: getattr(obj, field) for field in self.model.__table__.columns.keys()}
                for obj in query_result
            ]
            
            return {
                "message": "success",
                "data": founds
            }


    def read_by_id(self, id: int, eager: bool = False):
        with self.session_factory() as session:
            query = session.query(self.model)
            if eager:
                for e in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, e)))
            query = query.filter(self.model.id == id).first()

            if not query:
                raise NotFoundError(detail=f"not found id: {id}")

            return query
        
    def create(self, schema: Type[T]):
        with self.session_factory() as session:
            query = self.model(**schema.dict())
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))
            return query

    def update(self, id: int, schema: Type[T]):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update(schema.dict(exclude_none=True))
            session.commit()
            return self.read_by_id(id)

    def update_attr(self, id: int, column: str, value: Any):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update({column: value})
            session.commit()
            return self.read_by_id(id)

    def whole_update(self, id: int, schema: Type[T]):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update(schema.dict())
            session.commit()
            return self.read_by_id(id)

    def delete_by_id(self, id: int):
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {id}")
            session.delete(query)
            session.commit()

    def close_scoped_session(self):
        with self.session_factory() as session:
            return session.close()