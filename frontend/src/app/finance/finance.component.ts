import { Component, OnInit, Inject, ViewChild } from '@angular/core';
import { FinanceService } from '../services/finance.service';
import { Finance } from '../entities/Finance';
import { FinanceType } from '../entities/finance-type';
import { AggrFinance} from '../entities/aggrfinance';
import { MatTableDataSource } from '@angular/material';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA, MatSort, MatSnackBar } from '@angular/material';
import { FinanceDialog } from '../finance-dialog/finance-dialog.component';
import { DatePipe } from '@angular/common';

@Component({
  moduleId: module.id,
  selector: 'finance',
  templateUrl: './finance.component.html',
  styleUrls: ['./finance.component.css']
})
export class FinanceComponent implements OnInit{

  finances: Finance[];
  financeTypes: FinanceType[];
  chartFinances: AggrFinance[];

  selectedType: FinanceType;

  year: Number;
  month: Number;
  finance: Finance;

  displayedColumns = ['type', 'amount', 'comment', 'date', 'update'];
  dataSource = new MatTableDataSource(this.finances);
  @ViewChild(MatSort) sort: MatSort;

  constructor(
    private financeService: FinanceService,
    public dialog: MatDialog,
    private datePipe: DatePipe,
    public snackBar: MatSnackBar
  ) { 
    this.finance = new Finance();
    this.finance.finance_date = new Date();
   }

  ngOnInit() {
    this.fill_finance_types();
  }

  get_formatted_date(date: Date){
    return this.datePipe.transform(date, 'yyyy-MM-dd');
  }

  get_formatted_number(number: String){
    return number.replace(/,/g,".");
  }

  createRecord(): void {
      this.finance.finance_type_id = this.selectedType.id;
      this.financeService.new_finance(this.finance).subscribe((json: Object) => {
        let extraClasses = ['background-green'];
        this.snackBar.open("Finance record successfully created", null, {
          duration: 1000,
          panelClass: extraClasses
        });
        this.fillTable();
        this.finance = new Finance();
        this.finance.finance_date = new Date();
        this.selectedType = new FinanceType();
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
          this.finances = json as Finance[];
          this.dataSource = new MatTableDataSource(this.finances);
          this.dataSource.sort = this.sort;
        },
          error => console.error('Error: ' + error)
        );
      } else {
        this.financeService.get_finances_by_month(this.year, this.month).subscribe((json: Object) => {
          this.finances = json as Finance[];
          this.dataSource = new MatTableDataSource(this.finances);
          this.dataSource.sort = this.sort;
        },
          error => console.error('Error: ' + error)
        );
      }
    }
  }

  getTotalAmount() {
    if(this.finances == undefined) return 0;
    return this.finances.map(t => t.amount).reduce((acc, value) => acc + value, 0);
  }

  deleteFinance(finance: Finance){
    this.financeService.delete_finance(finance.id).subscribe((json: Object) => {
      this.fillTable();
    },
      error => console.error('Error: ' + error)
    );
  }

}