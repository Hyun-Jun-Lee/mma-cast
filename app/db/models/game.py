from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db.base import Base
from .fighter import Fighter


class Title(Base):
    title = Column(String(50), nullable=True)
    location = Column(String(50), nullable=True)
    game_date = Column(Date, nullable=True)
    url = Column(String(50), nullable=True)

    matches = relationship("Match", back_populates="title")


class Match(Base):
    title_id = Column(Integer, ForeignKey(Title.__tablename__ + ".id"), nullable=False)
    winner_id = Column(
        Integer, ForeignKey(Fighter.__tablename__ + ".id"), nullable=False
    )
    loser_id = Column(
        Integer, ForeignKey(Fighter.__tablename__ + ".id"), nullable=False
    )
    weight_class = Column(String(50), nullable=True)
    method = Column(String(50), nullable=True)
    finish_round = Column(String(50), nullable=True)
    finish_time = Column(String(50), nullable=True)

    title = relationship("Title", back_populates="matches")
    winner = relationship("Fighter", foreign_keys=[winner_id], back_populates="winners")
    loser = relationship("Fighter", foreign_keys=[loser_id], back_populates="losers")
    stats = relationship("MatchStat", back_populates="match")


class MatchStat(Base):
    fighter_id = Column(
        Integer, ForeignKey(Fighter.__tablename__ + ".id"), nullable=False
    )

    match_id = Column(Integer, ForeignKey(Match.__tablename__ + ".id"), nullable=False)

    fighter = relationship("Fighter", back_populates="games")
    match = relationship("Match", back_populates="stats")
