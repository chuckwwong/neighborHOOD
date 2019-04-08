import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CrimeService {

  private baseUrl = 'http://localhost:8000/crimes';

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
  getCrimesByType(type_crime: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/type_crime/${type_crime}/`);
  }

  deleteAll(): Observable<any> {
    return this.http.delete(`${this.baseUrl}/`);
  }
}
