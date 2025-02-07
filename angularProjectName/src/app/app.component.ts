import { Component } from '@angular/core';
import { ThreejsSceneComponent } from './threejs-scene/threejs-scene.component';

import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ThreejsSceneComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.sass'
})
export class AppComponent {
  title = 'angularProjectName';
}
