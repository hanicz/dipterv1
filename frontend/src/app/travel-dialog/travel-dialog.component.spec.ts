import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TravelDialogComponent } from './travel-dialog.component';

describe('TravelDialogComponent', () => {
  let component: TravelDialogComponent;
  let fixture: ComponentFixture<TravelDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TravelDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TravelDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
