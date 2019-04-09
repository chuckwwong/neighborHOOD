import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateCrimeComponent } from './create-crime.component';

describe('CreateCrimeComponent', () => {
  let component: CreateCrimeComponent;
  let fixture: ComponentFixture<CreateCrimeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateCrimeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateCrimeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
