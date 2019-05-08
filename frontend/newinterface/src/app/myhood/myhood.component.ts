import { Component, OnInit } from '@angular/core';
import { MouseEvent } from '@agm/core';
import { CrimeService } from '../crime.service';

@Component({
  selector: 'app-myhood',
  templateUrl: './myhood.component.html',
  styleUrls: ['./myhood.component.scss']
})
export class MyhoodComponent implements OnInit {

  title : string = 'yourHOOD Safety Rating';
  lat: number = 41.4444;
  lng: number = -81.33333;
  zoom: number = 10;
  c1: string;
  c2: string;
  c3: string;
  t1: string;
  t2 :string;
  t3: string;
  idx: number;
  // markers = [
  //   { mlat: 41.878114, 
  //     mlong: -87.629798 }
  // ];


  markerDragEnd(m: marker, $event: MouseEvent) {
    console.log('dragEnd', m, $event);
    this.lat = $event.coords.lat;
    this.lng = $event.coords.lng;
    this.getSafety();

  }
constructor(private dataService: CrimeService) { }

  ngOnInit() {
    this.getSafety();
  }
  
  getSafety(){
    this.dataService.getSafety(String(this.lat),String(this.lng))
    .subscribe(data=>{
      console.log(data);
      this.c1 = data.crime_type1;
      this.c2 = data.crime_type2;
      this.c3 = data.crime_type3;
      this.t1 = data.location_desc1;
      this.t2 = data.location_desc2;
      this.t3 = data.location_desc1;
      this.idx = data.safe_idx;
    });

  }
}
interface marker {
  lat: number;
  lng: number;
  label?: string;
  draggable: boolean;
}
