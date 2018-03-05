import { Component, OnInit, Inject } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
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
    public dialogRef: MatDialogRef<FinanceDialog>,
    @Inject(MAT_DIALOG_DATA) public data: any) {
    this.financeTypes = data.financeTypes;
    this.type = data.type;

    if (this.type == 'new') {
      this.finance = new Finance();
      this.finance.finance_date = new Date();
    } else if (this.type == 'update') {
      console.log(data.finance.finance_date)
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
      },
        error => console.error('Error: ' + error)
      );
    }
    else {
      this.finance.finance_type_id = this.selectedType.id;
      this.financeService.update_finance(this.finance).subscribe((json: Object) => {
      },
        error => console.error('Error: ' + error)
      );
    }
    this.dialogRef.close();
  }

  createType(): void {
    this.financeService.new_finance_type(this.newFinanceTypeName).subscribe((json: Object) => {

    },
      error => console.error('Error: ' + error)
    );
    this.dialogRef.close();
  }

}