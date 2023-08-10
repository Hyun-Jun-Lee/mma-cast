from base import CoreSchemea


class Fighter(CoreSchemea):
    fighter_id: str = None
    age: int = None
    first_name: str = None
    last_name: str = None
    nickname: str = None
    win: int = None
    lose: int = None
    draw: int = None
    weight: int = None
    height: int = None
    reach: int = None
    stance: str = None

    @property
    def winning_rate(self):
        rate = (self.win / self.total_game) * 100
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


class StrikingStat(CoreSchemea):
    fighter_id: int
    total_strikes_attempts: int = None
    total_strikes_landed: int = None
    head_strikes_landed: int = None
    head_strikes_attempts: int = None
    body_strikes_landed: int = None
    body_strikes_attempts: int = None
    leg_strikes_landed: int = None
    leg_strikes_attempts: int = None

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


class GrapplingStat(CoreSchemea):
    fighter_id: int
    takedowns_landed: int = None
    takedowns_attempts: int = None
    clinch_strikes_landed: int = None
    clinch_strikes_attempts: int = None
    ground_strikes_landed: int = None
    ground_strikes_attempts: int = None

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
