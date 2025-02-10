import { Component, OnInit, OnDestroy, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
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

  constructor() { return; }

  ngOnInit(): void {
    if (typeof window !== 'undefined') {
      // Setup scene and camera here
      this.scene = new THREE.Scene();
      this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      this.camera.position.z = 5;
    }
  }

  ngAfterViewInit(): void {
    // Make sure the DOM element is available before initializing the renderer
    if (typeof window !== 'undefined' && this.canvasContainer && this.canvasContainer.nativeElement) {
      // Create the renderer and attach it to the div container
      this.renderer = new THREE.WebGLRenderer();
      this.renderer.setSize(window.innerWidth/2, window.innerHeight/2);
      this.canvasContainer.nativeElement.appendChild(this.renderer.domElement); // Append the canvas to the div
      
      // Create a simple cube for demonstration
      const geometry = new THREE.BoxGeometry();
      const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
      this.cube = new THREE.Mesh(geometry, material);
      this.scene.add(this.cube);

      // Start the animation loop
      this.animate();
    }
  }

  ngOnDestroy(): void {
    return;
    // Clean up on destroy
    if (this.renderer) {
      this.renderer!.dispose();
    }
  }

  private animate(): void {
    requestAnimationFrame(() => this.animate());

    // Rotate the cube for animation
    this.cube.rotation.x += 0.01;
    this.cube.rotation.y += 0.01;

    // Render the scene
    this.renderer!.render(this.scene, this.camera);
  }
}
