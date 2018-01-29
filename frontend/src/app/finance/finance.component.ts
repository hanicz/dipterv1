import { Component, OnInit, Inject } from '@angular/core';
import { Chart, ChartPoint } from 'chart.js';
import { FinanceService } from '../services/finance.service';
import { Finance } from '../entities/Finance';
import { FinanceType } from '../entities/finance-type';
import { AggrFinance} from '../entities/aggrfinance';
import { forEach } from '@angular/router/src/utils/collection';
import { MatTableDataSource } from '@angular/material';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { FinanceDialog } from '../finance-dialog/finance-dialog.component';

@Component({
  moduleId: module.id,
  selector: 'finance',
  templateUrl: './finance.component.html',
  styleUrls: ['./finance.component.css']
})
export class FinanceComponent {

  chart: Chart;
  finances: Finance[];
  labels: string[];
  amounts: Number[];
  colors: string[];
  financeTypes: FinanceType[];
  chartFinances: AggrFinance[];

  year: Number;
  month: Number;
  aggr_year: Number;
  aggr_month: Number;

  displayedColumns = ['type', 'amount', 'comment', 'date'];
  dataSource = new MatTableDataSource(this.chartFinances);

  constructor(
    private financeService: FinanceService,
    public dialog: MatDialog
  ) { }

  ngOnInit() {

    this.labels = [];
    this.amounts = [];
    this.colors = [];

    this.financeService.get_finance_types().subscribe((json: Object) => {
      console.log(json);
      this.financeTypes = json as FinanceType[];
    },
      error => console.error('Error: ' + error)
    );
  }

  fill_chart() {
    if (this.aggr_year != null) {
      if (this.aggr_month != null) {
        this.financeService.get_finances_by_month_aggregated(this.aggr_year, this.aggr_month).subscribe((json: Object) => {
          console.log(json);

          this.labels = [];
          this.amounts = [];
          this.colors = [];

          this.chartFinances = json as AggrFinance[];
          this.build_chart();
        },
          error => console.error('Error: ' + error)
        );
      } else {
        this.financeService.get_finances_by_year_aggregated(this.aggr_year).subscribe((json: Object) => {
          console.log(json);

          this.labels = [];
          this.amounts = [];
          this.colors = [];

          this.chartFinances = json as AggrFinance[];
          this.build_chart();
        },
          error => console.error('Error: ' + error)
        );
      }
    }
  }

  build_chart() {
    this.dataSource = new MatTableDataSource(this.chartFinances);
    this.chartFinances.forEach((f) => {
      this.labels.push(f.type as string);
      this.amounts.push(f.sum);
      this.colors.push(this.getRandomColor());
    });

    this.chart = new Chart('canvas', {
      type: 'pie',
      data: {
        labels: this.labels,
        datasets: [
          {
            data: this.amounts as ChartPoint[],
            backgroundColor: this.colors
          }
        ]
      },
      options: {
        title: {
          display: true,
          text: 'Finance records'
        }
      }
    });
  }

  getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  openDialog(): void {
    let dialogRef = this.dialog.open(FinanceDialog, {
      data: { financeTypes: this.financeTypes }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
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

}
