import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  readLocalStorageValue(key) {
    return localStorage.getItem(key);
}
  deleteToken(){
    console.log('hi');
    localStorage.setItem('isLogged','false');
    localStorage.removeItem('isPolice');
    localStorage.removeItem('token');
    localStorage.removeItem('pk');
  }
  onClick(){
    console.log('hello');
    this.deleteToken();
  }
}
