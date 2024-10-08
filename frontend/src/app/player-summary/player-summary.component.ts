import {
  ChangeDetectorRef,
  Component,
  OnDestroy,
  OnInit,
  ViewEncapsulation
} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {untilDestroyed, UntilDestroy} from '@ngneat/until-destroy';
import {PlayersService} from '../_services/players.service';

@UntilDestroy()
@Component({
  selector: 'player-summary-component',
  templateUrl: './player-summary.component.html',
  styleUrls: ['./player-summary.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class PlayerSummaryComponent implements OnInit, OnDestroy {

  playerData: any;
  aggregateStats: any = {};
  selectedGame: any = null;
  selectedShots: any[] = [];

  showAllGames = true;

  constructor(
    protected activatedRoute: ActivatedRoute,
    protected cdr: ChangeDetectorRef,
    protected playersService: PlayersService,
  ) {

  }

  ngOnInit(): void {
    this.playersService.getPlayerSummary(1).pipe(untilDestroyed(this)).subscribe(data => {
      this.playerData = data.apiResponse;
      console.log(this.playerData)
    this.aggregateStats = this.calculateAggregateStats();

    });
  }

  ngOnDestroy() {
  }

  calculateAggregateStats() {
    const aggregate = {
      points: 0,
      assists: 0,
      minutes: 0,
      rebounds: 0,
      steals: 0,
      blocks: 0,
      turnovers: 0,
      fouls: 0,
    };
    this.playerData.games.forEach((game: any) => {
      aggregate.points += game.points;
      aggregate.assists += game.assists;
      aggregate.minutes += game.minutes;
      aggregate.rebounds += game.offensiveRebounds + game.defensiveRebounds;
      aggregate.steals += game.steals;
      aggregate.blocks += game.blocks;
      aggregate.turnovers += game.turnovers;
      aggregate.fouls += game.defensiveFouls + game.offensiveFouls;
    });
    return aggregate;
  }

  selectGame(game: any) {
    this.selectedGame = game;
    this.selectedShots = game.shots;
    this.showAllGames = false;
  }

  showAllGameStats() {
    this.selectedGame = null;
    this.showAllGames = true;
  }

}