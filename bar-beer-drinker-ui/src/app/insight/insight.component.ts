import { Component, OnInit } from '@angular/core';
import { BarsService } from '../bars.service';

declare const Highcharts: any;

@Component({
  selector: 'app-insight',
  templateUrl: './insight.component.html',
  styleUrls: ['./insight.component.css']
})
export class InsightComponent implements OnInit {

  constructor(private barService: BarsService) {
    this.barService.getFrequentCounts().subscribe(
      data => {
        console.log(data);

        const drinkers = [];
        const counts = [];

        data.forEach(drinker => {
          drinkers.push(drinker.Drinker_Name);
          counts.push(drinker.frequentCount);
        });

        this.renderChart(drinkers, counts);
      }
    );
  }

  ngOnInit() {
  }

  renderChart(drinkers: string[], counts: number[]) {
    Highcharts.chart('bargraph', {
      chart: {
        type: 'column'
      },
      title: {
        text: 'Top 20 Least Spenders'
      },
      xAxis: {
        categories: drinkers,
        title: {
          text: 'Drinkers'
        }
      },
      yAxis: {
        min: 0,
        title: {
          text: 'Money Spent'
        },
        labels: {
          overflow: 'justify'
        }
      },
      plotOptions: {
        bar: {
          dataLabels: {
            enabled: true
          }
        }
      },
      legend: {
        enabled: false
      },
      credits: {
        enabled: false
      },
      series: [{
        data: counts
      }]
    });
  }

}
