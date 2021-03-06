import { Component, OnInit, Inject } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { Travel } from '../entities/travel';
import { TravelService } from '../services/travel.service';

@Component({
  selector: 'app-travel-dialog',
  templateUrl: './travel-dialog.component.html',
  styleUrls: ['./travel-dialog.component.css']
})
export class TravelDialogComponent implements OnInit {

  travel: Travel;
  type: String;

  constructor(private travelService: TravelService,
    public dialogRef: MatDialogRef<TravelDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any) {
    this.type = data.type;
    if(this.type == 'new') this.travel = new Travel();
    else this.travel = data.travel;
  }

  ngOnInit() {
  }


  createRecord(): void {
    if (this.type == 'new') {
      this.travelService.create_travel(this.travel).subscribe((json: Object) => {
      },
        error => console.error('Error: ' + error)
      );
      this.dialogRef.close();
    } else if (this.type == 'update') {
      this.travelService.update_travel(this.travel).subscribe((json: Object) => {
      },
        error => console.error('Error: ' + error)
      );
      this.dialogRef.close();
    }
  }
}
