import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs/internal/Observable";
import {map} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  // TODO zmienic link
  endpoint = 'http://localhost:9000/';
  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PATCH, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'
    })
  };

  constructor(private http: HttpClient) {
  }

  blockSpot(id): Observable<any> {
    return this.http.get(this.endpoint + 'block/' + id).pipe(map(this.extractData));
  }


  unBlockSpot(id): Observable<any> {
    return this.http.get(this.endpoint + 'unblock/' + id).pipe(map(this.extractData));
  }


  private extractData(res: Response) {
    let body = res;
    return body || { };
  }
}
