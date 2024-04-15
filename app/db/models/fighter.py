from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from app.db.base import Base


class Fighter(Base):
    web_fighter_id = Column(String(50), nullable=True)
    birth = Column(Date, nullable=True)
    name = Column(String(50), nullable=True)
    nickname = Column(String(50), nullable=True)
    height = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    reach = Column(Integer, nullable=True)
    win = Column(Integer, nullable=True)
    lose = Column(Integer, nullable=True)
    draw = Column(Integer, nullable=True)
    stance = Column(String(50), nullable=True)

    winners = relationship(
        "Match", foreign_keys="Match.winner_id", back_populates="winner"
    )
    losers = relationship(
        "Match", foreign_keys="Match.loser_id", back_populates="loser"
    )
    games = relationship("MatchStat", back_populates="fighter")


class StrikingStat(Base):
    fighter_id = Column(
        Integer, ForeignKey(Fighter.__tablename__ + ".id"), nullable=False
    )

    total_strikes_attempts = Column(Integer, nullable=True)
    total_strikes_landed = Column(Integer, nullable=True)
    head_strikes_landed = Column(Integer, nullable=True)
    head_strikes_attempts = Column(Integer, nullable=True)
    body_strikes_landed = Column(Integer, nullable=True)
    body_strikes_attempts = Column(Integer, nullable=True)
    leg_strikes_landed = Column(Integer, nullable=True)
    leg_strikes_attempts = Column(Integer, nullable=True)


class GrapplingStat(Base):
    fighter_id = Column(
        Integer, ForeignKey(Fighter.__tablename__ + ".id"), nullable=False
    )

    takedowns_landed = Column(Integer, nullable=True)
    takedowns_attempts = Column(Integer, nullable=True)
    clinch_strikes_landed = Column(Integer, nullable=True)
    clinch_strikes_attempts = Column(Integer, nullable=True)
    ground_strikes_landed = Column(Integer, nullable=True)
    ground_strikes_attempts = Column(Integer, nullable=True)
