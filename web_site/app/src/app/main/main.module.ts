import { StartPageService } from './start-page/start-page.service';
import { HomePage } from './home-page/home-page.component';
import { NgModule } from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import { StartPage } from './start-page/start-page.component';
import { Routes, RouterModule } from '@angular/router';
import { WebcamModule } from 'ngx-webcam';
import { CommonModule } from '@angular/common';  
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';


const routes: Routes = [
    {
      path: '',
      redirectTo: 'homePage',
      pathMatch: 'full' 
    },
    { 
      path: 'homePage',
      component: HomePage 
    },
    {
        path: 'startPage',
        component: StartPage
    }
  ];

@NgModule({
    declarations: [
      StartPage,
      HomePage
    ],
    imports: [
        RouterModule.forChild(routes),
        MatButtonModule,
        MatIconModule,
        WebcamModule,
        CommonModule,
        FormsModule,
        HttpClientModule
    ],
    providers: [
      StartPageService
    ],
  })

  export class MainModule { }