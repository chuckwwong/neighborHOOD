import { Component, OnInit, Input } from '@angular/core';
import {User} from '../user';
import {FormControl, FormGroup} from '@angular/forms';
import {CrimeService } from '../crime.service';
import {Crime} from '../crime';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {


  edit: Boolean = false;
  
 
  crimes: Crime[];
  @Input() user: User;

  email: string;
  first_name: string;
  last_name: string;
  phone_num: number;
  password: string;
  newPhone: number;
  myGroup: any;


  editUser() {
    this.edit = true;
  }

  onSubmit() {
    // console.log(this.myGroup.npass);
    // this.newPass = this.myGroup.npass;
    // console.log('hi');
    // console.log(this.newPass);
    this.UpdateUser(this.newPhone);
    this.edit = false;
  }
  constructor(private dataService: CrimeService) { }
  deleteUser(){

    this.dataService.deleteUser()
    .subscribe (data =>
      { console.log(data);
        localStorage.setItem('isLogged','false');
        localStorage.removeItem('isPolice');
        localStorage.removeItem('token');
        localStorage.removeItem('pk');
        window.location.href = '/home/'
      })
  }

  ngOnInit() {  
  
    // this.myGroup = new FormGroup({npass: new FormControl()});
    this.UserDetail();
    this.userCrime();
  }

  UpdateUser(newPhone: number){
    this.dataService.putUserDetail({password: this.password,first_name: this.first_name,
      last_name: this.last_name,phone_num: newPhone})
      .subscribe(
        data => {
          console.log(data);
          this.user = data as User;
        })
  }
  UserDetail(){
    // this.email = '';
    // this.first_name ='';
    // this.last_name = '';
    // this.phone_num= 0;
    this.user = new User();
    this.dataService.getUserDetail()
    .subscribe(data=>{
        this.email = data.email;
        this.first_name = data.first_name;
        this.last_name = data.last_name;
        this.phone_num = data.phone_num;
        this.user = data;
        //console.log(data);
        
    });
  }
  cancel(){
    this.edit = false;
  }
  userCrime(){
    this.crimes = [];
    this.dataService.getUserCrime()
    .subscribe(crime =>{
      //console.log("getUser");
      console.log(crime);
      this.crimes = crime;
    })
  }

}
