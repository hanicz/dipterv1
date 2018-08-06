import { Component, OnInit, Inject } from '@angular/core';
import { TravelImage } from '../entities/travelimage';
import { TravelService } from '../services/travel.service';
import { Travel } from '../entities/travel';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';

@Component({
  selector: 'travel-images',
  templateUrl: './travel-images.component.html',
  styleUrls: ['./travel-images.component.css']
})
export class TravelImagesComponent implements OnInit {

  images: TravelImage[];
  travels: Travel[];
  paginatedImages: TravelImage[];
  selectedTravel: Travel;
  numberOfPictures: Number;
  index: number;

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
      height: '90vh',
      width: '160vh',
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
      this.paginatedImages = [];
      var maxIndex = (this.images.length > 32) ? 32 : this.images.length;
      for (let i = 0; i < maxIndex; i++) {
        this.paginatedImages.push(this.images[i]);
        console.log(this.paginatedImages[i]);
      }
      this.index = 32;
      this.numberOfPictures = this.images.length;
    },
      error => console.error('Error: ' + error)
    );
  }

  next() {
    if (this.index < this.images.length) {
      this.paginatedImages = [];
      let limit = (this.index + 32 < this.images.length) ? this.index + 32 : this.images.length;
      for (let i = this.index; i < limit; i++) {
        this.paginatedImages.push(this.images[i]);
      }
      this.index += 32;
    }
  }

  previous() {
    if (this.index - 32 > 0) {
      this.paginatedImages = [];
      let limit = (this.index - 64 > 0) ? (this.index - 64) : 0;

      for (let i = limit; i < limit + 32; i++) {
        this.paginatedImages.push(this.images[i]);
      }
      this.index -= 32;
    }
  }

}

@Component({
  selector: 'travel-images-dialog',
  templateUrl: 'travel-images-dialog.html',
  styleUrls: ['travel-images-dialog.css']
})
export class TravelImagesDialog {

  image: TravelImage;
  angle = 0;

  constructor(
    public dialogRef: MatDialogRef<TravelImagesDialog>,
    @Inject(MAT_DIALOG_DATA) public data: any) {
    var downloadImage = data.image;
    downloadImage.src = downloadImage.src.replace("thumbnail","download");
    this.image = downloadImage;
  }

  delete(): void {
    this.dialogRef.close();
  }

  rotate(): void {
    let img = document.getElementById('image');
    this.angle = (this.angle + 90) % 360;
    img.className = "rotate" + this.angle;
  }

}