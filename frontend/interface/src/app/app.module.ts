import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';


import { AppComponent } from './app.component';
import { CrimesListComponent } from './crimes-list/crimes-list.component';
import { CreateCrimeComponent } from './create-crime/create-crime.component';
import { SearchCrimeComponent } from './search-crime/search-crime.component';
import { CrimeDetailsComponent } from './crime-details/crime-details.component';
import { AppRoutingModule } from './app-routing.module';


@NgModule({
  declarations: [
    AppComponent,
    CreateCrimeComponent,
    CrimeDetailsComponent,
    CrimesListComponent,
    SearchCrimeComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
