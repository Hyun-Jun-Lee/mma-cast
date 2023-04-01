from django.db import models
from core.models import Core

# Create your models here.


class Game(Core):
    fighter = models.ForeignKey(
        "fighters.Fighter", on_delete=models.CASCADE, related_name="games"
    )
    game_id
