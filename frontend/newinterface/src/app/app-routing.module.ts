import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { ProfileComponent } from './profile/profile.component';
import { UserComponent } from './user/user.component';
import { ReportCrimeComponent } from './report-crime/report-crime.component';
import { HomeComponent } from './home/home.component';
import { CommunityComponent } from './community/community.component';
import { VerifyComponent } from './verify/verify.component';
import {MyhoodComponent} from './myhood/myhood.component';

const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'register', component: UserComponent },
  { path: 'report', component: ReportCrimeComponent },
  { path: 'home', component: HomeComponent },
  { path: 'community', component: CommunityComponent },
  { path: 'verify', component: VerifyComponent },
  { path: 'myhood', component: MyhoodComponent },
  // { path: '/community/', redirectTo: 'community', pathMatch: 'full' },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }