import { Component } from '@angular/core';
import { GymService } from '../services/gym.service';
import { Router } from '@angular/router';
import { Gym } from '../models/gym.model';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-gym-create',
  imports: [CommonModule, FormsModule],
  templateUrl: './gym-create.component.html',
  styleUrls: ['./gym-create.component.css']
})
export class GymCreateComponent {
  gym: Gym = { name: '', address: '', is_active: true };

  constructor(private gymService: GymService, private router: Router) { }

  createGym() {
    this.gymService.createGym(this.gym).subscribe({
      next: () => this.router.navigate(['/gyms']),
      error: (error: any) => console.error('Gym creation failed', error)
    });
  }
}
