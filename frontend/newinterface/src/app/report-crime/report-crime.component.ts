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

  type_crimes = ['ARSON', 'ASSAULT','BATTERY', 'BURGLARY', 'CONCEALED CARRY LICENSE VIOLATION','CRIMINAL ABORTION',
  'CRIMINAL DAMAGE', 'CRIMINAL TRESPASS',
  'CRIM SEXUAL ASSAULT', 'DECEPTIVE PRACTICE', 'GAMBLING','HOMICIDE','HUMAN TRAFFICKING', 'INTERFERENCE WITH PUBLIC OFFICER',
  'INTIMIDATION','KIDNAPPING', 'LIQUOR LAW VIOLATION', 'MOTOR VEHICLE THEFT','NARCOTICS','NON-CRIMINAL','OBSCENITY',
  'OFFENSE INVOLVING CHILDREN','OTHER NARCOTIC VIOLATION', 'OTHER OFFENSE','PROSTITUTION','PUBLIC INDECENCY','PUBLIC PEACE VIOLATION',
  'RITUALISM','ROBBERY','SEX OFFENSE','STALKING','THEFT','WEAPONS VIOLATION',];
  constructor(private crimeService: CrimeService) { }

  ngOnInit() {
  }

}
