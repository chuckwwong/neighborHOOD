import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchCrimeComponent } from './search-crime.component';

describe('SearchCrimeComponent', () => {
  let component: SearchCrimeComponent;
  let fixture: ComponentFixture<SearchCrimeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchCrimeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchCrimeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
