import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DENOTERComponent } from './DENOTER.component';

describe('PostFileComponent', () => {
  let component: DENOTERComponent;
  let fixture: ComponentFixture<DENOTERComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DENOTERComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DENOTERComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
