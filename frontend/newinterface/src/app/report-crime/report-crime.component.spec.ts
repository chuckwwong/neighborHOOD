import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportCrimeComponent } from './report-crime.component';

describe('ReportCrimeComponent', () => {
  let component: ReportCrimeComponent;
  let fixture: ComponentFixture<ReportCrimeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ReportCrimeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ReportCrimeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
