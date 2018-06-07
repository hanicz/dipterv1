import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TravelImagesComponent } from './travel-images.component';

describe('TravelImagesComponent', () => {
  let component: TravelImagesComponent;
  let fixture: ComponentFixture<TravelImagesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TravelImagesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TravelImagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
