import { TestBed } from '@angular/core/testing';

import { CrimeService } from './crime.service';

describe('CrimeService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: CrimeService = TestBed.get(CrimeService);
    expect(service).toBeTruthy();
  });
});
