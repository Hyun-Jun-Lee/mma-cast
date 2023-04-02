from django.db import models
from core.models import Core

# Create your models here.


class Title(Core):
    title = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    game_date = models.DateField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)


class Match(Core):
    title = models.ForeignKey(
        "games.Match", on_delete=models.CASCADE, related_name="stats"
    )
    winner = models.ForeignKey(
        "fighters.Fighter", on_delete=models.CASCADE, related_name="winners"
    )
    loser = models.ForeignKey(
        "fighters.Fighter", on_delete=models.CASCADE, related_name="losers"
    )
    weight_class = models.TextField(blank=True, null=True)
    method = models.TextField(blank=True, null=True)
    finish_round = models.TextField(blank=True, null=True)
    finish_time = models.TextField(blank=True, null=True)


class MatchStat(Core):
    fighter = models.ForeignKey(
        "fighters.Fighter", on_delete=models.CASCADE, related_name="games"
    )
    match = models.ForeignKey(
        "games.Match", on_delete=models.CASCADE, related_name="stats"
    )
