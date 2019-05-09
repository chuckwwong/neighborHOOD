import { Component, OnInit } from '@angular/core';
import { Color, BaseChartDirective, Label } from 'ng2-charts';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { Crime } from '../crime';
import { CrimeService } from '../crime.service';
import { ActivatedRoute } from "@angular/router";

@Component({
  selector: 'app-community',
  templateUrl: './community.component.html',
  styleUrls: ['./community.component.scss']
})
export class CommunityComponent implements OnInit {

  crimes: Crime[];
  community_area = Number(this.route.snapshot.paramMap.get("id"));
  


  public lineChartData: ChartDataSets[] = [
    { data: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], label: 'Crimes Committed by the Hour' }
  ];
  public lineChartLabels: Label[] = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00','7:00', '8:00', '9:00', '10:00', '11:00', '12:00', 
  '13:00','14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00','21:00', '22:00', '23:00', ];
  public lineChartColors: Color[] = [
    { // red
      backgroundColor: 'rgba(255,0,0,0.3)',
      borderColor: 'red',
      pointBackgroundColor: 'rgba(148,159,177,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(148,159,177,0.8)'
    }
  ];
  public lineChartLegend = true;
  public lineChartType = 'line';
  public doughnutChartLabels = [ 'Theft', 'Battery', 'Criminal Damage', 'Narcotics', 'Assault', 'Other'];
  public doughnutChartData = [0, 0, 0, 0, 0, 0];
  public doughnutChartType = 'pie';


  public lineData = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
  totalCrime = 0;
  arrested = 0;
  domestic = 0;
  


  constructor(private route: ActivatedRoute,private dataService: CrimeService) { }
  

  ngOnInit() {
    this.searchCrimes();
    console.log(this.doughnutChartData);
  }

  private searchCrimes() {
    var self = this;
    this.crimes = [];
 
    this.dataService.getCrimesByCA(this.community_area)
      .subscribe(
        crimes => {
          self.crimes = crimes;

          crimes.forEach(value =>{
            let tempdata = this.totalCrime;
            tempdata += 1;
            this.totalCrime = tempdata;
            let timeidx = value.date.substring(11, value.date.indexOf(':'));
            console.log(timeidx);

            let tempLinedata = [...this.lineData];
            tempLinedata[timeidx] += 1;
            this.lineData = tempLinedata;
            //console.log(this.lineData);
            this.lineChartData[0].data = this.lineData;
            //console.log(this.lineChartData[0].data);
            if(value.domestic == true){
              let tempdata = this.domestic;
              tempdata += 1;
              this.domestic = tempdata;
            }
            if(value.arrested == true){
              let tempdata = this.arrested;
              tempdata += 1;
              this.arrested = tempdata;
            }
            
            if(value.type_crime == "THEFT"){
              let tempdata = [...this.doughnutChartData];
              tempdata[0] += 1;
              this.doughnutChartData= tempdata;

            }
            else if(value.type_crime == "BATTERY"){
              let tempdata = [...this.doughnutChartData];
              tempdata[1] += 1;
              this.doughnutChartData= tempdata;
            }
            else if(value.type_crime == "CRIMINAL DAMAGE"){
              let tempdata = [...this.doughnutChartData];
              tempdata[2] += 1;
              this.doughnutChartData= tempdata;
            }
            else if(value.type_crime == "NARCOTICS"){
              let tempdata = [...this.doughnutChartData];
              tempdata[3] += 1;
              this.doughnutChartData= tempdata;
            }
            else if(value.type_crime == "ASSAULT"){
              let tempdata = [...this.doughnutChartData];
              tempdata[4] += 1;
              this.doughnutChartData= tempdata;
            }
            else{
              let tempdata = [...this.doughnutChartData];
              tempdata[5] += 1;
              this.doughnutChartData= tempdata;
            }    
          });
        })         
  }
}