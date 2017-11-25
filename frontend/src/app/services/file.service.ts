/**
 * Created by Hanicz on 2/19/2017.
 */
import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, Response } from '@angular/http';
import { CustomResponse } from '../utils/customResponse'
import { MyFile } from '../entities/file';
import { Folder } from '../entities/folder';
import { ResponseContentType, RequestOptions } from '@angular/http';

import 'rxjs/add/operator/map';



@Injectable()
export class FileService {

  private formDataHeaders = new Headers({
    'Content-Type': 'multipart/form-data',
    'Accept': 'application/json'
  });

  private jsonHeaders = new Headers({
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  });

  private userUrl = 'http://localhost:5000/files';

  constructor(private http: Http) { }

  upload_file(file: File[], folder_id: Number) {
    let headers = new Headers();
    let formData: FormData = new FormData();
    formData.append('file', file[0], file[0].name);
    console.log(file[0].name)
    // for (let i = 0; i < files.length; i++) {
    //     formData.append(`files[]`, files[i], files[i].name);
    // }

    const url = `${this.userUrl}/file/${folder_id}`;
    return this.http.post(url, formData, {
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  download(file_id: Number){
    const url = `${this.userUrl}/download/${file_id}`;
    let options = new RequestOptions({responseType: ResponseContentType.Blob,
                                      withCredentials: true});
    return this.http.get(url,options).map(res => res.blob());

  }

  get_files(folder_id: Number) {
    const url = `${this.userUrl}/file/${folder_id}`;
    return this.http.get(url, {
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  get_deleted_files() {
    const url = `${this.userUrl}/file/deleted`;
    return this.http.get(url, {
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  get_folders(folder_id: Number) {
    const url = `${this.userUrl}/folder/${folder_id}`;
    return this.http.get(url, {
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  get_deleted_folders() {
    const url = `${this.userUrl}/folder/deleted`;
    return this.http.get(url, {
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  rename_file(file: MyFile) {
    const url = `${this.userUrl}/file/rename`;
    return this.http.put(url, JSON.stringify(file), {
      headers: this.jsonHeaders,
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  rename_folder(folder: Folder) {
    const url = `${this.userUrl}/folder/rename`;
    return this.http.put(url, JSON.stringify(folder), {
      headers: this.jsonHeaders,
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  remove_file(id: Number) {
    const url = `${this.userUrl}/file/${id}`;
    return this.http.delete(url, {
      withCredentials: true
    }).map((res: Response) => res.json());
  }

  remove_folder(id: Number) {
    const url = `${this.userUrl}/folder/${id}`;
    return this.http.delete(url, {
      withCredentials: true
    }).map((res: Response) => res.json());
  }

  get_folder_list() {
    const url = `${this.userUrl}/folder/list`;
    return this.http.get(url, {
      withCredentials: true
    }).map((res: Response) => res.json());
  }

  move_file(folder_id: Number, file_id: Number) {
    let data = {
      'file_id': file_id,
      'new_folder_id': folder_id
    }

    const url = `${this.userUrl}/file/move`;
    return this.http.put(url, JSON.stringify(data), {
      headers: this.jsonHeaders,
      withCredentials: true
    }).map((res: Response) => res.json());
  }

  move_folder(folder_id: Number, parent_id: Number) {
    let data = {
      'folder_id': folder_id,
      'parent_id': parent_id
    }

    const url = `${this.userUrl}/folder/move`;
    return this.http.put(url, JSON.stringify(data), {
      headers: this.jsonHeaders,
      withCredentials: true
    }).map((res: Response) => res.json());
  }

  restore_file(file_id: Number) {
    const url = `${this.userUrl}/file/restore/${file_id}`;
    return this.http.put(url, null, {
      withCredentials: true
    }).map((res: Response) => res.json());
  }

  restore_folder(folder_id: Number) {
    const url = `${this.userUrl}/folder/restore/${folder_id}`;
    return this.http.put(url, null, {
      withCredentials: true
    }).map((res: Response) => res.json());
  }

  create_folder(folder: Folder) {

    let data = {
      'folderName': folder.folderName,
      'parent': String(folder.parent)
    }

    const url = `${this.userUrl}/createFolder`;
    return this.http.post(url, JSON.stringify(data), {
      headers: this.jsonHeaders,
      withCredentials: true
    }).map((res: Response) => res.json());
  }

  get_shared_with_me_files() {
    const url = `${this.userUrl}/shared`;
    return this.http.get(url, {
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }

  search_files(file_name: String) {
    const url = `${this.userUrl}/search/${file_name}`;
    return this.http.get(url, {
      withCredentials: true
    })
      .map((res: Response) => res.json());
  }
}
