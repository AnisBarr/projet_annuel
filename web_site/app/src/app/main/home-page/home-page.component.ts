import { Component, OnDestroy, OnInit, ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector     : 'home-page',
    templateUrl  : './home-page.component.html',
    styleUrls    : ['./home-page.component.scss'],
    encapsulation: ViewEncapsulation.None
})
export class HomePage implements OnInit, OnDestroy
{
    constructor(
        private router: Router
    ){

    }

    ngOnInit(){

    }

    ngOnDestroy() {
        
    }

    startPage(){
        this.router.navigateByUrl('main/startPage');
    }
}