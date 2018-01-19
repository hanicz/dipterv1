import { Component, OnInit, Inject } from '@angular/core';
import { Chart, ChartPoint } from 'chart.js';
import { FinanceService } from '../services/finance.service';
import { Finance } from '../entities/Finance';
import { FinanceType } from '../entities/finance-type';
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

  year: Number;
  month: Number;

  displayedColumns = ['type', 'amount', 'comment', 'date'];
  dataSource = new MatTableDataSource(this.finances);

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
    this.financeService.get_finances_by_year(2018).subscribe((json: Object) => {
      console.log(json);
      this.finances = json as Finance[];
      this.dataSource = new MatTableDataSource(this.finances);


      this.finances.forEach((f) => {
        this.labels.push(f.comment as string);
        this.amounts.push(f.amount);
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
    },
      error => console.error('Error: ' + error)
    );
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

}
