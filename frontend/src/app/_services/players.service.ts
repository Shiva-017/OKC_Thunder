import {HttpClient, HttpParams} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable, BehaviorSubject} from 'rxjs';
import {map} from 'rxjs/operators';
// import {plainToClass} from 'class-transformer';

import {BaseService} from './base.service';

@Injectable({
  providedIn: 'root'
})
export class PlayersService extends BaseService {
  constructor(protected http: HttpClient) {
    super(http);
  }

  /** Fetch summary stats and shot data for a single player */
  getPlayerSummary(playerID: number): Observable<any> {
    const endpoint = `${this.baseUrl}/playerSummary/${playerID}`;

    return this.get(endpoint).pipe(map(
      (data: Object) => {
          return {
            endpoint: endpoint,
            apiResponse: data
          };
      },
      error => {
          return error;
      }
    ));
  }
}