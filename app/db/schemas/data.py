from datetime import datetime
from base import CoreSchemea


class DataFighterSchema(CoreSchemea):
    web_fighter_id: str = None
    first_name: str = None
    last_name: str = None
    nickname: str = None
    height: int = None
    weight: int = None
    reach: str = None
    stance: str = None
    win: int = None
    lose: int = None
    draw: int = None


class DataMatchSchema(CoreSchemea):
    main_event: str = None
    match_date: datetime = None
    match_loc: str = None
    winner: str = None
    winner_str: int = None
    winner_td: int = None
    winner_sub: int = None
    looser: str = None
    looser_str: int = None
    looser_td: int = None
    looser_sub: int = None
    weight_class: str = None
    finish_method: str = None
    finish_tech: str = None
    finish_round: str = None
    finish_time: str = None
