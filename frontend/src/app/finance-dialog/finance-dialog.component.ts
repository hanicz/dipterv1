import { Component, OnInit, Inject } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA, MatSnackBar } from '@angular/material';
import { FinanceType } from '../entities/finance-type';
import { FinanceService } from '../services/finance.service';
import { Finance } from '../entities/Finance';


@Component({
  moduleId: module.id,
  selector: 'finance-dialog',
  templateUrl: './finance-dialog.component.html',
  styleUrls: ['./finance-dialog.component.css']
})
export class FinanceDialog {

  financeTypes: FinanceType[];
  selectedType: FinanceType;
  finance: Finance;
  newFinanceTypeName: String;
  type: String;

  constructor(
    private financeService: FinanceService,
    public snackBar: MatSnackBar,
    public dialogRef: MatDialogRef<FinanceDialog>,
    @Inject(MAT_DIALOG_DATA) public data: any) {
    this.financeTypes = data.financeTypes;
    this.type = data.type;

    if (this.type == 'new') {
      this.finance = new Finance();
      this.finance.finance_date = new Date();
    } else if (this.type == 'update') {
      this.finance = data.finance;
      this.financeTypes.forEach(ft => {
        if (ft.id == this.finance.finance_type_id)
          this.selectedType = ft;
      });
    }
  }

  createRecord(): void {
    if (this.type == 'new') {
      this.finance.finance_type_id = this.selectedType.id;
      this.financeService.new_finance(this.finance).subscribe((json: Object) => {
        let extraClasses = ['background-green'];
        this.snackBar.open("Finance record successfully created", null, {
          duration: 1000,
          panelClass: extraClasses
        });
        this.dialogRef.close();
      },
        error => {
          if (error.status == 409) {
            let extraClasses = ['background-red'];
            this.snackBar.open("Finance record already exists", null, {
              duration: 1000,
              panelClass: extraClasses
            });
          }
        }
      );
    }
    else {
      this.finance.finance_type_id = this.selectedType.id;
      this.financeService.update_finance(this.finance).subscribe((json: Object) => {
        let extraClasses = ['background-green'];
        this.snackBar.open("Finance record successfully updated", null, {
          duration: 1000,
          panelClass: extraClasses
        });
        this.dialogRef.close();
      },
        error => {
          let extraClasses = ['background-red'];
          this.snackBar.open("Finance record update failed", null, {
            duration: 1000,
            panelClass: extraClasses
          });
        }
      );
    }
  }

  createType(): void {
    this.financeService.new_finance_type(this.newFinanceTypeName).subscribe((json: Object) => {

    },
      error => console.log('Error: ' + error)
    );
    this.dialogRef.close();
  }

}