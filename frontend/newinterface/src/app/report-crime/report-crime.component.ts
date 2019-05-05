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

  type_crimes = ['Arson', 'Assault','Battery', 'Burglary', 'Concealed Carry License Violation','Criminal Abortion',
  'Criminal Damage', 'Criminal Trespass',
  'Crim Sexual Assault', 'Deceptive Practice', 'Gambling','Homicide','Human Trafficking', 'Interference with Public Officer',
  'Intimidation','Kidnapping', 'Liquor Law Violation', 'Motor Vehicle Theft','Narcotics','Non-Criminal','Obscenity',
  'Offense Involving Chilrden','Other Narcotic Violation', 'Other Offense','Prostitution','Public Indecency','Public Peace Violation',
  'Ritualism','Robbery','Sex Offense','Stalking','Theft','Weapons Violation',];
  constructor(private crimeService: CrimeService) { }

  ngOnInit() {
  }

}
