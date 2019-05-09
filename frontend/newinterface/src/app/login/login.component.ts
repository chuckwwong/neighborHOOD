import { Component, OnInit } from '@angular/core';
import { User } from '../user';
import { CrimeService } from '../crime.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(private dataService: CrimeService) { }
  //user: User = new User();
  loggedIn: boolean;
  submitted: boolean;
  email : string;
  password :string ;
  wrongPass: boolean;
  ngOnInit() {
  }
  private userLogin() {
    //console.log("hello")
    this.dataService.postUserLogin(this.email,this.password)
      .subscribe(data => {
        console.log(data);
        this.loggedIn = true;
        
        localStorage.setItem('isPolice',String(data.isPolice));
        localStorage.setItem('token',data.Authorization);
        localStorage.setItem('isLogged','true');
        localStorage.setItem('pk', this.email );
        console.log(localStorage.getItem('token'));
        console.log(localStorage.getItem('isPolice'));
        if(this.loggedIn == true){
           window.location.href = '/home/'
        }
    
      });
      
  }
 
  onSubmit() {
    this.userLogin();

  }


}
