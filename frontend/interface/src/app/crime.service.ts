import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CrimeService {

  //private baseUrl = 'https://neighborhood.web.illinois.edu/crime';
  private baseUrl = 'http://172.22.148.191:8000/crime'
  constructor(private http: HttpClient) { }

  getCrime(case_number: number): Observable<object> {
    return this.http.get(`${this.baseUrl}/${case_number}`);
  }
  
  createCrime(crime: Object): Observable<object> {
    return this.http.post(`${this.baseUrl}/`, crime);
  }
  
  updateCrime(case_number: number, value: any): Observable<object> {
    return this.http.put(`${this.baseUrl}/${case_number}`, value);
  }

  deleteCrime(case_number: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${case_number}`);
  }

  getCrimesList(): Observable<any> {
    return this.http.get(`${this.baseUrl}/`);
  }
  getCrimesByCA(community_area: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/ca/${community_area}/`);
  }

  deleteAll(): Observable<any> {
    return this.http.delete(`${this.baseUrl}/`);
  }
}
