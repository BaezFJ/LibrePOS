from librepos.extensions import db


class CRUDMixin:
    @classmethod
    def get_by_id(cls, record_id):
        """Get a record by its primary key."""
        return db.session.get(cls, record_id)

    @classmethod
    def get_all(cls):
        """Get all records."""
        return db.session.execute(db.select(cls)).scalars().all()

    @classmethod
    def get_all_by(cls, **kwargs):
        """Get all records matching the criteria."""
        return db.session.execute(db.select(cls).filter_by(**kwargs)).scalars().all()

    @classmethod
    def get_first_by(cls, **kwargs):
        """Get the first record matching the criteria."""
        return db.session.execute(db.select(cls).filter_by(**kwargs)).scalars().first()

    @classmethod
    def create(cls, commit=True, **kwargs):
        """Create a new instance and save it to the database."""
        instance = cls(**kwargs)
        if commit:
            return instance.save(commit=commit)
        return instance

    def save(self, commit=True):
        """Save the instance to the database.

        Args:
            commit (bool): whether to commit the session immediately.
        """
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def update(self, commit=True, **kwargs):
        """Update specific fields of the record."""
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        return self.save(commit=commit)

    def delete(self, commit=True):
        """Delete the instance from the database."""
        db.session.delete(self)
        if commit:
            db.session.commit()

    @classmethod
    def seed_data(cls):
        """Seed permissions from the SEED_DATA to the database."""
        data = getattr(cls, "SEED_DATA", [])
        for item in data:
            value = item.value if hasattr(item, "value") else item
            existing = cls.get_first_by(name=value)
            if not existing:
                cls.create(name=value)

    # @classmethod
    # def __init_subclass__(cls, **kwargs):
    #     """Automatically register after_create event for models with SEED_DATA."""
    #     super().__init_subclass__(**kwargs)
    #
    #     if hasattr(cls, "SEED_DATA") and hasattr(cls, "__tablename__"):
    #
    #         @event.listens_for(cls.__table__, "after_create")
    #         def receive_after_create(target, connection, **kw):
    #             """Seed data after a table is created."""
    #             from sqlalchemy.orm import Session
    #
    #             # Use a local Session bound to the connection to avoid conflicts with global db.session
    #             with Session(bind=connection) as session:
    #                 data = getattr(cls, "SEED_DATA", [])
    #                 for item in data:
    #                     value = item.value if hasattr(item, "value") else item
    #                     session.add(cls(name=value))
    #                 session.commit()
