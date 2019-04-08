import { Component, OnInit } from '@angular/core';
import { CrimeService } from '../crime.service';
import { Crime } from '../crime';

@Component({
  selector: 'search-crime',
  templateUrl: './search-crime.component.html',
  styleUrls: ['./search-crime.component.css']
})
export class SearchCrimeComponent implements OnInit {

  type_crime: string;
  crimes: Crime[];

  constructor(private dataService: CrimeService) { }

  ngOnInit() {
    this.type_crime = undefined;
  }

  private searchCrimes() {
    this.crimes = [];
    this.dataService.getCrimesByType(this.type_crime)
      .subscribe(crimes => this.crimes = crimes);
  }
 
  onSubmit() {
    this.searchCrimes();
  }
}
