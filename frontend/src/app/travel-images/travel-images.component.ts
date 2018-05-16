import { Component, OnInit, Inject } from '@angular/core';
import { TravelImage } from '../entities/travelimage';
import { TravelService } from '../services/travel.service';
import { Travel } from '../entities/travel';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';

@Component({
  selector: 'travel-images',
  templateUrl: './travel-images.component.html',
  styleUrls: ['./travel-images.component.css']
})
export class TravelImagesComponent implements OnInit {

  images: TravelImage[];
  travels: Travel[];
  selectedTravel: Travel;

  cardHidden: boolean = false;

  constructor(private travelService: TravelService,
              public dialog: MatDialog) { }

  ngOnInit() {
    this.selectedTravel = new Travel();
    this.selectedTravel.id = 0;
    this.fill_travels();
  }

  openDialog(image: TravelImage): void {
    let dialogRef = this.dialog.open(TravelImagesDialog, {
      
      data: { image: image }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }


  fill_travels() {
    this.travelService.get_travels().subscribe((json: Object) => {
      this.travels = json as Travel[];
      this.selectedTravel = this.travels[0];
      this.fill_images();
    },
      error => console.error('Error: ' + error)
    );
  }

  fill_images() {
    this.travelService.get_image_src(this.selectedTravel.id).subscribe((json: Object) => {
      this.images = json as TravelImage[];
    },
      error => console.error('Error: ' + error)
    );
  }

}

@Component({
  selector: 'travel-images-dialog',
  templateUrl: 'travel-images-dialog.html',
})
export class TravelImagesDialog {

  image: TravelImage;

  constructor(
    public dialogRef: MatDialogRef<TravelImagesDialog>,
    @Inject(MAT_DIALOG_DATA) public data: any) { 
      this.image = data.image;
    }

  delete(): void {
    this.dialogRef.close();
  }

}