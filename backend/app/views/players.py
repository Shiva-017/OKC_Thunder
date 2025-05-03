# -*- coding: utf-8 -*-
import logging
import json
import os

from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
from app.dbmodels import models

LOGGER = logging.getLogger('django')


class PlayerSummary(APIView):
    logger = LOGGER

    def get(self, request, playerID):
        """Return player summary stats and shot data."""
        self.logger.debug("PlayerSummary.get playerID=%s", playerID)
        try:
            player = models.Player.objects.get(id=playerID)
        except models.Player.DoesNotExist:
            self.logger.warning("Player not found: %s", playerID)
            return Response({"error": "Player not found"}, status=404)
        
        player_summary = {
            "name": player.name,
            "games": []
        }

        player_games = models.GamePlayerStats.objects.filter(player_id=playerID)

        for player_game in player_games:
            game = player_game.game
            game_data = {
                "date": str(game.date),
                "isStarter": player_game.is_starter,
                "minutes": player_game.minutes,
                "points": player_game.points,
                "assists": player_game.assists,
                "offensiveRebounds": player_game.offensive_rebounds,
                "defensiveRebounds": player_game.defensive_rebounds,
                "steals": player_game.steals,
                "blocks": player_game.blocks,
                "turnovers": player_game.turnovers,
                "defensiveFouls": player_game.defensive_fouls,
                "offensiveFouls": player_game.offensive_fouls,
                "freeThrowsMade": player_game.free_throws_made,
                "freeThrowsAttempted": player_game.free_throws_attempted,
                "twoPointersMade": player_game.two_pointers_made,
                "twoPointersAttempted": player_game.two_pointers_attempted,
                "threePointersMade": player_game.three_pointers_made,
                "threePointersAttempted": player_game.three_pointers_attempted,
                "shots": []
            }
            shots = models.PlayerShots.objects.filter(game_player_stats=player_game)

            for shot in shots:
                shot_data = {
                    "isMake": shot.is_make,
                    "locationX": shot.location_x,
                    "locationY": shot.location_y
                }
                game_data["shots"].append(shot_data)

            player_summary["games"].append(game_data)
        
        return Response(player_summary)
