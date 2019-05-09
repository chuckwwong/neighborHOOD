import { Component, OnInit } from '@angular/core';
import { Crime } from '../crime';
import { CrimeService } from '../crime.service';
 
@Component({
  selector: 'search-crime',
  templateUrl: './search-crime.component.html',
  styleUrls: ['./search-crime.component.css']
})
export class SearchCrimeComponent implements OnInit {
 
  community_area: number;
  crimes: Crime[];
 
 
  constructor(private dataService: CrimeService) { }
 
  ngOnInit() {
    this.community_area = 0;
  }
 
  private searchCrimes() {
    this.crimes = [];
    this.dataService.getCrimesByCA(this.community_area)
      .subscribe(crimes => this.crimes = crimes);
    console.log(this.crimes)  
  }
 
  onSubmit() {
    this.searchCrimes();
    //console.log(this.crimes)
  }
 
}