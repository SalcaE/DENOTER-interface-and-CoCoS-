import {Directive, HostBinding, HostListener, Output, EventEmitter} from '@angular/core';


@Directive({
  selector: '[appDnd]'
})
export class DndDirective {

  @HostBinding('class.fileover') fileOver = false;
  @Output() fileDropped = new EventEmitter<any>();

  // Dragover listener
  // tslint:disable-next-line:typedef
  @HostListener('dragover', ['$event']) onDragOver(evt: any) {
    evt.preventDefault();
    evt.stopPropagation();
    this.fileOver = true;
  }

  // Dragleave listener
  // tslint:disable-next-line:typedef
  @HostListener('dragleave', ['$event'])
  // tslint:disable-next-line:typedef
  public onDragLeave(evt: any) {
    evt.preventDefault();
    evt.stopPropagation();
    this.fileOver = false;
  }

  // Drop listener
  // tslint:disable-next-line:typedef
  @HostListener('drop', ['$event'])
  // tslint:disable-next-line:typedef
  public ondrop(evt: any) {
    //  this.totalAngularPackages = 'File caricato :';
    evt.preventDefault();
    evt.stopPropagation();

    // this.oppure = evt.name;
    this.fileOver = false;
    const files = evt.dataTransfer.files;

    //  this.totalAngularPackages = 'File caricato :';
    // this.oppure = files[0].name;
    if (files.length > 0) {
      this.fileDropped.emit(files[0]);
      // this.persona = files[0].name;
      //  this.file = files[0];
    }

  }

}
