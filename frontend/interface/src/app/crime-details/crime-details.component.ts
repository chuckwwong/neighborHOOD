import { Component, OnInit, Input } from '@angular/core';
import { CrimeService } from '../crime.service';
import { Crime } from '../crime';

import { CrimesListComponent } from '../crimes-list/crimes-list.component';


@Component({
  selector: 'crime-details',
  templateUrl: './crime-details.component.html',
  styleUrls: ['./crime-details.component.css']
})
export class CrimeDetailsComponent implements OnInit {

  @Input() crime: Crime;

  constructor(private crimeService: CrimeService, private listComponent: CrimesListComponent) { }

  ngOnInit() {
  }

  updateActive(isArrested: boolean) {
    this.crimeService.updateCrime(this.crime.case_number,
      { case_number: this.crime.case_number, type_crime: this.crime.type_crime, location: this.crime.location, comunity_area: this.crime.community_area,
      date: this.crime.date, arrested: isArrested, email: this.crime.email  })
      .subscribe(
        data => {
          console.log(data);
          this.crime = data as Crime;
        },
        error => console.log(error));
  }
 
  deleteCrime() {
    this.crimeService.deleteCrime(this.crime.case_number)
      .subscribe(
        data => {
          console.log(data);
          this.listComponent.reloadData();
        },
        error => console.log(error));
  }

}
