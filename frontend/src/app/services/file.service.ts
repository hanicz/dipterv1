/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable }    from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { CustomResponse } from '../utils/customResponse'

import 'rxjs/add/operator/map';



@Injectable()
export class FileService {

  private headers = new Headers({'Content-Type': 'multipart/form-data',
                                  'Accept': 'application/json'});
  private userUrl = 'http://localhost:5000/files';

  constructor(private http: Http) { }

  upload_file(file : File[]) {
    let headers = new Headers();
    let formData:FormData = new FormData();
    formData.append('file', file[0], file[0].name);
    console.log(file[0].name)
    // for (let i = 0; i < files.length; i++) {
    //     formData.append(`files[]`, files[i], files[i].name);
    // }

    const url = `${this.userUrl}/file/1`;
    return this.http.post(url,formData,{
        headers:this.headers,
        withCredentials: true
      })
      .map((res: Response) => res.json());
  }

  get_files(folder_id: number){
    const url = `${this.userUrl}/userFiles/` + folder_id;
    return this.http.get(url,{
        headers:this.headers,
        withCredentials: true
      })
      .map((res: Response) => res.json());
  }

  get_folders(folder_id: number){
    const url = `${this.userUrl}/userFolders/` + folder_id;
    return this.http.get(url,{
      headers:this.headers,
        withCredentials: true
      })
      .map((res: Response) => res.json());
  }

}
