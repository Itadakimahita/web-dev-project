import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BookingService } from '../services/booking.service';

@Component({
  selector: 'app-booking',
  templateUrl: './booking.component.html',
  styleUrls: ['./booking.component.css']
})
export class BookingComponent implements OnInit {
  timestampId: number = 0;

  constructor(
    private route: ActivatedRoute,
    private bookingService: BookingService,
    private router: Router
  ) { }

  ngOnInit() {
    this.timestampId = +this.route.snapshot.paramMap.get('id')!;
  }

  book() {
    this.bookingService.bookTimestamp(this.timestampId).subscribe({
      next: () => this.router.navigate(['/gyms']),
      error: (error: any) => console.error('Booking failed', error)
    });
  }
}
