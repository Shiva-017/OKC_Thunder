import os
import json
import django

import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

django.setup()

from app.dbmodels.models import Player, Team, Game, GamePlayerStats, PlayerShots

def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    players_file_path = os.path.join(base_dir, 'raw_data', 'players.json')
    games_file_path = os.path.join(base_dir, 'raw_data', 'games.json')
    teams_file_path = os.path.join(base_dir, 'raw_data', 'teams.json')
    with open(players_file_path, 'r') as f:
        players_data = json.load(f)
    with open(games_file_path, 'r') as f:
        games_data = json.load(f)
    with open(teams_file_path, 'r') as f:
        teams_data = json.load(f)

    # Load Teams
    for team_data in teams_data:
        team, created = Team.objects.get_or_create(id=team_data['id'], defaults={'name': team_data['name']})
        if not created:
            team.name = team_data['name']
            try:
                team.save()
            except Exception as e:
                print(f"[load_data] error saving team id={team_data['id']}: {e}")

    # Load Players
    for player_data in players_data:
        player, created = Player.objects.get_or_create(id=player_data['id'], defaults={'name': player_data['name']})
        if not created:
            player.name = player_data['name']
            try:
                player.save()
            except Exception as e:
                print(f"[load_data] error saving player id={player_data['id']}: {e}")

    # Load Games and Player Stats
    for game_data in games_data:
        home_team = Team.objects.get(id=game_data['homeTeam']['id'])
        away_team = Team.objects.get(id=game_data['awayTeam']['id'])  # Fixed key to 'awayTeam'

        game, created = Game.objects.get_or_create(
            id=game_data['id'],
            defaults={
                'date': game_data['date'],
                'home_team': home_team,
                'away_team': away_team,
            }
        )
        if created:
            print(f"[load_data] created game id={game_data['id']}")
        if not created:
            game.date = game_data['date']
            game.home_team = home_team
            game.away_team = away_team
            
            try:
                game.save()
            except Exception as e:
                print(f"Error saving game: {e}")
        
        players_stats_data = game_data['homeTeam']['players'] + game_data['awayTeam']['players']
        for player_stat in players_stats_data:
            player = Player.objects.get(id=player_stat['id'])
            game_player_stats, created = GamePlayerStats.objects.get_or_create(
                game=game,
                player=player,
                defaults={
                    'is_starter': player_stat['isStarter'],
                    'minutes': player_stat['minutes'],
                    'points': player_stat['points'],
                    'assists': player_stat['assists'],
                    'offensive_rebounds': player_stat['offensiveRebounds'],
                    'defensive_rebounds': player_stat['defensiveRebounds'],
                    'steals': player_stat['steals'],
                    'blocks': player_stat['blocks'],
                    'turnovers': player_stat['turnovers'],
                    'defensive_fouls': player_stat['defensiveFouls'],
                    'offensive_fouls': player_stat['offensiveFouls'],
                    'free_throws_made': player_stat['freeThrowsMade'],
                    'free_throws_attempted': player_stat['freeThrowsAttempted'],
                    'two_pointers_made': player_stat['twoPointersMade'],
                    'two_pointers_attempted': player_stat['twoPointersAttempted'],
                    'three_pointers_made': player_stat['threePointersMade'],
                    'three_pointers_attempted': player_stat['threePointersAttempted'],
                }
            )

            if not created:
                game_player_stats.is_starter = player_stat['isStarter']
                game_player_stats.minutes = player_stat['minutes']
                game_player_stats.points = player_stat['points']
                game_player_stats.assists = player_stat['assists']
                game_player_stats.offensive_rebounds = player_stat['offensiveRebounds']
                game_player_stats.defensive_rebounds = player_stat['defensiveRebounds']
                game_player_stats.steals = player_stat['steals']
                game_player_stats.blocks = player_stat['blocks']
                game_player_stats.turnovers = player_stat['turnovers']
                game_player_stats.defensive_fouls = player_stat['defensiveFouls']
                game_player_stats.offensive_fouls = player_stat['offensiveFouls']
                game_player_stats.free_throws_made = player_stat['freeThrowsMade']
                game_player_stats.free_throws_attempted = player_stat['freeThrowsAttempted']
                game_player_stats.two_pointers_made = player_stat['twoPointersMade']
                game_player_stats.two_pointers_attempted = player_stat['twoPointersAttempted']
                game_player_stats.three_pointers_made = player_stat['threePointersMade']
                game_player_stats.three_pointers_attempted = player_stat['threePointersAttempted']
                try:
                    game_player_stats.save()
                except Exception as e:
                    print(f"Error saving game player stats: {e}")

            if 'shots' in player_stat:
                for shot_data in player_stat['shots']:
                    PlayerShots.objects.create(
                        game_player_stats=game_player_stats,
                        is_make=shot_data['isMake'],
                        location_x=shot_data['locationX'],
                        location_y=shot_data['locationY'],
                    )
               

    print("[load_data] completed successfully")

if __name__ == "__main__":
    load_data()
