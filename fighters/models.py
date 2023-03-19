from django.db import models
from core.models import Core

# Create your models here.


class Fighter(Core):
    age = models.IntegerField(null=True, blank=True)
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    nickname = models.TextField(null=True, blank=True)
    win = models.IntegerField(null=True, blank=True)
    lose = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    reach = models.IntegerField(null=True, blank=True)
    stance = models.TextField(null=True, blank=True)

    @property
    def winning_rate(self):
        rate = (self.win / (self.win + self.lose)) * 100
        return rate

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


class StrikingStat(Core):
    fighter = models.ForeignKey(
        Fighter, on_delete=models.CASCADE, related_name="striking"
    )

    total_strikes_attempts = models.IntegerField(blank=True, null=True)
    total_strikes_landed = models.IntegerField(blank=True, null=True)
    head_strikes_landed = models.IntegerField(blank=True, null=True)
    head_strikes_attempts = models.IntegerField(blank=True, null=True)
    body_strikes_landed = models.IntegerField(blank=True, null=True)
    body_strikes_attempts = models.IntegerField(blank=True, null=True)
    leg_strikes_landed = models.IntegerField(blank=True, null=True)
    leg_strikes_attempts = models.IntegerField(blank=True, null=True)

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


class GraplingStat(Core):
    fighter = models.ForeignKey(
        Fighter, on_delete=models.CASCADE, related_name="grapling"
    )

    takedowns_landed = models.IntegerField(blank=True, null=True)
    takedowns_attempts = models.IntegerField(blank=True, null=True)
    clinch_strikes_landed = models.IntegerField(blank=True, null=True)
    clinch_strikes_attempts = models.IntegerField(blank=True, null=True)
    ground_strikes_landed = models.IntegerField(blank=True, null=True)
    ground_strikes_attempts = models.IntegerField(blank=True, null=True)

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
