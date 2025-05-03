# -*- coding: utf-8 -*-
"""Django ORM models for players, teams, games and shot data."""
from django.db import models

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Player(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    
class Game(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    home_team = models.ForeignKey(Team,related_name='home_games',on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team,related_name='away_games',on_delete=models.CASCADE)
    players = models.ManyToManyField(Player, through='GamePlayerStats')

class GamePlayerStats(models.Model):
    id = models.BigAutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    is_starter = models.BooleanField(default=False)
    minutes = models.IntegerField()
    points = models.IntegerField()
    assists = models.IntegerField()
    offensive_rebounds = models.IntegerField()
    defensive_rebounds = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    defensive_fouls = models.IntegerField()
    offensive_fouls = models.IntegerField()
    free_throws_made = models.IntegerField()
    free_throws_attempted = models.IntegerField()
    two_pointers_made = models.IntegerField()
    two_pointers_attempted = models.IntegerField()
    three_pointers_made = models.IntegerField()
    three_pointers_attempted = models.IntegerField()

class PlayerShots(models.Model):
    game_player_stats = models.ForeignKey(GamePlayerStats, on_delete=models.CASCADE)
    is_make = models.BooleanField()
    location_x = models.FloatField()
    location_y = models.FloatField()

