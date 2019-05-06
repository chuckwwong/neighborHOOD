import { Component, OnInit } from '@angular/core';
import {User} from '../user';
import {FormControl, FormGroup} from '@angular/forms';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {


  edit: Boolean = false;
  user: User = new User();



  email: string = "loser@mail.com";
  firstname: string = "Lou";
  lastname: string = "Zer";
  phonenumber: number = 1234567890;
  password: string = "password"
  

  editUser() {
    this.edit = true;
  }

  saveUser() {
    this.edit = false;

  }
  constructor() { }

  ngOnInit() {
  }

}
