import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CommonService } from '../../services/common.service';

@Component({
  selector: 'app-counter',
  imports: [],
  template: '<p>My count: {{ this.common.data() }} </p>',
  styleUrl: './counter.component.sass',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CounterComponent {
  constructor(public common: CommonService) {
  }
}


