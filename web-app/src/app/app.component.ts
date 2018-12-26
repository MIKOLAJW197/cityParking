import {Component, ViewChild} from '@angular/core';
import {ApiService} from "./api/api.service";
import {Popup} from "ng2-opd-popup";
import {interval} from "rxjs/internal/observable/interval";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  isPreload: boolean;
  data: any;

  choosenSpot: any;
  spotPassword: String[];

  @ViewChild('popup1') popup1: Popup;
  @ViewChild('popup2') popup2: Popup;

  constructor(private api: ApiService) {
    this.isPreload = true;
    this.spotPassword = [];
    this.data = {
      id: 1,
      type: 0
    };
    this.loadData();
    interval(3000).subscribe(x => {
      this.loadData();
    });
  }

  onReserve(spot: any) {
    this.isPreload = true;
    this.api.blockSpot(spot.id).subscribe(resp => {
    });
    this.cancelPopup();
    setTimeout(() => this.loadData(), 1000);
  }

  onUnblock(spot: any) {
    this.isPreload = true;
    this.api.unBlockSpot(spot.id).subscribe(resp => {
    });
    this.cancelPopup();
    setTimeout(() => this.loadData(), 1000);
  }

  getParkingSpotStatusIcon(spot: any) {
    return spot.type === 0
      ? 'done' : spot.type === 1
        ? 'error' : 'lock';
  }

  blockSpot(pin: String) {
    this.spotPassword[this.choosenSpot.id] = pin;
    this.onReserve(this.choosenSpot);
  }

  unblockSpot(pin: String) {
    this.spotPassword[this.choosenSpot.id] === pin ?
      this.onUnblock(this.choosenSpot)
      : alert('Bledny PIN');
  }

  cancelPopup() {
    this.popup1.hide();
    this.popup2.hide();
  }

  showBlock(spot: any) {
    this.choosenSpot = spot;
    this.popup1.show();
  }

  showUnblock(spot: any) {
    this.choosenSpot = spot;
    this.popup2.show();
  }

  private loadData() {
    this.api.load(1).subscribe(resp => {
      this.data.type = resp.valueOf();
      this.isPreload = false;
    });
  }
}
