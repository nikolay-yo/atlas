import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ThreejsSceneComponent } from './threejs-scene.component';

describe('ThreejsSceneComponent', () => {
  let component: ThreejsSceneComponent;
  let fixture: ComponentFixture<ThreejsSceneComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ThreejsSceneComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ThreejsSceneComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
