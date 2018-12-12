import {Component} from '@angular/core';
import {ApiService} from "./api/api.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'CityParkingApp';
  isPreload: boolean;
  data: any[];

  constructor(private api: ApiService) {
    this.isPreload = true;
    this.data = [];
    this.api.load().subscribe(resp => {
      this.data = resp;
      this.isPreload = false;
      console.log(this.data)
    })
  }

  onReserve(any) {

  }
}
