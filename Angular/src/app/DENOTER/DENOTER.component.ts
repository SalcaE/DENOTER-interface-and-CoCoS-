import {
  Component,
  ElementRef,
  HostBinding,
  OnInit,
  ViewChild
} from '@angular/core';
import {HttpClient, HttpClientModule, HttpErrorResponse, HttpEventType, HttpResponse} from '@angular/common/http';
import {RequestService} from '../request.service';

class ClientError {
  code: string | undefined;
  description: string | undefined;
}

@Component({
  selector: 'app-post-file',
  templateUrl: './DENOTER.component.html',
  styleUrls: ['./DENOTER.component.css']
})
export class DENOTERComponent implements OnInit {

  constructor(private http: HttpClient, private requestService: RequestService) {
  }

  @ViewChild('fileDropRef', {static: false}) fileDropEl: ElementRef | undefined;

  @HostBinding('class.fileover') fileOver: boolean | undefined;

  error: any;
  oppure = 'Choose a file or drag here';

  styleFromParent = {opacity: '0'};
  styleFileContent = {opacity: '0'};
  styleSbinner = {opacity: '0'};

  fileName = '';

  file: any;
  dropText: any;


  ngOnInit(): void {
  }

  onFileSelectedDrop(event: any) {
    this.file = event;
    this.oppure = 'File caricato: ' + this.file.name;
    if (this.dropText !== null) {
      this.styleFromParent = {opacity: '100'};
      this.styleFileContent = {opacity: '0'};
      this.dropText = '';
    }
  }

  onFileSelected(event: any) {
    this.file = event.target.files[0];
    if (event.target.files[0]) {
      this.oppure = 'File caricato: ' + this.file.name;
    }
    if (this.dropText !== null) {
      this.styleFromParent = {opacity: '100'};
      this.styleFileContent = {opacity: '0'};
      this.dropText = '';
    }
  }

  uploadFile() {

    if (this.file) {

      this.fileName = this.file.name;

      const formData = new FormData();

      formData.append('file', this.file);
      this.styleSbinner = {opacity: '100'};

      this.requestService.uploadDenoter(formData).subscribe(result => {
          this.oppure = result.response;
          this.styleSbinner = {opacity: '0'};


          if (result) {
            if (result.response !== 'formato non valido') {
              this.styleFileContent = {opacity: '100'};
              this.download(result.response);
            } else {
              this.dropText = null;
            }
          }
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


  download(ciao: string) {
    this.requestService.downloadFile(ciao).subscribe(name => {
      if (name) {

        const fileReader = new FileReader();
        fileReader.onload = (e: any) => {
          this.dropText = fileReader.result;
        };
        fileReader.readAsText(name);
      }
    });
  }


}
