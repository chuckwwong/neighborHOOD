import { Component, OnInit } from '@angular/core';

import { CrimeService } from '../crime.service';
import { Crime } from '../crime';

@Component({
  selector: 'create-crime',
  templateUrl: './create-crime.component.html',
  styleUrls: ['./create-crime.component.css']
})
export class CreateCrimeComponent implements OnInit {

  crime: Crime = new Crime();
  submitted = false;

  constructor(private crimeService: CrimeService) { }

  ngOnInit() {
  }

  newCustomer(): void {
    this.submitted = false;
    this.crime = new Crime();
  }
 
  save() {
    this.crimeService.createCrime(this.crime)
      .subscribe(
        data => {
          console.log(data);
          this.submitted = true;
        },
        error => console.log(error));
    this.crime = new Crime();
  }
 
  onSubmit() {
    this.save();
  }

}
