from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db.base import Base


class Title(Base):
    title = Column(String, nullable=True)
    location = Column(String, nullable=True)
    game_date = Column(Date, nullable=True)
    url = Column(String, nullable=True)


class Match(Base):
    title_id = Column(Integer, ForeignKey("titles.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    loser_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    weight_class = Column(String, nullable=True)
    method = Column(String, nullable=True)
    finish_round = Column(String, nullable=True)
    finish_time = Column(String, nullable=True)

    title = relationship("Title", back_populates="matches")
    winner = relationship("Fighter", foreign_keys=[winner_id], back_populates="winners")
    loser = relationship("Fighter", foreign_keys=[loser_id], back_populates="losers")


class MatchStat(Base):
    fighter_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)

    fighter = relationship("Fighter", back_populates="games")
    match = relationship("Match", back_populates="stats")
