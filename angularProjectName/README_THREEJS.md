To integrate **Three.js** into an existing Angular application and create a component that renders 3D content, follow these steps:

### Step 1: Install Three.js
You need to install Three.js as a dependency in your Angular project.

1. Open a terminal in your project directory.
2. Run the following command to install Three.js via npm:

   ```bash
   npm install three
   ```

### Step 2: Create a New Component for Three.js
Now, you'll create a component to manage your 3D scene.

1. Generate a new Angular component using Angular CLI:

   ```bash
   ng generate component threejs-scene
   ```

   This will create the component files: `threejs-scene.component.ts`, `threejs-scene.component.html`, and `threejs-scene.component.css`.

### Step 3: Set Up Three.js in Your Component

In your newly created component, you will set up Three.js to render a 3D scene.

1. Open `threejs-scene.component.ts` and add the necessary imports from Three.js. Then, set up the Three.js scene inside the component.

Here's a basic setup for your component:

#### `threejs-scene.component.ts`
```typescript
import { Component, OnInit, OnDestroy, ElementRef } from '@angular/core';
import * as THREE from 'three';

@Component({
  selector: 'app-threejs-scene',
  templateUrl: './threejs-scene.component.html',
  styleUrls: ['./threejs-scene.component.css']
})
export class ThreejsSceneComponent implements OnInit, OnDestroy {
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private renderer: THREE.WebGLRenderer;
  private cube: THREE.Mesh;

  constructor(private el: ElementRef) {}

  ngOnInit(): void {
    this.initThreeJS();
    this.animate();
  }

  ngOnDestroy(): void {
    // Clean up on destroy
    if (this.renderer) {
      this.renderer.dispose();
    }
  }

  private initThreeJS(): void {
    // Set up the scene, camera, and renderer
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    this.renderer = new THREE.WebGLRenderer();
    this.renderer.setSize(window.innerWidth, window.innerHeight);

    // Append the renderer to the DOM
    this.el.nativeElement.appendChild(this.renderer.domElement);

    // Create a cube and add it to the scene
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    this.cube = new THREE.Mesh(geometry, material);
    this.scene.add(this.cube);

    // Set the camera position
    this.camera.position.z = 5;
  }

  private animate(): void {
    requestAnimationFrame(() => this.animate());

    // Rotate the cube for animation
    this.cube.rotation.x += 0.01;
    this.cube.rotation.y += 0.01;

    // Render the scene
    this.renderer.render(this.scene, this.camera);
  }
}
```

### Step 4: Add the Component to Your Template
Next, you need to add the component to your application’s template.

1. Open `app.component.html` (or wherever you'd like to display the Three.js scene).
2. Insert the `<app-threejs-scene></app-threejs-scene>` tag in the template:

   ```html
   <app-threejs-scene></app-threejs-scene>
   ```

### Step 5: Adjust Styles (Optional)
You might want to adjust the CSS to make sure your 3D scene occupies the full screen or fits within a specific area. For example, in `threejs-scene.component.css`, you could add:

```css
:host {
  display: block;
  width: 100%;
  height: 100%;
}

canvas {
  display: block; /* Remove space below canvas */
  width: 100%;
  height: 100%;
}
```

### Step 6: Serve the Application
Now that everything is set up, you can run the Angular app:

```bash
ng serve
```

Navigate to `http://localhost:4200/` in your browser, and you should see a rotating cube rendered using Three.js in your Angular component!

### Recap:
1. Install Three.js: `npm install three`.
2. Create a new Angular component: `ng generate component threejs-scene`.
3. Set up Three.js in the component by creating a scene, camera, and renderer.
4. Animate the scene (e.g., a rotating cube).
5. Add the component to your template to display the 3D content.
6. Optionally, adjust the styles to ensure proper rendering.

With this setup, you can easily add more Three.js objects, animations, or interactions to your Angular app. Would you like to add something more complex or explore specific Three.js features?

https://dev.to/renancferro/understanding-and-implementing-threejs-with-angular-and-creating-a-3d-animation-3eea

npm i @types/three