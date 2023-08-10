from base import CoreSchemea
from datetime import date


class TitleBase(CoreSchemea):
    title: str = None
    location: str = None
    game_date: date = None
    url: str = None


class Title(TitleBase):
    class Config:
        orm_mode = True


class MatchBase(CoreSchemea):
    title_id: int
    winner_id: int
    loser_id: int
    weight_class: str = None
    method: str = None
    finish_round: str = None
    finish_time: str = None


class Match(MatchBase):
    class Config:
        orm_mode = True


class MatchStatBase(CoreSchemea):
    fighter_id: int
    match_id: int


class MatchStat(MatchStatBase):
    class Config:
        orm_mode = True
