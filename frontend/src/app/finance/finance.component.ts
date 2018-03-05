import { Component, OnInit, Inject } from '@angular/core';
import { FinanceService } from '../services/finance.service';
import { Finance } from '../entities/Finance';
import { FinanceType } from '../entities/finance-type';
import { AggrFinance} from '../entities/aggrfinance';
import { forEach } from '@angular/router/src/utils/collection';
import { MatTableDataSource } from '@angular/material';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { FinanceDialog } from '../finance-dialog/finance-dialog.component';
import { DatePipe } from '@angular/common';

@Component({
  moduleId: module.id,
  selector: 'finance',
  templateUrl: './finance.component.html',
  styleUrls: ['./finance.component.css']
})
export class FinanceComponent {

  finances: Finance[];
  financeTypes: FinanceType[];
  chartFinances: AggrFinance[];

  year: Number;
  month: Number;

  displayedColumns = ['type', 'amount', 'comment', 'date', 'update'];
  dataSource = new MatTableDataSource(this.finances);

  constructor(
    private financeService: FinanceService,
    public dialog: MatDialog,
    private datePipe: DatePipe
  ) { 
   }

  ngOnInit() {
    this.fill_finance_types();
  }

  get_formatted_date(date: Date){
    return this.datePipe.transform(date, 'yyyy-MM-dd');
  }

  get_finance_type_name(id: Number) {
    let retVal;
    this.financeTypes.forEach((f) => {
      if(f.id == id) {
        retVal = f.name;
      }
    });
    return retVal;
  }

  fill_finance_types(){
    this.financeService.get_finance_types().subscribe((json: Object) => {
      console.log(json);
      this.financeTypes = json as FinanceType[];
    },
      error => console.error('Error: ' + error)
    );
  }

  openDialog(): void {
    let dialogRef = this.dialog.open(FinanceDialog, {
      data: { financeTypes: this.financeTypes,
              type: 'new' }
    });

    dialogRef.afterClosed().subscribe((result) => {
      this.fill_finance_types();
    });
  }

  updateFinance(finance: Finance): void{
    let dialogRef = this.dialog.open(FinanceDialog, {
      data: { finance: finance,
              financeTypes: this.financeTypes,
              type: 'update' }
    });

    dialogRef.afterClosed().subscribe((result) => {
      this.fill_finance_types();
    });
  }

  applyFilter(filterValue: string) {
    filterValue = filterValue.trim();
    filterValue = filterValue.toLowerCase();
    this.dataSource.filter = filterValue;
  }

  fillTable() {
    if (this.year != null) {
      if (this.month == null) {
        this.financeService.get_finances_by_year(this.year).subscribe((json: Object) => {
          console.log(json);
          this.finances = json as Finance[];
          this.dataSource = new MatTableDataSource(this.finances);
        },
          error => console.error('Error: ' + error)
        );
      } else {
        this.financeService.get_finances_by_month(this.year, this.month).subscribe((json: Object) => {
          console.log(json);
          this.finances = json as Finance[];
          this.dataSource = new MatTableDataSource(this.finances);
        },
          error => console.error('Error: ' + error)
        );
      }
    }
  }

  deleteFinance(finance: Finance){
    this.financeService.delete_finance(finance.id).subscribe((json: Object) => {
      this.fillTable();
    },
      error => console.error('Error: ' + error)
    );
  }

}
