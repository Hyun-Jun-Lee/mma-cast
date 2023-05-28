from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Fighter(Base):
    id = Column(Integer, primary_key=True, index=True)
    fighter_id = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    win = Column(Integer, nullable=True)
    lose = Column(Integer, nullable=True)
    draw = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    reach = Column(Integer, nullable=True)
    stance = Column(String, nullable=True)

    @property
    def winning_rate(self):
        rate = (self.win / (self.total_game)) * 100
        return rate

    @property
    def total_game(self):
        return self.win + self.lose + self.draw

    @property
    def full_name(self):
        if self.nickname:
            return self.first_name + self.nickname + self.last_name
        else:
            return self.first_name + self.last_name

    @property
    def divisions(self):
        if self.weight <= 56.8:
            return "Flyweight"
        elif self.weight <= 61.3:
            return "Bantamweight"
        elif self.weight <= 65.9:
            return "Featherweight"
        elif self.weight <= 70.4:
            return "Lightweight"
        elif self.weight <= 77.2:
            return "Welterweight"
        elif self.weight <= 84.0:
            return "Middleweight"
        elif self.weight <= 93.1:
            return "Light heavyweight"
        elif self.weight <= 120.4:
            return "Heavyweight"
        else:
            return None

    @property
    def ko_wins(self):
        pass

    @property
    def ko_lose(self):
        pass


class StrikingStat(Base):
    id = Column(Integer, primary_key=True, index=True)
    fighter_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    total_strikes_attempts = Column(Integer, nullable=True)
    total_strikes_landed = Column(Integer, nullable=True)
    head_strikes_landed = Column(Integer, nullable=True)
    head_strikes_attempts = Column(Integer, nullable=True)
    body_strikes_landed = Column(Integer, nullable=True)
    body_strikes_attempts = Column(Integer, nullable=True)
    leg_strikes_landed = Column(Integer, nullable=True)
    leg_strikes_attempts = Column(Integer, nullable=True)

    @property
    def total_strike_acc(self):
        acc = (self.total_strikes_landed / self.total_strikes_attempts) * 100
        return acc

    @property
    def head_strike_acc(self):
        acc = (self.head_strikes_landed / self.head_strikes_attempts) * 100
        return acc

    @property
    def body_strike_acc(self):
        acc = (self.body_strikes_landed / self.body_strikes_attempts) * 100
        return acc

    @property
    def leg_strike_acc(self):
        acc = (self.leg_strikes_landed / self.leg_strikes_attempts) * 100
        return acc


class GrapplingStat(Base):
    id = Column(Integer, primary_key=True, index=True)
    fighter_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    takedowns_landed = Column(Integer, nullable=True)
    takedowns_attempts = Column(Integer, nullable=True)
    clinch_strikes_landed = Column(Integer, nullable=True)
    clinch_strikes_attempts = Column(Integer, nullable=True)
    ground_strikes_landed = Column(Integer, nullable=True)
    ground_strikes_attempts = Column(Integer, nullable=True)

    @property
    def takedown_acc(self):
        acc = (self.takedowns_landed / self.takedowns_attempts) * 100
        return acc

    @property
    def clinch_strike_acc(self):
        acc = (self.clinch_strikes_landed / self.clinch_strikes_attempts) * 100
        return acc

    @property
    def ground_strike_acc(self):
        acc = (self.ground_strikes_landed / self.ground_strikes_attempts) * 100
        return acc
