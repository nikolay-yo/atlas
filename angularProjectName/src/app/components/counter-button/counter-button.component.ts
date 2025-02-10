import { Component } from '@angular/core';
import { CommonService } from '../../services/common.service';

@Component({
  selector: 'app-counter-button',
  imports: [],
  template: '<button (click)="change()"> Add by 10</button>',
  styleUrl: './counter-button.component.sass'
})
export class CounterButtonComponent {
  constructor(private common: CommonService) {}

  change() {
    this.common.data.update((val) => val + 10)
  }
}
