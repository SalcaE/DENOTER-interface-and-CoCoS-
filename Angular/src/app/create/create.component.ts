import {
  Component, Directive,
  ElementRef,
  HostBinding,
  OnInit,
  ViewChild
} from '@angular/core';

import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {RequestService} from '../request.service';
import {CdkDragDrop, moveItemInArray, transferArrayItem} from '@angular/cdk/drag-drop';
import {FormControl, Validators} from '@angular/forms';
import {MatCheckboxChange} from '@angular/material/checkbox';
import * as fileSaver from 'file-saver';

class ClientError {
  code: string | undefined;
  description: string | undefined;
}


interface MClass {
  name: string;
  selected: boolean;
  percentage: number | undefined;
  MClassCollection?: MClass[];
}

@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.css']
})
export class CreateComponent implements OnInit {

  constructor(private http: HttpClient, private requestService: RequestService) {
  }

  @ViewChild('fileDropRef', {static: false}) fileDropEl: ElementRef | undefined;

  resHeadSelected: string | undefined;
  resModifierSelected: string | undefined;

  dato: any;

  HSave = '';
  HIndex = -1;
  MSave = '';
  MIndex = -1;

  dropText = 'Choose a file or drag here';
  readComplete = '';
  resultFile = '';
  downloadFileName = '';

  // elementi grafici aggiornabili da codice
  styleFromParent = {opacity: '0'};
  styleFromParentFile = {opacity: '0'};
  styleBtnDownload = {opacity: '0'};

  fileName = '';

  file: any;

  // dati delle liste delle textbox
  myControl = new FormControl();
  options: string[] = [];
  options1: string[] = [];

  arrayH: string[] = [];
  error = '';
  checked = false;
  headC: MClass = {
    name: 'Dynamic HClass List',
    selected: false,
    MClassCollection: [],
    percentage: undefined
  };

  tipicheH: MClass = {
    name: 'Dynamic HClass List',
    selected: false,
    MClassCollection: [],
    percentage: undefined
  };

  modifierC: MClass = {
    name: 'Dynamic HClass List',
    selected: false,
    MClassCollection: [],
    percentage: undefined
  };

  tipicheM: MClass = {
    name: 'Dynamic HClass List',
    selected: false,
    MClassCollection: [],
    percentage: undefined
  };

  @Directive({
    selector: '[appDnd]'
  })

  @HostBinding('class.fileover') fileOver: boolean | undefined;

  ngOnInit(): void {
  }

  onFileSelectedDrop(event: any) {
    this.file = event;
    this.styleFromParent = {opacity: '100'};
    this.dropText = 'File caricato: ' + this.file.name;

  }

  onFileSelected(event: any) {
    this.file = event.target.files[0];
    if (event.target.files[0]) {
      this.dropText = 'File caricato: ' + this.file.name;
    }
    this.styleFromParent = {opacity: '100'};
  }

  uploadOnto() {

    if (this.file) {

      this.fileName = this.file.name;

      const formData = new FormData();

      formData.append('file', this.file);

      this.requestService.uploadOntology(formData).subscribe(result => {

          if (result.response !== 'Formato non valido') {
            this.readComplete = 'File letto correttamente';
            this.arrayH = result;
          } else {

            this.readComplete = result.response;
            this.arrayH = [];
            this.headC.MClassCollection = [];
            this.tipicheH.MClassCollection = [];
            this.modifierC.MClassCollection = [];
            this.tipicheM.MClassCollection = [];
          }

          for (const i in this.arrayH) {

            const item = this.arrayH;
            const str = String(item[i]);
            const res = str.split('.');
            this.arrayH[i] = res[1];

          }

          this.options = this.arrayH;
          this.options1 = this.arrayH;

        },
        (error: HttpErrorResponse) => {
          if (error.status === 400) {
            const errors: Array<ClientError> = error.error;
            errors.forEach(clientError => {
              console.log(clientError.code);
            });
          }
        },
      );
    }
  }

  drop(event: CdkDragDrop<string[] | any>) {

    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      transferArrayItem(event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex);
    }
    this.dato = event.container.data;
  }

  changeCombo(value: any) {
    this.options1.forEach((arrayItem) => {

      if (arrayItem === value) {
        if (this.MSave !== '') {
          this.options.splice(this.MIndex, 0, this.MSave);
        }
        this.MSave = value;
        const index = this.options.indexOf(arrayItem);
        this.MIndex = index;
        this.options.splice(index, 1);
      }
    });
  }

  changeCombo1(value: any) {
    this.options.forEach((arrayItem) => {

      if (arrayItem === value) {
        if (this.HSave !== '') {
          this.options1.splice(this.HIndex, 0, this.HSave);
        }
        this.HSave = value;
        const index = this.options1.indexOf(arrayItem);
        this.HIndex = index;
        this.options1.splice(index, 1);
        console.log('Eliminato : ');
      }
    });
  }


  showOptionsH(event: MatCheckboxChange, selected: string): void {
    // @ts-ignore
    this.headC.MClassCollection.forEach(function (arrayItem) {

      if (arrayItem.name === selected) {
        arrayItem.selected = event.checked;
        if (event.checked === true) {
          arrayItem.name = '-' + arrayItem.name;
          arrayItem.selected = event.checked;

        } else {
          arrayItem.name = arrayItem.name.replace('-', '');
        }
        console.log(arrayItem.name + ' ' + arrayItem.selected);
      }
    });

  }

  showOptionsHT(event: MatCheckboxChange, selected: string): void {
    // @ts-ignore
    this.tipicheH.MClassCollection.forEach((arrayItem: any) => {

      if (arrayItem.name === selected) {
        arrayItem.selected = event.checked;
        const str = arrayItem.name;
        const res = str.split('-');

        // this.isChecked = arrayItem.selected;
        if (event.checked === true && res[1] === undefined) {
          arrayItem.name = '-' + arrayItem.name;
        } else {
          arrayItem.name = arrayItem.name.replace('-', '');
        }
        console.log(arrayItem.name + ' ' + arrayItem.selected);
      }
    });
  }

  showOptionsM(event: MatCheckboxChange, selectedElem: string): void {
    // @ts-ignore
    this.modifierC.MClassCollection.forEach(function (arrayItem) {

      if (arrayItem.name === selectedElem) {
        arrayItem.selected = event.checked;
        if (event.checked === true) {
          arrayItem.name = '-' + arrayItem.name;
          arrayItem.selected = event.checked;

        } else {
          arrayItem.name = arrayItem.name.replace('-', '');
        }
        console.log(arrayItem.name + ' ' + arrayItem.selected);
      }
    });
  }

  showOptionsMT(event: MatCheckboxChange, selectedElem: string): void {
    // @ts-ignore
    this.tipicheM.MClassCollection.forEach(function (arrayItem) {

      if (arrayItem.name === selectedElem) {
        arrayItem.selected = event.checked;
        if (event.checked === true) {
          arrayItem.name = '-' + arrayItem.name;
          arrayItem.selected = event.checked;

        } else {
          arrayItem.name = arrayItem.name.replace('-', '');
        }
      }
    });
  }

  headSelected(option: string) {
    // @ts-ignore
    if (this.headC.MClassCollection?.length > 0) {
      this.headC.MClassCollection = [];
    }
    this.resHeadSelected = option;
    this.requestService.getClasses(option).subscribe(result => {

      result.forEach((arrayItem: any) => {
        const str = arrayItem;
        const res = str.split('.');
        this.headC.MClassCollection?.push({name: res[1], selected: false, percentage: 0});
      });
    });

  }

  ModifierSelected(option: string) {
    // @ts-ignore
    if (this.modifierC.MClassCollection?.length > 0) {
      this.modifierC.MClassCollection = [];
    }
    this.resModifierSelected = option;
    this.requestService.getClasses(option).subscribe(result => {

      result.forEach((arrayItem: any) => {
        const str = arrayItem;
        const res = str.split('.');
        this.modifierC.MClassCollection?.push({name: res[1], selected: false, percentage: 0});
      });
    });
  }

  savePercentageH(number: any, elem: string) {
    // @ts-ignore
    this.tipicheH.MClassCollection.forEach(function (arrayItem) {
      if (arrayItem.name === elem) {
        console.log('perc' + number.target.value);
        arrayItem.percentage = number.target.value;
      }
    });
  }

  savePercentageM(number: any, elem: string) {
    // @ts-ignore
    this.tipicheM.MClassCollection.forEach(function (arrayItem) {
      if (arrayItem.name === elem) {
        arrayItem.percentage = number.target.value;
      }
    });
  }

  uploadFileCreated() {

    const file = {
      head: [],
      modifier: [],
      headT: [],
      modifierT: []
    };

    for (const i in this.headC.MClassCollection) {

      // @ts-ignore
      const item = this.headC.MClassCollection[i];

      if (i === '0') {
        // @ts-ignore
        file.head.push(this.resHeadSelected);
      }
      // @ts-ignore
      file.head.push(item.name);
    }

    console.log('Head :' + file.head);

    for (const i in this.modifierC.MClassCollection) {
      // @ts-ignore
      const item = this.modifierC.MClassCollection[i];

      // @ts-ignore
      if (i === '0') {

        // @ts-ignore
        file.modifier.push(this.resModifierSelected);
      }
      // @ts-ignore
      file.modifier.push(item.name);
    }
    console.log('Modifier :' + file.modifier);

    this.error = '';
    for (const i in this.tipicheH.MClassCollection) {
      // @ts-ignore
      const item = this.tipicheH.MClassCollection[i];

      const str = item.name;
      const res = str.split(':');

      if (res[0] === item.name) {
        item.name = item.name + ':';
      }

      if (item.percentage === undefined) {
        // @ts-ignore
        item.percentage = 0.00;
      }
      const ris = item.name + String(item.percentage);

      // @ts-ignore
      file.headT.push(ris);

      if (item.percentage > 1) {
        this.error = 'Le probabilità delle proprietà tipiche del head non posso essere maggiori di 1';
      }

    }
    console.log('HeadT :' + file.headT);

    // ARRAY ModifierTT
    // tslint:disable-next-line:forin
    for (const i in this.tipicheM.MClassCollection) {
      // @ts-ignore
      const item = this.tipicheM.MClassCollection[i];

      const str = item.name;
      const res = str.split(':');

      if (res[0] === item.name) {
        item.name = item.name + ':';
      }

      if (item.percentage === undefined) {
        // @ts-ignore
        item.percentage = 0.00;
      }
      const ris = item.name + String(item.percentage);
      // @ts-ignore
      file.modifierT.push(ris);
      console.log('1 ' + this.error);

      if (item.percentage > 1) {
        this.error = 'Le probabilità delle proprietà tipiche del modifier non posso essere maggiori di 1';
        console.log('2 ' + this.error);
      }

    }
    console.log('3 ' + this.error);
    console.log('ModifierT :' + file.modifierT);

    // tslint:disable-next-line:no-bitwise
    // @ts-ignore
    // tslint:disable-next-line:no-bitwise
    if (file.head.length !== 0 && file.modifier.length !== 0) {
      if (this.error === '') {
        this.requestService.uploadFileCreated(file).subscribe(result => {
          this.styleFromParentFile = {opacity: '100'};
          this.styleBtnDownload = {opacity: '100'};
          this.resultFile = result.response;
          this.downloadFileName = result.name;
        });
      }
    } else {
      this.error = 'Le proprietà rigide non possono essere vuote';
    }
  }

  returnBlob(res: BlobPart): Blob {
    console.log('file downloaded');
    return new Blob([res]);
  }


  downloadFile() {
    console.log('super meh' + this.downloadFileName);
    this.requestService.downloadFileCreated(this.downloadFileName).subscribe(res => {
      if (res) {
        fileSaver.saveAs(this.returnBlob(res), this.downloadFileName);
      }
    });
  }


}
