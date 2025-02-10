import { Component, OnInit } from '@angular/core';
import { ThreejsSceneComponent } from './components/threejs-scene/threejs-scene.component';
import { PlatformCheckService } from './services/platform.service';
import { RouterOutlet } from '@angular/router';
import { CounterComponent } from "./components/counter/counter.component";
import { ButtonCounterComponent } from './components/button/button.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ThreejsSceneComponent, ButtonCounterComponent, CounterComponent ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.sass'
})
export class AppComponent implements OnInit {
  
  isLoadingOnServer = false;

  title = 'angularProjectName';

  constructor(private platformService: PlatformCheckService) {}

  ngOnInit(): void {
    if (this.platformService.isServer()) {
      this.isLoadingOnServer = true;
      console.log('Running on the server');
    } else if (this.platformService.isBrowser()) {
      console.log('Running in the browser');
    }
  }
  
}
