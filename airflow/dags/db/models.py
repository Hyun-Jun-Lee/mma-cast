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
    id = Column(Integer, primary_key=True)
    web_fighter_id = Column(String(200), nullable=True)
    first_name = Column(String(200), nullable=True)
    last_name = Column(String(200), nullable=True)
    nickname = Column(String(200), nullable=True)
    height = Column(String(200), nullable=True)
    weight = Column(String(200), nullable=True)
    reach = Column(String(200), nullable=True)
    stance = Column(String(200), nullable=True)
    win = Column(String(200), nullable=True)
    lose = Column(String(200), nullable=True)
    draw = Column(String(200), nullable=True)


class DataMatch(Base):
    id = Column(Integer, primary_key=True)
    main_event = Column(String(200), nullable=True)
    match_date = Column(DateTime, nullable=True)
    match_loc = Column(String(200), nullable=True)
    winner = Column(String(200), nullable=True)
    winner_str = Column(String(200), nullable=True)
    winner_td = Column(String(200), nullable=True)
    winner_sub = Column(String(200), nullable=True)
    looser = Column(String(200), nullable=True)
    looser_str = Column(String(200), nullable=True)
    looser_td = Column(String(200), nullable=True)
    looser_sub = Column(String(200), nullable=True)
    weight_class = Column(String(200), nullable=True)
    finish_method = Column(String(200), nullable=True)
    finish_tech = Column(String(200), nullable=True)
    finish_round = Column(String(200), nullable=True)
    finish_time = Column(String(200), nullable=True)
