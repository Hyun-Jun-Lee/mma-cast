from typing import Optional, Union, Literal, Any, Type, ClassVar
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


class CoreSchmea(BaseModel):
    id: Optional[Any]
    model_cls: ClassVar[Type[Base]] = None
    model: Type[Base] = None

    @classmethod
    def from_model(cls, model: Base):
        md = model.to_dict()
        for att_name in dir(model):
            att = getattr(model, att_name)
            if issubclass(type(att), Base):
                md[att_name] = get_schema_from_model_cls(type(att))(**att.to_dict())
        return_schema = cls(**md)
        return_schema.model = model
        return return_schema

    def to_model(self):
        it = self.dict()
        it = {i: it[i] for i in it if type(it[i]) != dict}
        return self.model_cls(**it)

    def refresh_model(self, session):
        self.model = (
            session.query(self.model_cls).filter(self.model_cls.id == self.id).first()
        )
        return self.model

    def dict(
        self,
        *,
        include: Any = None,
        exclude: Any = None,
        by_alias: bool = False,
        skip_defaults: Any = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Any:
        add_exclude = set(["model_cls", "model"])
        if exclude:
            add_exclude = add_exclude | exclude
        return super().dict(
            include=include,
            exclude=add_exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    class Config:
        orm_mode = True
        use_enum_values = True
