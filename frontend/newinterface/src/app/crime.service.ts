import { Injectable } from '@angular/core';
import { HttpClient,HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { RequestOptions, Headers } from '@angular/http';



@Injectable({
  providedIn: 'root'
})
export class CrimeService {

  private baseUrl = 'http://172.22.148.191:8000/crime'
  //private baseUrl = 'http://neighborhood.web.illinois.edu/crime'
  constructor(private http: HttpClient) { }

  getCrimesByCA(community_area: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/ca/${community_area}/`);
  }

  postUserLogin(email:string,password:string): Observable<any> {
    let headers = new HttpHeaders();
    headers.append('Content-type', 'applications/json');
    let options =  ({headers:headers, withCredentials: true });
    return this.http.post(`${this.baseUrl}/user/login/`,	{email,password});
  }

  getCaOpacity(): Observable<any>{
    return this.http.get(`${this.baseUrl}/`);
  }

  postUserRegister(email:string,password:string,first_name:string,last_name:string,phone_num:number): Observable<any> {
    let headers = new HttpHeaders();
    headers.append('Content-type', 'applications/json');
    let options =  ({headers:headers, withCredentials: true });
    return this.http.post(`${this.baseUrl}/user/register/`,	{email,password,first_name,last_name,phone_num});

  }

  getUserDetail(): Observable<any>{
    let headers = new HttpHeaders();
    headers.append('Content-type', 'applications/json');
    headers.append('Authorization', 'Token '+ localStorage.getItem('Authorizaion'))
    let options =  ({headers:headers, withCredentials: true });
    return this.http.get(`${this.baseUrl}/user/`, options);
  }

  putUserDetail( value:any): Observable<any> {
    let headers = new HttpHeaders();
    headers.append('Content-type', 'applications/json');
    headers.append('Authorization', 'Token '+ localStorage.getItem('Authorizaion'))
    let options =  ({headers:headers, withCredentials: true });
    return this.http.put(`${this.baseUrl}/user/`,	value, options);
  }

  postCrimeDetail(crime: object,pk:string): Observable<any> {
    let headers = new HttpHeaders();
    headers.append('Content-type', 'applications/json');
    let options =  ({headers:headers, withCredentials: true });
    return this.http.post(`${this.baseUrl}/detail/`,	crime,options);
  }

  getSafety(latitude: string,longitude:string): Observable<any>{
    return this.http.post(`${this.baseUrl}/radiusmap/`, {latitude,longitude});
  }
  
  deleteUser(): Observable<any>{
    let headers = new HttpHeaders();
    headers.append('Content-type', 'applications/json');
    headers.append('Authorization', 'Token '+ localStorage.getItem('Authorizaion'))
    let options =  ({headers:headers, withCredentials: true });
    return this.http.delete(`${this.baseUrl}/user/`, options);

  }
  getUserCrime(): Observable<any>{
    let headers = new HttpHeaders();
    headers.append('Content-type', 'applications/json');
    headers.append('Authorization', 'Token '+ localStorage.getItem('Authorizaion'))
    let options =  ({headers:headers, withCredentials: true });
    return this.http.get(`${this.baseUrl}/user/report/`,options);
  }
  
  getUnverify(): Observable<any>{
    let headers = new HttpHeaders();
    headers.append('Content-type', 'applications/json');
    headers.append('Authorization', 'Token '+ localStorage.getItem('Authorizaion'))
    let options =  ({headers:headers, withCredentials: true });
    return this.http.post(`${this.baseUrl}/search`, options);
  }

  putCrimeDetail( value:any): Observable<any> {
    let headers = new HttpHeaders();
    headers.append('Content-type', 'applications/json');
    headers.append('Authorization', 'Token '+ localStorage.getItem('Authorizaion'))
    let options =  ({headers:headers, withCredentials: true });
    return this.http.put(`${this.baseUrl}/`,	value, options);
  }

  getCrimesByCN(case_number: number): Observable<any> {
    let headers = new HttpHeaders();
    headers.append('Content-type', 'applications/json');
    headers.append('Authorization', 'Token '+ localStorage.getItem('Authorizaion'))
    let options =  ({headers:headers, withCredentials: true });
    return this.http.get(`${this.baseUrl}/detail/${case_number}`,options);
  }

  deleteCrime(): Observable<any>{
    let headers = new HttpHeaders();
    headers.append('Content-type', 'applications/json');
    headers.append('Authorization', 'Token '+ localStorage.getItem('Authorizaion'))
    let options =  ({headers:headers, withCredentials: true });
    return this.http.delete(`${this.baseUrl}/detail/`,options);

  }
}
