import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ToDoFlowComponent } from './to-do-flow.component';

describe('ToDoFlowComponent', () => {
  let component: ToDoFlowComponent;
  let fixture: ComponentFixture<ToDoFlowComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ToDoFlowComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ToDoFlowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
