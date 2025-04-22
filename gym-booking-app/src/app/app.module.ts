import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { routes } from './app.routes';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { GymListComponent } from './gym-list/gym-list.component';
import { GymCreateComponent } from './gym-create/gym-create.component';
import { GymDetailComponent } from './gym-detail/gym-detail.component';
import { BookingComponent } from './booking/booking.component';
import { AuthGuard } from './auth.guard';
import { AuthService } from './services/auth.service'; // Импортируем сервисы
import { GymService } from './services/gym.service';
import { BookingService } from './services/booking.service';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { JwtInterceptor } from './jwt.interceptor';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    GymListComponent,
    GymCreateComponent,
    GymDetailComponent,
    BookingComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    RouterModule.forRoot(routes)
  ],
  providers: [
    AuthGuard,
    AuthService,
    GymService,
    BookingService,
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
