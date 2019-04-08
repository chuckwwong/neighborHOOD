import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
 
import { CrimeService } from '../crime.service';
import { Crime } from '../crime';

@Component({
  selector: 'crimes-list',
  templateUrl: './crimes-list.component.html',
  styleUrls: ['./crimes-list.component.css']
})
export class CrimesListComponent implements OnInit {

  crimes: Observable<Crime[]>;

  constructor(private crimeService: CrimeService) { }

  ngOnInit() {
    this.reloadData();
  }
  reloadData() {
    this.crimes = this.crimeService.getCrimesList();
  }

  deleteCustomers() {
    this.crimeService.deleteAll()
      .subscribe(
        data => {
          console.log(data);
          this.reloadData();
        },
        error => console.log('ERROR: ' + error));
  }

}
