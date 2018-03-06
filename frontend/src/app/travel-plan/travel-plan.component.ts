import { Component, OnInit } from '@angular/core';
import { MouseEvent as AGMMouseEvent } from '@agm/core';
import { TravelPlan } from '../entities/travel-plan';
import { TravelService } from '../services/travel.service';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { TravelPlanDialogComponent } from '../travel-plan-dialog/travel-plan-dialog.component';

@Component({
  selector: 'app-travel-plan',
  templateUrl: './travel-plan.component.html',
  styleUrls: ['./travel-plan.component.css']
})
export class TravelPlanComponent implements OnInit {

  markers: TravelPlan[];

  constructor(private travelService: TravelService,
              public dialog: MatDialog) { }

  ngOnInit() {
    this.fill_markers();
  }

  fill_markers() {
    this.travelService.get_travel_plans().subscribe((json: Object) => {
      this.markers = json as TravelPlan[];
    },
      error => console.error('Error: ' + error)
    );
  }

  zoom: Number = 10;
  lat: Number = 47.475559;
  lng: Number = 19.058886;

  clickedMarker(label: string, index: number) {
    console.log(`clicked the marker: ${label || index}`)
  }

  onSelectPlan(marker: TravelPlan){
    this.lat = marker.lat;
    this.lng = marker.lng;
  }

  deletePlan(marker: TravelPlan){
    this.travelService.delete_travel_plan(marker.id).subscribe((json: Object) => {
      this.fill_markers();
    },
      error => console.error('Error: ' + error)
    );
  }

  updatePlan(marker: TravelPlan){
    let dialogRef = this.dialog.open(TravelPlanDialogComponent, {
      data: { marker: marker, type: 'update' }
    });

    dialogRef.afterClosed().subscribe((result) => {
      this.fill_markers();
    });
  }

  mapClicked($event: AGMMouseEvent) {

    let plan = new TravelPlan;

    plan.lat = $event.coords.lat;
    plan.lng = $event.coords.lng;

    let dialogRef = this.dialog.open(TravelPlanDialogComponent, {
      data: { marker: plan, type: 'new' }
    });

    dialogRef.afterClosed().subscribe((result) => {
      this.fill_markers();
    });
  }

}