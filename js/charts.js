/* ==========================================================================
   POWER BI & ML CHART RENDERING SYSTEM (CHART.JS & CANVAS VISUALS)
   ========================================================================== */

const ChartEngine = {
  instances: {},

  // 1. Revenue Trend Line Chart (Apr 2024 - Mar 2025)
  renderRevenueTrend: function(canvasId, dataPoints) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    if (this.instances[canvasId]) {
      this.instances[canvasId].destroy();
    }

    const labels = dataPoints.map(d => d.month);
    const values = dataPoints.map(d => d.rev);

    this.instances[canvasId] = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Revenue (₹ Millions)',
          data: values,
          borderColor: '#2563eb',
          backgroundColor: 'rgba(37, 99, 235, 0.12)',
          borderWidth: 3,
          tension: 0.35,
          fill: true,
          pointBackgroundColor: '#2563eb',
          pointBorderColor: '#ffffff',
          pointRadius: 5,
          pointHoverRadius: 7
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => ` Revenue: ₹${context.raw}M`
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#94a3b8', font: { size: 11 } }
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: {
              color: '#94a3b8',
              font: { size: 11 },
              callback: (val) => '₹' + val + 'M'
            },
            min: 0,
            max: 6
          }
        }
      }
    });
  },

  // 2. Portfolio Distribution Donut Chart
  renderProductDistribution: function(canvasId, dataPoints) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    if (this.instances[canvasId]) {
      this.instances[canvasId].destroy();
    }

    const labels = dataPoints.map(d => d.product);
    const values = dataPoints.map(d => d.pct);
    const colors = dataPoints.map(d => d.color);

    this.instances[canvasId] = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: values,
          backgroundColor: colors,
          borderColor: '#0f172a',
          borderWidth: 3,
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        plugins: {
          legend: {
            position: 'right',
            labels: {
              color: '#cbd5e1',
              font: { size: 11 },
              usePointStyle: true,
              padding: 12
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => ` ${context.label}: ${context.raw}%`
            }
          }
        }
      }
    });
  },

  // 3. RM Performance Revenue Bar Chart
  renderRMPerformance: function(canvasId, dataPoints) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    if (this.instances[canvasId]) {
      this.instances[canvasId].destroy();
    }

    const labels = dataPoints.map(d => d.rm);
    const values = dataPoints.map(d => d.revenue);
    const barColors = ['#2563eb', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4'];

    this.instances[canvasId] = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Revenue (₹ Millions)',
          data: values,
          backgroundColor: barColors,
          borderRadius: 6,
          barThickness: 32
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => ` Revenue: ₹${context.raw}M`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: '#94a3b8', font: { size: 11, weight: 'bold' } }
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: {
              color: '#94a3b8',
              font: { size: 11 },
              callback: (val) => val + 'M'
            },
            min: 0,
            max: 10
          }
        }
      }
    });
  },

  // 4. Risk Distribution Donut Chart
  renderRiskDistribution: function(canvasId, dataPoints) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    if (this.instances[canvasId]) {
      this.instances[canvasId].destroy();
    }

    const labels = dataPoints.map(d => `${d.category} (${d.count.toLocaleString()})`);
    const values = dataPoints.map(d => d.pct);
    const colors = dataPoints.map(d => d.color);

    this.instances[canvasId] = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: values,
          backgroundColor: colors,
          borderColor: '#0f172a',
          borderWidth: 3,
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '68%',
        plugins: {
          legend: {
            position: 'right',
            labels: {
              color: '#cbd5e1',
              font: { size: 11 },
              usePointStyle: true,
              padding: 12
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => ` ${context.label}: ${context.raw}%`
            }
          }
        }
      }
    });
  },

  // 5. Churn Rate Trend Line Chart
  renderChurnTrend: function(canvasId, dataPoints) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    if (this.instances[canvasId]) {
      this.instances[canvasId].destroy();
    }

    const labels = dataPoints.map(d => d.month);
    const values = dataPoints.map(d => d.rate);

    this.instances[canvasId] = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Churn Rate (%)',
          data: values,
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          borderWidth: 3,
          tension: 0.3,
          fill: true,
          pointBackgroundColor: '#ef4444',
          pointRadius: 5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => ` Churn Rate: ${context.raw}%`
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#94a3b8', font: { size: 11 } }
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: {
              color: '#94a3b8',
              font: { size: 11 },
              callback: (val) => val + '%'
            },
            min: 0,
            max: 10
          }
        }
      }
    });
  },

  // 6. Efficient Frontier Scatter Chart
  renderEfficientFrontier: function(canvasId, scatterPoints) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    if (this.instances[canvasId]) {
      this.instances[canvasId].destroy();
    }

    this.instances[canvasId] = new Chart(ctx, {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: 'Efficient Frontier',
            data: scatterPoints,
            showLine: true,
            borderColor: '#38bdf8',
            backgroundColor: 'rgba(56, 189, 248, 0.2)',
            borderWidth: 3,
            pointRadius: 6,
            pointBackgroundColor: '#38bdf8'
          },
          {
            label: 'Optimal Portfolio',
            data: [{ x: 11.2, y: 14.8 }],
            borderColor: '#f59e0b',
            backgroundColor: '#f59e0b',
            pointRadius: 10,
            pointStyle: 'star'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#cbd5e1' } }
        },
        scales: {
          x: {
            title: { display: true, text: 'Portfolio Risk (Volatility %)', color: '#94a3b8' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#94a3b8' }
          },
          y: {
            title: { display: true, text: 'Expected Return (%)', color: '#94a3b8' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#94a3b8' }
          }
        }
      }
    });
  }
};
