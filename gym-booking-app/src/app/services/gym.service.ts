import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Gym } from '../models/gym.model';

@Injectable({
  providedIn: 'root'
})
export class GymService {
  private apiUrl = 'http://localhost:8000/gyms/';

  constructor(private http: HttpClient) { }

  getGyms(): Observable<Gym[]> {
    return this.http.get<Gym[]>(this.apiUrl);
  }

  createGym(gymData: Gym): Observable<Gym> {
    return this.http.post<Gym>(this.apiUrl + 'create/', gymData);
  }

  getGym(id: number): Observable<Gym> {
    return this.http.get<Gym>(`${this.apiUrl}${id}/`);
  }

  updateGym(id: number, gymData: Gym): Observable<Gym> {
    return this.http.put<Gym>(`${this.apiUrl}${id}/`, gymData);
  }

  deleteGym(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`);
  }
}
