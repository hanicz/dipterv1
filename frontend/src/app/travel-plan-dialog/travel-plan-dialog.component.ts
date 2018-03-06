import { Component, OnInit, Inject } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { TravelService } from '../services/travel.service';
import { TravelPlan } from '../entities/travel-plan';

@Component({
  selector: 'app-travel-plan-dialog',
  templateUrl: './travel-plan-dialog.component.html',
  styleUrls: ['./travel-plan-dialog.component.css']
})
export class TravelPlanDialogComponent implements OnInit {

  marker: TravelPlan;
  type: String;

  constructor(private travelService: TravelService,
    public dialogRef: MatDialogRef<TravelPlanDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any) {
    this.marker = data.marker;
    this.type = data.type;
  }

  ngOnInit() {
  }


  save(): void {
    if (this.type == 'new') {
      this.travelService.create_travel_plan(this.marker).subscribe((json: Object) => {
      },
        error => console.error('Error: ' + error)
      );
      this.dialogRef.close();
    }
    else if (this.type == 'update') {
      this.travelService.update_travel_plan(this.marker).subscribe((json: Object) => {
      },
        error => console.error('Error: ' + error)
      );
      this.dialogRef.close();
    }
  }
}
