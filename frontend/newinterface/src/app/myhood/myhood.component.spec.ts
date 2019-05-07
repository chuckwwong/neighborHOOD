import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MyhoodComponent } from './myhood.component';

describe('MyhoodComponent', () => {
  let component: MyhoodComponent;
  let fixture: ComponentFixture<MyhoodComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MyhoodComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MyhoodComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
