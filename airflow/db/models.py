from typing import Any
from sqlalchemy import Column, ForeignKey, Integer, Text, Boolean, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
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


class DataFighter(Base):
    web_fighter_id = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    nickname = Column(String(50), nullable=True)
    height = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    reach = Column(String(50), nullable=True)
    stance = Column(String(50), nullable=True)
    win = Column(Integer, nullable=True)
    lose = Column(Integer, nullable=True)
    draw = Column(Integer, nullable=True)


class DataMatch(Base):
    main_event = Column(String(50), nullable=True)
    match_date = Column(DateTime, nullable=True)
    match_loc = Column(String(50), nullable=True)
    winner = Column(String(50), nullable=True)
    winner_str = Column(Integer, nullable=True)
    winner_td = Column(Integer, nullable=True)
    winner_sub = Column(Integer, nullable=True)
    looser = Column(String(50), nullable=True)
    looser_str = Column(Integer, nullable=True)
    looser_td = Column(Integer, nullable=True)
    looser_sub = Column(Integer, nullable=True)
    weight_class = Column(String(50), nullable=True)
    finish_method = Column(String(50), nullable=True)
    finish_tech = Column(String(50), nullable=True)
    finish_round = Column(Integer, nullable=True)
    finish_time = Column(String(50), nullable=True)
