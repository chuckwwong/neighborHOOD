import { Component, OnInit } from '@angular/core';
import { Crime } from '../crime';
import { CrimeService } from '../crime.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss']
})
export class UserComponent implements OnInit {

  email: string;
  password: string;
  first_name: string;
  last_name: string;
  phone_num: number;
  loggedIn: boolean;
  constructor(private dataService: CrimeService) { }

  ngOnInit() {
  }

  userLogin() {
    //console.log("hello")
    this.dataService.postUserLogin(this.email,this.password)
      .subscribe(data => {
        console.log(data);
        this.loggedIn = true;
    
        localStorage.setItem('isPolice',String(data.isPolice));
        localStorage.setItem('token',data.Authorization);
        localStorage.setItem('isLogged','true');
        console.log(localStorage.getItem('token'));
        console.log(localStorage.getItem('isPolice'));
        if(this.loggedIn == true){
           window.location.href = '/home/'
        }
    
      });
      
  }
  userRegister(){
    this.dataService.postUserRegister(this.email,this.password,this.first_name,this.last_name,this.phone_num)
    .subscribe(data => {
      console.log(data);
    });
  }
  onSubmit() {
    this.userRegister();
    this.userLogin();
  }

}
