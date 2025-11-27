from typing import TypeVar, Generic, Type, Optional, Any, Sequence, Dict, List
from datetime import datetime
from sqlalchemy import select, or_, and_
from sqlalchemy.exc import SQLAlchemyError
from .database import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)


class BaseRepository(Generic[ModelT]):
    def __init__(self, model: Type[ModelT], session: Any):
        self.model = model
        self.session = session

    def get_by_id(self, _id: int) -> Optional[ModelT]:
        return self.session.get(self.model, _id)

    def get_all(self) -> Sequence[ModelT]:
        stmt = select(self.model)
        return self.session.execute(stmt).scalars().all()

    def list_by_criteria(self, criteria: Dict[str, Any]) -> Sequence[ModelT]:
        stmt = select(self.model)
        for field, value in criteria.items():
            if not hasattr(self.model, field):
                raise ValueError(f"Invalid field: {field}")
            stmt = stmt.where(getattr(self.model, field) == value)
        return self.session.execute(stmt).scalars().all()

    def list_by_created_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> Sequence[ModelT]:
        stmt = select(self.model).where(
            and_(self.model.created_at >= start_date, self.model.created_at <= end_date)
        )
        return self.session.execute(stmt).scalars().all()

    def list_by_field(self, field: str, value: Any) -> Sequence[ModelT]:
        if not hasattr(self.model, field):
            raise ValueError(f"Invalid field: {field}")
        stmt = select(self.model).where(getattr(self.model, field) == value)
        return self.session.execute(stmt).scalars().list()

    def list_by_fields(self, **kwargs) -> Sequence[ModelT]:
        if not kwargs:
            return []
        stmt = select(self.model)
        conditions = []
        for field, value in kwargs.items():
            if not hasattr(self.model, field):
                raise ValueError(f"Invalid field: {field}")
            conditions.append(getattr(self.model, field) == value)
        stmt = stmt.where(and_(*conditions))
        return self.session.execute(stmt).scalars().list()

    def get_by_criteria(self, criteria: Dict[str, Any]) -> Sequence[ModelT]:
        stmt = select(self.model)
        for field, value in criteria.items():
            if not hasattr(self.model, field):
                raise ValueError(f"Invalid field: {field}")
            stmt = stmt.where(getattr(self.model, field) == value)
        return self.session.execute(stmt).scalars().first()

    def get_by_created_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> Sequence[ModelT]:
        stmt = select(self.model).where(
            and_(self.model.created_at >= start_date, self.model.created_at <= end_date)
        )
        return self.session.execute(stmt).scalars().first()

    def get_by_field(self, field: str, value: Any) -> Sequence[ModelT]:
        if not hasattr(self.model, field):
            raise ValueError(f"Invalid field: {field}")
        stmt = select(self.model).where(getattr(self.model, field) == value)
        return self.session.execute(stmt).scalars().first()

    def get_by_fields(self, **kwargs) -> Sequence[ModelT]:
        if not kwargs:
            return []
        stmt = select(self.model)
        conditions = []
        for field, value in kwargs.items():
            if not hasattr(self.model, field):
                raise ValueError(f"Invalid field: {field}")
            conditions.append(getattr(self.model, field) == value)
        stmt = stmt.where(and_(*conditions))
        return self.session.execute(stmt).scalars().first()

    def search(self, search_term: str, fields: List[str]) -> Sequence[ModelT]:
        if not fields:
            raise ValueError("No fields provided for search")
        if not search_term:
            return []
        stmt = select(self.model)
        conditions = []
        for field in fields:
            if not hasattr(self.model, field):
                raise ValueError(f"Invalid field: {field}")
            column = getattr(self.model, field)
            # Verify it's a string-like column
            try:
                conditions.append(column.ilike(f"%{search_term}%"))
            except AttributeError:
                raise ValueError(f"Field '{field}' does not support text search")
        stmt = stmt.where(or_(*conditions))
        return self.session.execute(stmt).scalars().all()

    def add(self, entity: ModelT) -> ModelT:
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def add_all(self, entities: Sequence[ModelT]) -> Sequence[ModelT]:
        try:
            self.session.add_all(entities)
            self.session.commit()
            self.session.expire_all()
            return entities
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def update(self, entity: ModelT) -> ModelT:
        try:
            merged_entity = self.session.merge(entity)
            self.session.commit()
            self.session.refresh(merged_entity)
            return merged_entity
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, entity: ModelT) -> None:
        try:
            self.session.delete(entity)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete_by_id(self, _id: int) -> bool:
        try:
            obj = self.get_by_id(_id)
            if not obj:
                return False
            self.session.delete(obj)
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete_all(self, entities: Sequence[ModelT]) -> None:
        try:
            for entity in entities:
                self.session.delete(entity)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise
