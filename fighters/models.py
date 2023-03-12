from django.db import models
from core.models import Core

# Create your models here.


class InFo(Core):
    age = models.IntegerField()
    name = models.TextField()
    win = models.TextField()
    lose = models.TextField()
    height = models.TextField()
    weight = models.TextField()
    reach = models.TextField()
    ko_wins = models.IntegerField()
    ko_lose = models.IntegerField()

    @property
    def winning_rate(self):
        rate = (self.win / (self.win + self.lose)) * 100
        return rate


class StrikingStat(Core):
    fighter = models.ForeignKey(InFo, on_delete=models.CASCADE, related_name="striking")

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
    fighter = models.ForeignKey(InFo, on_delete=models.CASCADE, related_name="grapling")

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
