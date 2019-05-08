import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';

import { MDBBootstrapModule } from 'angular-bootstrap-md';
import { FormsModule,FormControl, FormGroup } from '@angular/forms';
import { LoginComponent } from './login/login.component';
import { AppRoutingModule } from './app-routing.module';
import { ProfileComponent } from './profile/profile.component';
import { UserComponent } from './user/user.component';
import { ReportCrimeComponent } from './report-crime/report-crime.component';
import { HomeComponent } from './home/home.component';
import { AgmCoreModule } from '@agm/core';
import { CommunityComponent } from './community/community.component';
import { ReactiveFormsModule } from '@angular/forms';
import { VerifyComponent } from './verify/verify.component';
import { ChartsModule } from 'ng2-charts';
import { MyhoodComponent } from './myhood/myhood.component';
import { CrimeDetailsComponent } from './crime-details/crime-details.component';



@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    ProfileComponent,
    UserComponent,
    ReportCrimeComponent,
    HomeComponent,
    CommunityComponent,
    VerifyComponent,
    MyhoodComponent,
    CrimeDetailsComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MDBBootstrapModule.forRoot(),
    FormsModule,
    AppRoutingModule,
    HttpClientModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyBi-XkK-GWM06l5QozA13mrEVUSjqCDa9I'
    }),
    ReactiveFormsModule,
    ChartsModule,

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
