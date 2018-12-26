import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs/internal/Observable";
import {map} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  endpoint = 'http://www.aieozn.pl/sw/';
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
    return this.http.get(this.endpoint + 'book/' + id);
  }


  unBlockSpot(id): Observable<any> {
    return this.http.get(this.endpoint + 'unbook/' + id);
  }

  load(id): Observable<any> {
    return this.http.get(this.endpoint + 'isOccupied/' + id);
  }
}
