import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GymService } from '../services/gym.service';
import { Gym } from '../models/gym.model';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-gym-detail',
  imports: [CommonModule, FormsModule],
  templateUrl: './gym-detail.component.html',
  styleUrls: ['./gym-detail.component.css']
})
export class GymDetailComponent implements OnInit {
  gym: Gym | null = null;

  constructor(
    private route: ActivatedRoute,
    private gymService: GymService,
    private router: Router
  ) { }

  ngOnInit() {
    const id = +this.route.snapshot.paramMap.get('id')!;
    this.gymService.getGym(id).subscribe({
      next: (data: Gym) => this.gym = data,
      error: (error: any) => console.error('Gym fetch failed', error)
    });
  }

  updateGym() {
    if (this.gym) {
      this.gymService.updateGym(this.gym.id!, this.gym).subscribe({
        next: () => this.router.navigate(['/gyms']),
        error: (error: any) => console.error('Gym update failed', error)
      });
    }
  }

  deleteGym() {
    if (this.gym) {
      this.gymService.deleteGym(this.gym.id!).subscribe({
        next: () => this.router.navigate(['/gyms']),
        error: (error: any) => console.error('Gym deletion failed', error)
      });
    }
  }
}
