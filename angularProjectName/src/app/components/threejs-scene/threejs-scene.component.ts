import { Component, OnInit, OnDestroy, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { DataService } from '../../services/data.service';
import * as THREE from "three"

@Component({
  selector: 'app-threejs-scene',
  imports: [],
  templateUrl: './threejs-scene.component.html',
  styleUrl: './threejs-scene.component.sass'
})
export class ThreejsSceneComponent implements OnInit, OnDestroy, AfterViewInit {
  @ViewChild('canvasContainer') canvasContainer!: ElementRef<HTMLDivElement>;

  private scene!: THREE.Scene;
  private camera! : THREE.PerspectiveCamera;
  private renderer!: THREE.WebGLRenderer;
  private cube!: THREE.Mesh;
  object3Ds: any[] = [] //  fix make classes and parse with json
  threeObjects: THREE.Mesh[] = []

  constructor(private dataService: DataService) { return; }

  ngOnInit(): void {
    if (typeof window !== 'undefined') {
      // Setup scene and camera here
      this.scene = new THREE.Scene();
      this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      this.camera.position.z = 3;

      this.dataService.getData().subscribe({
        next: (value) => { this.object3Ds = value.objects; },
        error: (error) => { console.error(error); },
        complete: () => { console.log("Completed"); }
      })
    }
  };

  ngAfterViewInit(): void {
    // Make sure the DOM element is available before initializing the renderer
    if (typeof window !== 'undefined' && this.canvasContainer && this.canvasContainer.nativeElement) {
      // Create the renderer and attach it to the div container
      this.renderer = new THREE.WebGLRenderer();
      this.renderer.setSize(window.innerWidth/2, window.innerHeight/2);
      this.canvasContainer.nativeElement.appendChild(this.renderer.domElement); // Append the canvas to the div
      
      // Create a simple cube for demonstration
      const geometry = new THREE.SphereGeometry( 26, 32, 16 ); //new THREE.BoxGeometry();
      
      const material = new THREE.MeshBasicMaterial({ color: 0x00ff12 });
      this.cube = new THREE.Mesh(geometry, material);
      this.cube.position.set(0, 0, -50);
      
      console.log("position " + this.cube.position.x, " ", this.cube.position.y, " ", this.cube.position.z);

      for (const obj3D of this.object3Ds)
      {
        if (obj3D._class === "Point")
        {
          const sphereGeometry = new THREE.SphereGeometry( 0.25, 32, 16 ); 
          //const material = new THREE.MeshBasicMaterial( { color: 0xffff00 } ); 
          const sphere = new THREE.Mesh( sphereGeometry, material );
          const pos3d: number[] = JSON.parse(obj3D._initArguments);
          sphere.position.set(pos3d[0], pos3d[1], pos3d[2]);//.position = 
          console.log("position " + sphere.position.x, " ", sphere.position.y, " ", sphere.position.z);
 
          //console.log("osphere position is " + sphere.position.x,);
          this.threeObjects.push(sphere);
          this.scene.add(sphere);
          //scene.add( sphere );
          //const sphere = new THREE.SphereGeometry(10);//new THREE.Vector3( obj3D._initArguments), 10);
          //sphere.pos
          //let cubeA = new THREE.Mesh( sphere, material );
          //this.scene.add(new THREE.Mesh( point, material ));
          const light = new THREE.PointLight(0xFFFFFF, 1, 100);  // White point light
          light.position.set(10, 10, 10); // Position the light
          this.scene.add(light);
        }
      }
      
      //const material = new THREE.MeshBasicMaterial( {color: 0x00ff00} );

      // const cubeA = new THREE.Mesh( point, material );
      // cubeA.position.set( 100, 100, 0 );

      // const cubeB = new THREE.Mesh( geometry, material );
      // cubeB.position.set( -100, -100, 0 );

      //create a group and add the two cubes
      //These cubes can now be rotated / scaled etc as a group
      // const group = new THREE.Group();
      // group.add( cubeA );
      // group.add( cubeB );
      // this.scene.add(this.threeObjects);
      //this.scene.add(this.cube);

      // Start the animation loop
      this.animate();
    
  };
}

  ngOnDestroy(): void {
    // Clean up on destroy
    if (this.renderer) {
      this.renderer!.dispose();
    }
  }

  private animate(): void {
    requestAnimationFrame(() => this.animate());

    // Rotate the cube for animation
    //this.cube.rotation.x += 0.01;
    //this.cube.rotation.y += 0.01;

    // Render the scene
    this.renderer!.render(this.scene, this.camera);
  }
}
