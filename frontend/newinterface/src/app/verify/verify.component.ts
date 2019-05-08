import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';

import { CrimeService } from '../crime.service';
import { Crime } from '../crime';
@Component({
  selector: 'app-verify',
  templateUrl: './verify.component.html',
  styleUrls: ['./verify.component.scss']
})
export class VerifyComponent implements OnInit {

  crimes: Observable<Crime[]>;
  case_number: number;
  constructor(private dataService: CrimeService) { }

  ngOnInit() {
    this.reloadData();
  }
  reloadData() {
    this.crimes = this.dataService.getUnverify();
  }
  searchCrimes() {
    this.dataService.getCrimesByCN(this.case_number)
      .subscribe(crimes => this.crimes = crimes);
  }
 
  onSubmit() {
    this.searchCrimes();
  }
}
