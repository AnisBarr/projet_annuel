import { HomePage } from './main/home-page/home-page.component';
import { MainModule } from './main/main.module';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
  {
    path: '',
    redirectTo: '/main/homePage',
    pathMatch: 'full' 
  },
  { 
    path: 'main',
    loadChildren: "./main/main.module#MainModule" 
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
