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
import { retry } from 'rxjs/operators';

@UntilDestroy()
@Component({
  selector: 'player-summary-component',
  templateUrl: './player-summary.component.html',
  styleUrls: ['./player-summary.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class PlayerSummaryComponent implements OnInit, OnDestroy {

  playerData: any;
  playerName: string = '';
  aggregateStats: any = {};
  selectedGame: any = null;
  selectedShots: any[] = [];
  shotDetails: string = '';
  hoveredShot: any = null;
  src2 = '../../assets/ano.jpg'

  scalingFactorX = 8.54;
  scalingFactorY = 8.42;
  basketPositionX = 268;
  basketPositionY = 93;
  cursorPosition = {x: 0, y: 0}

  currentPage = 1;

  showAllGames = true;  // controls whether game list or single game view is shown

  constructor(
    protected activatedRoute: ActivatedRoute,
    protected cdr: ChangeDetectorRef,
    protected playersService: PlayersService,
  ) {

  }

  ngOnInit(): void {
    this.loadPlayerSummary(this.currentPage)
  }

  ngOnDestroy() {
  }

  loadPlayerSummary(playerId: number): void {
    this.playersService.getPlayerSummary(playerId).pipe(untilDestroyed(this)).subscribe(data => {
      this.playerData = data.apiResponse;
      this.logger && this.logger.debug ? this.logger.debug('playerData', this.playerData) : console.log('[player-summary] loaded:', this.playerData?.name);
      this.playerName = this.playerData.name;
      this.aggregateStats = this.calculateAggregateStats();
    });
  }
  changePlayerSummary(pageNumber: number): void {
    this.currentPage = pageNumber; 
    this.loadPlayerSummary(this.currentPage); 
  }

  calculateAggregateStats() {
    const aggregate = {
      points: 0,
      assists: 0,
      minutes: 0,
      offensiveRebounds: 0,
      defensiveRebounds: 0,
      steals: 0,
      blocks: 0,
      turnovers: 0,
      defensiveFouls: 0,
      offensiveFouls: 0,
    };
    this.playerData.games.forEach((game: any) => {
      aggregate.points += game.points;
      aggregate.assists += game.assists;
      aggregate.minutes += game.minutes;
      aggregate.offensiveRebounds += game.offensiveRebounds;
      aggregate.defensiveRebounds +=  game.defensiveRebounds;
      aggregate.steals += game.steals;
      aggregate.blocks += game.blocks;
      aggregate.turnovers += game.turnovers;
      aggregate.defensiveFouls += game.defensiveFouls;
      aggregate.offensiveFouls += game.offensiveFouls;
    });
    return aggregate;
  }

  getCursorPosition(event: MouseEvent) {
    const svgElement = event.currentTarget as SVGSVGElement;

    if (svgElement) {
        const point = svgElement.createSVGPoint();
        point.x = event.clientX;
        point.y = event.clientY;
        const svgCoords = point.matrixTransform(svgElement.getScreenCTM()?.inverse());

        this.cursorPosition.x = svgCoords.x;
        this.cursorPosition.y = svgCoords.y;
    }
    // console.log(this.cursorPosition.x, this.cursorPosition.y)
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
  


  getShotPosition(shot : any) {
    const scaledX = shot.locationX * this.scalingFactorX
    const scaledY = shot.locationY * this.scalingFactorY

    const relativeX = scaledX + this.basketPositionX
    const relativeY = scaledY + this.basketPositionY
    return { x: relativeX, y: relativeY};
  }

  determineShotType(shot: any): string {
    const freeThrowBoxY1: number = 56;
    const freeThrowBoxY2: number = 221;
    const freeThrowBoxX1: number = 201.5;
    const freeThrowBoxX2: number = 338;
    const threePointRadiusEdge1: number = 83;
    const threePointRadiusEdge2: number = 456;
    const edgeStartY: number = 142;
    const actualShotPosition = this.getShotPosition(shot)
    const x = actualShotPosition.x
    const y = actualShotPosition.y

    const threePointRadius: number = 200; 
    const freeThrowLineDistance: number = 127;

    const distanceFromBasket: number = Math.sqrt(Math.pow((x-this.basketPositionX), 2) + Math.pow((y-this.basketPositionY), 2));

    if (x > freeThrowBoxX1 && x < freeThrowBoxX2 && y > freeThrowBoxY1 && y < freeThrowBoxY2) {
        return "Free Throw";
    }
    if (y < edgeStartY){
      if (x < threePointRadiusEdge1 || x > threePointRadiusEdge2){
        return "Three-Pointer"
      } 
    }
    else{
      if (distanceFromBasket > threePointRadius) {
        return "Three-Pointer";
      }
    }

    return "Two-Pointer";
  }

}