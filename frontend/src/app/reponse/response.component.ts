/**
 * Created by Hanicz on 2/19/2017.
 */
import { Component, Input, OnChanges, SimpleChanges  } from '@angular/core';


@Component({
    moduleId: module.id,
    selector: 'response',
    templateUrl: './response.component.html',
    styleUrls: ['./response.component.css']
})
export class ResponseComponent {
    @Input() inresponse: String;

    public border: String;
    public background : String;

    constructor() { }

    ngOnChanges(changes: SimpleChanges) {
        for (let propName in changes) {
          if (propName == "inresponse" && this.inresponse != undefined) {
            if(this.inresponse.includes("success")){
                this.border = "green";
                this.background = "#00ff00";
            }
            else if(this.inresponse.includes("fail")){
                this.border = "red";
                this.background = "#ff3300";
            }
          }
        }
      }
}
