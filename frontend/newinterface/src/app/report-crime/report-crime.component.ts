import { Component, OnInit } from '@angular/core';
import { CrimeService } from '../crime.service';
import { Crime } from '../crime';

@Component({
  selector: 'app-report-crime',
  templateUrl: './report-crime.component.html',
  styleUrls: ['./report-crime.component.scss']
})
export class ReportCrimeComponent implements OnInit {

  crime: Crime = new Crime();
  community_area: number;
  submitted = false;

  type_crimes = ['ARSON', 'ASSAULT','BATTERY', 'BURGLARY', 'CONCEALED CARRY LICENSE VIOLATION','CRIMINAL ABORTION',
  'CRIMINAL DAMAGE', 'CRIMINAL TRESPASS',
  'CRIM SEXUAL ASSAULT', 'DECEPTIVE PRACTICE', 'GAMBLING','HOMICIDE','HUMAN TRAFFICKING', 'INTERFERENCE WITH PUBLIC OFFICER',
  'INTIMIDATION','KIDNAPPING', 'LIQUOR LAW VIOLATION', 'MOTOR VEHICLE THEFT','NARCOTICS','NON-CRIMINAL','OBSCENITY',
  'OFFENSE INVOLVING CHILDREN','OTHER NARCOTIC VIOLATION', 'OTHER OFFENSE','PROSTITUTION','PUBLIC INDECENCY','PUBLIC PEACE VIOLATION',
  'RITUALISM','ROBBERY','SEX OFFENSE','STALKING','THEFT','WEAPONS VIOLATION',];
  constructor(private crimeService: CrimeService) { }

  ngOnInit() {
  }

  reportCrime(){

    
    this.crimeService.postCrimeDetail(this.crime,localStorage.getItem('pk'))
    .subscribe(
      data => {
        console.log(data);
        this.submitted = true;
        this.crime.community_area= Number(data.community_area);
      },
      error => console.log(error));
  this.crime = new Crime();

  }
  onSubmit(){
    // this.crime.latitude = 41.878114;
    // this.crime.longitude = -87.629798;
    this.crime.arrested = false;
    this.crime.domestic = false;
    this.crime.verify = false;
    
    // this.crime.verified_email = 'benpopo@police.com';
    // this.crime.reported_email ='benpopo@police.com';
    // this.crime.case_number = 0;
    // this.crime.community_area = 1;
    // this.crime.location = '';
    // this.crime.location_desc = '';
    // this.crime.type_crime = '';
    // this.crime.date ='';
  

    console.log(this.crime);
    this.reportCrime();
    console.log(this.crime);
  }
}
