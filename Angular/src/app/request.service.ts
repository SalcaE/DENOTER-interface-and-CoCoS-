import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';

const url = 'http://127.0.0.1:5000/getfile?';

@Injectable({
  providedIn: 'root'
})
export class RequestService {

  constructor(private http: HttpClient) {
  }

  downloadFile(x: string): Observable<any> {
    const param = new HttpParams().set('filename', x);
    const options = {params: param};
    return this.http.get(url, {...options, responseType: 'blob'});
  }

  uploadDenoter(formData: any): Observable<any> {
    return this.http.post<any>('http://127.0.0.1:5000/postfile', formData);
  }

  uploadOntology(formData: any): Observable<any> {
    return this.http.post<any>('http://127.0.0.1:5000/postOntology', formData);
  }

  getClasses(x: any): Observable<any> {
    const param = new HttpParams().set('classname', x);
    const options = {params: param};
    return this.http.get('http://127.0.0.1:5000/getClasses', {...options, responseType: 'json'});
  }

  uploadFileCreated(formData: any): Observable<any> {
    return this.http.post<any>('http://127.0.0.1:5000/postFileCreated', formData);
  }

  downloadFileCreated(x: any): Observable<any> {
    const param = new HttpParams().set('filename', x);
    const options = {params: param};
    return this.http.get('http://127.0.0.1:5000/dowloadFile', {...options, responseType: 'blob'});
  }


}
