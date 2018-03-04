import { Component, OnInit } from '@angular/core';
import { FinanceService } from '../services/finance.service';
import { AggrFinance } from '../entities/aggrfinance';
import { Chart, ChartPoint } from 'chart.js';
import { MatTableDataSource } from '@angular/material';

@Component({
  selector: 'app-finance-chart',
  templateUrl: './finance-chart.component.html',
  styleUrls: ['./finance-chart.component.css']
})
export class FinanceChartComponent implements OnInit {

  labels: string[];
  amounts: Number[];
  colors: string[];
  aggr_year: Number;
  aggr_month: Number;
  chartFinances: AggrFinance[];
  chartHidden: boolean = true;
  chart: Chart;
  dataSource = new MatTableDataSource(this.chartFinances);

  constructor(private financeService: FinanceService) { }

  ngOnInit() {
    this.labels = [];
    this.amounts = [];
    this.colors = [];
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

    if (this.chart !== undefined) {
      this.chart.ngOnDestroy();
    }

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

}
