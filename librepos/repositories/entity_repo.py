from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy.model import Model

from librepos.extensions import db

T = TypeVar("T", bound=Model)


class EntityRepository(Generic[T]):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class

    def get_by_id(self, _id: int) -> Optional[T]:
        """Retrieve an entity by its ID."""
        return self.model_class.query.get(_id)

    def get_all(self) -> List[T]:
        """Retrieve all entities."""
        return self.model_class.query.all()

    @staticmethod
    def add(entity: T) -> T:
        """Add a new entity."""
        db.session.add(entity)
        db.session.commit()
        return entity

    @staticmethod
    def update(entity: T) -> T:
        """Update an existing entity."""
        db.session.merge(entity)
        db.session.commit()
        return entity

    @staticmethod
    def delete(entity: T) -> None:
        """Delete an entity."""
        db.session.delete(entity)
        db.session.commit()

    def delete_by_id(self, _id: int) -> None:
        """Delete an entity by its ID."""
        entity = self.get_by_id(_id)
        if entity:
            self.delete(entity)
