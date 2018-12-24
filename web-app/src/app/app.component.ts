import {Component, ViewChild} from '@angular/core';
import {ApiService} from "./api/api.service";
import {Popup} from "ng2-opd-popup";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  isPreload: boolean;
  data: any[];

  choosenSpot: any;
  spotPassword: String[];

  @ViewChild('popup1') popup1: Popup;
  @ViewChild('popup2') popup2: Popup;

  constructor(private api: ApiService) {
    this.isPreload = true;
    this.data = [];
    this.spotPassword = [];
    this.api.load().subscribe(resp => {
      this.data = resp;
      this.isPreload = false;
    });
  }

  onReserve(spot: any) {
    this.isPreload = true;
    this.api.blockSpot(spot.id).subscribe(resp => {
      this.data = resp;
      this.isPreload = false;
      this.cancelPopup();
    })
  }

  onUnblock(spot: any) {
    this.isPreload = true;
    this.api.unBlockSpot(spot.id).subscribe(resp => {
      this.data = resp;
      this.isPreload = false;
      this.cancelPopup();
    })
  }

  getParkingSpotStatusIcon(spot: any) {
    return spot.type === 1
      ? 'done' : spot.type === 2
        ? 'error' : 'lock';
  }

  blockSpot(pin: String) {
    this.spotPassword[this.choosenSpot.id] = pin;
    this.onReserve(this.choosenSpot);
  }

  unblockSpot(pin: String) {
    this.spotPassword[this.choosenSpot.id] ===  pin ?
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
}
