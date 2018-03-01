import { TestBed, inject } from '@angular/core/testing';

import { TravelService } from './travel.service';

describe('TravelService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [TravelService]
    });
  });

  it('should be created', inject([TravelService], (service: TravelService) => {
    expect(service).toBeTruthy();
  }));
});
