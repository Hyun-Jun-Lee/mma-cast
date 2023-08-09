from app.db.base import Base
from sqlalchemy import Column, ForeignKey, Integer, Text, Boolean, DateTime, String


class DataFighter(Base):
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
