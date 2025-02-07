import { Component, OnInit, OnDestroy, ElementRef } from '@angular/core';
import * as THREE from "three"

@Component({
  selector: 'app-threejs-scene',
  imports: [],
  templateUrl: './threejs-scene.component.html',
  styleUrl: './threejs-scene.component.sass'
})
export class ThreejsSceneComponent implements OnInit, OnDestroy {
  private scene = new THREE.Scene();
  private camera = new THREE.PerspectiveCamera();
  private renderer?: THREE.WebGLRenderer;
  private cube = new THREE.Mesh();

  constructor(private el: ElementRef) {}

  ngOnInit(): void {
    this.initThreeJS();
    this.animate();
  }

  ngOnDestroy(): void {
    return;
    // Clean up on destroy
    if (this.renderer) {
      this.renderer!.dispose();
    }
  }

  private initThreeJS(): void {
    // Set up the scene, camera, and renderer
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    this.renderer = new THREE.WebGLRenderer();
    this.renderer.setSize(window.innerWidth, window.innerHeight);

    // Append the renderer to the DOM
    alert("asaaaa");
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
    this.renderer!.render(this.scene, this.camera);
  }
}
