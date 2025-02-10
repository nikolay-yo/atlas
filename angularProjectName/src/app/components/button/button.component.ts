import { Component } from '@angular/core';
import { CommonService } from '../../services/common.service';


@Component({
  selector: 'app-button-counter',
  imports: [],
  template: '<button (click)="change()"> Add by 10</button>',
  styleUrl: './button.component.sass'
})
export class ButtonCounterComponent {
  constructor(private common: CommonService) {}

  change() {
    this.common.data.update((val) => val + 10)
  }
}
