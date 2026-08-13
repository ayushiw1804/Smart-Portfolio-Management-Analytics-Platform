/* ==========================================================================
   BIG DATA STREAMING INGESTION ENGINE (KAFKA / SPARK EVENT EMULATOR)
   ========================================================================== */

const PipelineStream = {
  isRunning: true,
  recordsIngested: 4892040,
  currentRate: 1420, // records per second
  latencyMs: 14,
  qualityScore: 99.8,
  subscribers: [],
  timerId: null,

  topics: [
    'market.stock_ticks',
    'customer.transactions',
    'portfolio.balance_updates',
    'credit.risk_signals',
    'pipeline.telemetry'
  ],

  sampleSymbols: ['HDFCBANK', 'RELIANCE', 'INFY', 'TCS', 'ICICIBANK', 'SBIN', 'BHARTIARTL'],

  init: function() {
    this.startStreaming();
  },

  startStreaming: function() {
    if (this.timerId) clearInterval(this.timerId);
    this.isRunning = true;

    this.timerId = setInterval(() => {
      if (!this.isRunning) return;

      this.recordsIngested += Math.floor(Math.random() * 25) + 10;
      this.latencyMs = Math.floor(12 + Math.random() * 6);

      const randomTopic = this.topics[Math.floor(Math.random() * this.topics.length)];
      const eventMsg = this.generateEventLog(randomTopic);

      this.notifySubscribers({
        timestamp: new Date().toISOString().split('T')[1].slice(0, 12),
        topic: randomTopic,
        message: eventMsg.msg,
        isAlert: eventMsg.isAlert,
        totalRecords: this.recordsIngested,
        rate: this.currentRate + Math.floor(Math.random() * 60 - 30),
        latency: this.latencyMs
      });
    }, 1200);
  },

  pauseStreaming: function() {
    this.isRunning = false;
  },

  generateEventLog: function(topic) {
    let msg = '';
    let isAlert = false;

    if (topic === 'market.stock_ticks') {
      const sym = this.sampleSymbols[Math.floor(Math.random() * this.sampleSymbols.length)];
      const price = (500 + Math.random() * 2000).toFixed(2);
      const change = (Math.random() * 3 - 1.5).toFixed(2);
      msg = `TICK: ${sym} price=₹${price} (${change > 0 ? '+' : ''}${change}%) vol=${Math.floor(Math.random() * 5000 + 100)}`;
    } else if (topic === 'customer.transactions') {
      const custId = 'CUST-' + Math.floor(100 + Math.random() * 50);
      const amt = Math.floor(Math.random() * 450000 + 5000);
      msg = `TX_EVENT: ${custId} deposited ₹${amt.toLocaleString('en-IN')} channel=UPI status=SUCCESS`;
    } else if (topic === 'portfolio.balance_updates') {
      const rm = 'RM ' + String.fromCharCode(65 + Math.floor(Math.random() * 5));
      msg = `AUM_SYNC: ${rm} portfolio balance re-indexed (+₹${Math.floor(Math.random() * 120 + 20)}k AUM delta)`;
    } else if (topic === 'credit.risk_signals') {
      const custId = 'CUST-' + Math.floor(101 + Math.random() * 10);
      isAlert = true;
      msg = `ALERT: High risk delta detected for ${custId} - PD increased by +2.4% due to credit utilization spikes`;
    } else {
      msg = `TELEMETRY: Spark Streaming worker-node-#${Math.floor(Math.random()*4+1)} healthy (CPU 18%, Mem 42%)`;
    }

    return { msg: msg, isAlert: isAlert };
  },

  subscribe: function(callback) {
    this.subscribers.push(callback);
  },

  notifySubscribers: function(data) {
    this.subscribers.forEach(cb => cb(data));
  }
};
