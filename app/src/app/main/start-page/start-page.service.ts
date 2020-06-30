
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { Router } from '@angular/router';
@Injectable()
export class StartPageService
{

    host : string = "http://localhost:8000/api/";
    onImageSubmit : BehaviorSubject<any>;

    /**
     * Constructor
     *
     * @param {HttpClient} _httpClient
     */
    constructor(
        protected _httpClient: HttpClient,
        protected _router : Router
    )
    {
        this.onImageSubmit = new BehaviorSubject({});
    }

    submitImg(img){
        return new Promise((resolve, reject) => {
            this._httpClient.post(this.host + "submitImage", img)
                .subscribe((response : any) => {
                    if(!response.sucess){ //TODO : check Result
                        this.onImageSubmit.next("error");
                        resolve(response);
                        return;
                    }
                    this.onImageSubmit.next(response.data);
                    resolve(response);
                }, reject);
        })
    }


}
