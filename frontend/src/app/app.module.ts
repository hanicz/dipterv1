import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { HttpModule }    from '@angular/http';

import { AppComponent }  from './app.component';
import { LoginComponent }  from './login/login.component';
import { UserService} from './services/user.service';
import { RegisterComponent }  from './register/register.component';

@NgModule({
  imports:      [ BrowserModule,
                  AppRoutingModule,
                  HttpModule],
  declarations: [ AppComponent,
                  LoginComponent,
                  RegisterComponent],
  bootstrap:    [ AppComponent ],
  providers: [ UserService ],
})
export class AppModule { }
