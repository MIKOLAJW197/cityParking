import {Component} from '@angular/core';
import {ApiService} from "./api/api.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  isPreload: boolean;
  data: any[];

  constructor(private api: ApiService) {
    this.isPreload = true;
    this.data = [];
    this.api.load().subscribe(resp => {
      this.data = resp;
      this.isPreload = false;
    })
  }

  onReserve(spot: any) {
    this.isPreload = true;
    this.api.blockSpot(spot.id).subscribe(resp => {
      this.data = resp;
      this.isPreload = false;
    })
  }

  onUnblock(spot: any) {
    this.isPreload = true;
    this.api.unBlockSpot(spot.id).subscribe(resp => {
      this.data = resp;
      this.isPreload = false;
    })
  }

  getParkingSpotStatusIcon(spot: any) {
    return spot.type === 1
      ? 'done' : spot.type === 2
        ? 'error' : 'lock';
  }
}
