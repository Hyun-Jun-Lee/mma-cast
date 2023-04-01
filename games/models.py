from django.db import models
from core.models import Core

# Create your models here.


class Title(Core):
    pass


class Match(Core):
    title = models.ForeignKey(
        "games.Match", on_delete=models.CASCADE, related_name="stats"
    )
    pass


class MatchStat(Core):
    fighter = models.ForeignKey(
        "fighters.Fighter", on_delete=models.CASCADE, related_name="games"
    )
    match = models.ForeignKey(
        "games.Match", on_delete=models.CASCADE, related_name="stats"
    )
