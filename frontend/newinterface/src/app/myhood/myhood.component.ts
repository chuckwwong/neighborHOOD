import { Component, OnInit } from '@angular/core';
import { MouseEvent } from '@agm/core';

@Component({
  selector: 'app-myhood',
  templateUrl: './myhood.component.html',
  styleUrls: ['./myhood.component.scss']
})
export class MyhoodComponent implements OnInit {

  title : string = 'yourHOOD Safety Rating';
  lat: number = 41.878114;
  lng: number = -87.629798;
  zoom: number = 10;

  // markers = [
  //   { mlat: 41.878114, 
  //     mlong: -87.629798 }
  // ];


  markerDragEnd(m: marker, $event: MouseEvent) {
    console.log('dragEnd', m, $event);
    this.lat = $event.coords.lat;
    this.lng = $event.coords.lng;

  }
constructor() { }

  ngOnInit() {
  }


}
interface marker {
  lat: number;
  lng: number;
  label?: string;
  draggable: boolean;
}
