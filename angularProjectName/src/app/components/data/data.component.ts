import { Component, OnInit } from '@angular/core';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-data',

  templateUrl: './data.component.html',
  styleUrl: './data.component.sass'
})
export class DataComponent implements OnInit {
  object3Ds: any[] = []

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.dataService.getData().subscribe({
      next: (value) => { this.object3Ds = value.objects; },
      error: (error) => { console.error(error); },
      complete: () => { console.log("Completed"); }
    })
  }
}
