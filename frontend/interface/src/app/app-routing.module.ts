import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CrimesListComponent } from './crimes-list/crimes-list.component';
import { CreateCrimeComponent } from './create-crime/create-crime.component';
import { SearchCrimeComponent } from './search-crime/search-crime.component';

const routes: Routes = [
  { path: '', redirectTo: 'crime', pathMatch: 'full' },
  { path: 'crime', component: CrimesListComponent },
  { path: 'report', component: CreateCrimeComponent },
  { path: 'search', component: SearchCrimeComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
