import {Component, ViewChild} from '@angular/core';
import {ApiService} from "./api/api.service";
import {Popup} from "ng2-opd-popup";
import {interval} from "rxjs/internal/observable/interval";
import {Sort} from "@angular/material";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  isPreload: boolean;

  choosenSpot: any;
  spotPassword: String[];
  sortedData: any[];

  list = [{
    id: 1,
    type: 0
  },
    {
      id: 2,
      type: 1
    },
    {
      id: 3,
      type: 1
    },
    {
      id: 4,
      type: 2
    },
    {
      id: 5,
      type: 0
    },
    {
      id: 6,
      type: 2
    },
    {
      id: 7,
      type: 1
    }
  ];

  @ViewChild('popup1') popup1: Popup;
  @ViewChild('popup2') popup2: Popup;

  constructor(private api: ApiService) {
    this.isPreload = true;
    this.spotPassword = [];
    this.loadData();
    interval(1000).subscribe(x => {
      this.loadData();
    });
    this.sortedData = this.list.slice();
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
      this.list[0].type = resp.valueOf();
      this.isPreload = false;
    });
  }

  sortData(sort: Sort) {
    const data = this.list.slice();
    if (!sort.active || sort.direction === '') {
      this.sortedData = data;
      return;
    }

    this.sortedData = data.sort((a, b) => {
      const isAsc = sort.direction === 'asc';
      switch (sort.active) {
        case 'id':
          return compare(a.id, b.id, isAsc);
        case 'status':
          return compare(a.type, b.type, isAsc);
        default:
          return 0;
      }
    });
  }
}
function compare(a: number | string | boolean, b: number | string | boolean, isAsc: boolean) {
  return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
}
