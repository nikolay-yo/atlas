import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ButtonCounterComponent } from './button.component';

describe('ButtonCounterComponent', () => {
  let component: ButtonCounterComponent;
  let fixture: ComponentFixture<ButtonCounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ButtonCounterComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ButtonCounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
