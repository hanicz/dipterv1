import { Component, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { TravelDialogComponent } from '../travel-dialog/travel-dialog.component';
import { TravelService } from '../services/travel.service';
import { Travel } from '../entities/travel';

@Component({
  selector: 'app-travel',
  templateUrl: './travel.component.html',
  styleUrls: ['./travel.component.css']
})
export class TravelComponent implements OnInit {

  travels: Travel[];


  constructor(
    public dialog: MatDialog,
    private travelService: TravelService) { }

  ngOnInit() {
    this.fill_travels();
  }

  fill_travels() {
    this.travelService.get_travels().subscribe((json: Object) => {
      this.travels = json as Travel[];
    },
      error => console.error('Error: ' + error)
    );
  }

  deleteTravel(travel: Travel){
    this.travelService.delete_travel(travel.id).subscribe((json: Object) => {
      this.fill_travels();
    },
      error => console.error('Error: ' + error)
    );
  }

  updateTravel(travel: Travel){
    let dialogRef = this.dialog.open(TravelDialogComponent, {
      data: { travel: travel, type: 'update' }
    });

    dialogRef.afterClosed().subscribe((result) => {
      this.fill_travels();
    });
  }

  openDialog(): void {
    let dialogRef = this.dialog.open(TravelDialogComponent, {
      data: { type: 'new' }
    });

    dialogRef.afterClosed().subscribe((result) => {
      this.fill_travels();
    });
  }
}
