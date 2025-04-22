import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { GymListComponent } from './gym-list/gym-list.component';
import { GymCreateComponent } from './gym-create/gym-create.component';
import { GymDetailComponent } from './gym-detail/gym-detail.component';
import { BookingComponent } from './booking/booking.component';
import { AuthGuard } from './auth.guard';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'gyms', component: GymListComponent, canActivate: [AuthGuard] },
  { path: 'gyms/create', component: GymCreateComponent, canActivate: [AuthGuard] },
  { path: 'gyms/:id', component: GymDetailComponent, canActivate: [AuthGuard] },
  { path: 'book/:id', component: BookingComponent, canActivate: [AuthGuard] },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
];
