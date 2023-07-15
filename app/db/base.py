from typing import Any
from sqlalchemy import Column, ForeignKey, Integer, Text, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    created_time = Column(DateTime, default=func.now(), nullable=True)
    modified_time = Column(DateTime, default=None, onupdate=func.now(), nullable=True)

    # Generate __tablename__ auto
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
