import { Component, OnInit } from '@angular/core';
import { ThreejsSceneComponent } from './threejs-scene/threejs-scene.component';
import { PlatformServiceService } from './platform-service.service';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ThreejsSceneComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.sass'
})
export class AppComponent implements OnInit {
  
  isLoadingOnServer = false;

  title = 'angularProjectName';

  constructor(private platformService: PlatformServiceService) {}

  ngOnInit(): void {
    if (this.platformService.isServer()) {
      this.isLoadingOnServer = true;
      console.log('Running on the server');
    } else if (this.platformService.isBrowser()) {
      console.log('Running in the browser');
    }
  }
  
}
