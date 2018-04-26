import { Component, OnInit } from '@angular/core';
import { TravelImage } from '../entities/travelimage';
import { TravelService } from '../services/travel.service';
import { Travel } from '../entities/travel';

@Component({
  selector: 'travel-images',
  templateUrl: './travel-images.component.html',
  styleUrls: ['./travel-images.component.css']
})
export class TravelImagesComponent implements OnInit {

  images: TravelImage[];
  travels: Travel[];
  selectedTravel: Travel;

  constructor(private travelService: TravelService) { }

  ngOnInit() {
    this.selectedTravel = new Travel();
    this.selectedTravel.id = 0;
    this.fill_travels();
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
