import { StartPageService } from './start-page.service';
import { Component, OnInit, ViewEncapsulation } from '@angular/core';

import {Subject, Observable} from 'rxjs';
import {WebcamImage, WebcamInitError, WebcamUtil} from 'ngx-webcam';

@Component({
    selector     : 'start-page',
    templateUrl  : './start-page.component.html',
    styleUrls    : ['./start-page.component.scss'],
    encapsulation: ViewEncapsulation.None
})
export class StartPage implements OnInit
{

    public startVideo = false;
    public videoEven;
    public showWebcam = true;
    public allowCameraSwitch = true;
    public multipleWebcamsAvailable = false;
    public deviceId: string;
    public returnWord: string = "";
    public videoOptions: MediaTrackConstraints = {
    // width: {ideal: 1024},
    // height: {ideal: 576}
  };
  public errors: WebcamInitError[] = [];

  // latest snapshot
  public webcamImage: WebcamImage = null;

  // webcam snapshot trigger
  private trigger: Subject<void> = new Subject<void>();
  // switch to next / previous / specific webcam; true/false: forward/backwards, string: deviceId
  private nextWebcam: Subject<boolean|string> = new Subject<boolean|string>();

  constructor(
    private _startPageService :  StartPageService
  ){

  }

  public ngOnInit(): void {
    WebcamUtil.getAvailableVideoInputs()
      .then((mediaDevices: MediaDeviceInfo[]) => {
        this.multipleWebcamsAvailable = mediaDevices && mediaDevices.length > 1;
      });
    
    this._startPageService.onImageSubmit
      .subscribe(response => {
        
        if(Object.keys(response).length === 0){
          response = "";
        }
        console.log(response);
        this.returnWord += response
      });
  }

  public triggerSnapshot(): void {
    this.startVideo = true;
    this.returnWord = "";
    this.videoEven = setInterval(() => {
      this.trigger.next();
      }, 1000);
    
  }


  public stop() : void {
      this.startVideo = false;
      if(this.videoEven){
        clearInterval(this.videoEven)
      }
  }

  public toggleWebcam(): void {
    this.showWebcam = !this.showWebcam;
  }

  public handleInitError(error: WebcamInitError): void {
    this.errors.push(error);
  }

  public showNextWebcam(directionOrDeviceId: boolean|string): void {
    // true => move forward through devices
    // false => move backwards through devices
    // string => move to device with given deviceId
    this.nextWebcam.next(directionOrDeviceId);
  }

  public handleImage(webcamImage: WebcamImage): void {
    console.info('received webcam image', webcamImage);
    this.webcamImage = webcamImage;

    const data: FormData = new FormData();
    var blob = new Blob([webcamImage.imageAsBase64], {type : 'image/jpeg'});
    data.append("img", blob, "img");

    this._startPageService.submitImg(data);
  }

  public cameraWasSwitched(deviceId: string): void {
    console.log('active device: ' + deviceId);
    this.deviceId = deviceId;
  }


  public get triggerObservable(): Observable<void> {
    return this.trigger.asObservable();
  }

  public get nextWebcamObservable(): Observable<boolean|string> {
    return this.nextWebcam.asObservable();
  }
}