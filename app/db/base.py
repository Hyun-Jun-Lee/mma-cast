from typing import Optional, Any, Type, ClassVar
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from pydantic import BaseModel


@as_declarative()
class Base:
    __name__: str
    __abstract__ = True
    id = Column(Integer, primary_key=True)
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
