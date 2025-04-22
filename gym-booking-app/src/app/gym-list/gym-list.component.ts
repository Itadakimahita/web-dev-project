import { Component, OnInit } from '@angular/core';
import { GymService } from '../services/gym.service';
import { Gym } from '../models/gym.model';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-gym-list',
  imports: [CommonModule, RouterLink],
  templateUrl: './gym-list.component.html',
  styleUrls: ['./gym-list.component.css']
})
export class GymListComponent implements OnInit {
  gyms: Gym[] = [];

  constructor(private gymService: GymService) { }

  ngOnInit() {
    this.gymService.getGyms().subscribe({
      next: (data: Gym[]) => this.gyms = data,
      error: (error: any) => console.error('Gym fetch failed', error)
    });
  }
}
