import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CrimesListComponent } from './crimes-list.component';

describe('CrimesListComponent', () => {
  let component: CrimesListComponent;
  let fixture: ComponentFixture<CrimesListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CrimesListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CrimesListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
