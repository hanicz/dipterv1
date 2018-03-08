import { Component, OnInit } from '@angular/core';
import { TravelImage } from '../entities/travelimage';

@Component({
  selector: 'app-travel-images',
  templateUrl: './travel-images.component.html',
  styleUrls: ['./travel-images.component.css']
})
export class TravelImagesComponent implements OnInit {

  images: TravelImage[];

  constructor() { }

  ngOnInit() {
  }

}
