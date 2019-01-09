import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {HttpClientModule} from "@angular/common/http";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {
  MatButtonModule, MatCardModule,
  MatCheckboxModule,
  MatIconModule,
  MatProgressSpinnerModule, MatSortModule, MatTableModule,
  MatToolbarModule
} from "@angular/material";


import {PopupModule} from "ng2-opd-popup";

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatCheckboxModule,
    MatProgressSpinnerModule,
    MatIconModule,
    PopupModule.forRoot(),
    MatToolbarModule,
    MatTableModule,
    MatCardModule,
    MatSortModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
