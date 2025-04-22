import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BookingService {
  private apiUrl = 'http://localhost:8000/timestamps/';

  constructor(private http: HttpClient) { }

  bookTimestamp(id: number): Observable<void> {
    return this.http.post<void>(`${this.apiUrl}${id}/book/`, {});
  }
}
