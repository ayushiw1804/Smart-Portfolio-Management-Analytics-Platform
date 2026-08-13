/* ==========================================================================
   AI-POWERED PORTFOLIO INTELLIGENCE PLATFORM - MAIN APP & SLICER CONTROLLER
   ========================================================================== */

const App = {
  currentFilters: {
    branch: 'All',
    rm: 'All',
    product: 'All',
    dateStart: '2024-04-01',
    dateEnd: '2025-03-31'
  },

  init: function() {
    this.bindSlicers();
    this.bindNavigation();
    this.bindModals();
    this.renderAllVisuals();

    // Initialize Big Data Stream Simulator
    PipelineStream.init();
    PipelineStream.subscribe((data) => this.updateStreamLogConsole(data));

    // Initialize AI Copilot
    AICopilot.init();

    console.log('Portfolio Intelligence Platform initialized successfully.');
  },

  // Slicer Filter Handling
  bindSlicers: function() {
    const branchSel = document.getElementById('slicer-branch');
    const rmSel = document.getElementById('slicer-rm');
    const prodSel = document.getElementById('slicer-product');
    const clearBtn = document.getElementById('btn-clear-slicers');

    if (branchSel) {
      branchSel.addEventListener('change', (e) => {
        this.currentFilters.branch = e.target.value;
        this.applySlicerFilters();
      });
    }

    if (rmSel) {
      rmSel.addEventListener('change', (e) => {
        this.currentFilters.rm = e.target.value;
        this.applySlicerFilters();
      });
    }

    if (prodSel) {
      prodSel.addEventListener('change', (e) => {
        this.currentFilters.product = e.target.value;
        this.applySlicerFilters();
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        if (branchSel) branchSel.value = 'All';
        if (rmSel) rmSel.value = 'All';
        if (prodSel) prodSel.value = 'All';
        this.currentFilters = { branch: 'All', rm: 'All', product: 'All', dateStart: '2024-04-01', dateEnd: '2025-03-31' };
        this.applySlicerFilters();
      });
    }
  },

  applySlicerFilters: function() {
    // Dynamically calculate multipliers based on active slicers
    let multiplier = 1.0;
    if (this.currentFilters.branch !== 'All') multiplier *= 0.28;
    if (this.currentFilters.rm !== 'All') multiplier *= 0.22;
    if (this.currentFilters.product !== 'All') multiplier *= 0.32;

    // Update KPI Card Displays
    const base = PORTFOLIO_DATA.baselineKPIs;
    document.getElementById('kpi-total-cust').innerText = Math.round(base.totalCustomers * multiplier).toLocaleString();
    
    const calculatedAUM = base.totalAUM * multiplier;
    document.getElementById('kpi-aum').innerText = '₹ ' + (calculatedAUM >= 100000000 ? (calculatedAUM / 10000000).toFixed(2) + ' Cr' : Math.round(calculatedAUM).toLocaleString('en-IN'));

    const calculatedRev = base.revenueGenerated * multiplier;
    document.getElementById('kpi-revenue').innerText = '₹ ' + (calculatedRev / 10000000).toFixed(2) + ' Cr';

    document.getElementById('kpi-high-risk').innerText = Math.round(base.highRiskCustomers * multiplier).toLocaleString();
    document.getElementById('kpi-calls-due').innerText = Math.round(base.callsDueToday * multiplier).toLocaleString();

    // Re-render visual charts with sliced data
    this.renderAllVisuals(multiplier);
  },

  renderAllVisuals: function(multiplier = 1.0) {
    // 1. Monthly Revenue Trend
    const slicedRevTrend = PORTFOLIO_DATA.monthlyRevenueTrend.map(d => ({
      month: d.month,
      rev: Number((d.rev * multiplier).toFixed(2))
    }));
    ChartEngine.renderRevenueTrend('chart-revenue-trend', slicedRevTrend);

    // 2. Product Distribution
    ChartEngine.renderProductDistribution('chart-product-dist', PORTFOLIO_DATA.productDistribution);

    // 3. RM Performance
    const slicedRM = PORTFOLIO_DATA.rmPerformance.map(d => ({
      rm: d.rm,
      revenue: Number((d.revenue * (this.currentFilters.rm === 'All' ? 1 : (d.rm === this.currentFilters.rm ? 1 : 0.1))).toFixed(2))
    }));
    ChartEngine.renderRMPerformance('chart-rm-perf', slicedRM);

    // 4. Risk Distribution
    ChartEngine.renderRiskDistribution('chart-risk-dist', PORTFOLIO_DATA.riskDistribution);

    // 5. Churn Rate Trend
    ChartEngine.renderChurnTrend('chart-churn-trend', PORTFOLIO_DATA.churnTrend);

    // 6. Efficient Frontier ML Chart
    const opt = MLEngine.optimizePortfolio(0.5, 10000000);
    ChartEngine.renderEfficientFrontier('chart-efficient-frontier', opt.frontierPoints);

    // Render Tables
    this.renderHighRiskTable();
    this.renderCallPrioritiesTable();
  },

  renderHighRiskTable: function() {
    const tbody = document.getElementById('table-high-risk-body');
    if (!tbody) return;

    let filtered = PORTFOLIO_DATA.topHighRiskCustomers;
    if (this.currentFilters.rm !== 'All') {
      filtered = filtered.filter(c => c.rm === this.currentFilters.rm);
    }
    if (this.currentFilters.branch !== 'All') {
      filtered = filtered.filter(c => c.branch === this.currentFilters.branch);
    }
    if (this.currentFilters.product !== 'All') {
      filtered = filtered.filter(c => c.product === this.currentFilters.product);
    }

    if (filtered.length === 0) filtered = PORTFOLIO_DATA.topHighRiskCustomers.slice(0, 5);

    tbody.innerHTML = filtered.map(c => `
      <tr>
        <td><strong>${c.name}</strong></td>
        <td>${c.aum}</td>
        <td><span class="badge-score risk-critical">${c.riskScore}</span></td>
        <td><strong style="color:#ef4444;">${c.pd}</strong></td>
        <td><button class="btn-action-sm" onclick="App.openCustomerModal('${c.id}')">View 360°</button></td>
      </tr>
    `).join('');
  },

  renderCallPrioritiesTable: function() {
    const tbody = document.getElementById('table-call-priorities-body');
    if (!tbody) return;

    tbody.innerHTML = PORTFOLIO_DATA.callPriorities.map(c => `
      <tr>
        <td><strong>${c.customer}</strong></td>
        <td>
          <span class="priority-tag ${c.priority.toLowerCase()}">
            <i class="fas ${c.icon}"></i> ${c.priority}
          </span>
        </td>
        <td>${c.reason}</td>
        <td>${c.aum}</td>
        <td><span class="badge-score ${c.riskScore > 80 ? 'risk-critical' : (c.riskScore > 50 ? 'risk-high' : 'risk-low')}">${c.riskScore}</span></td>
        <td>${c.lastContact}</td>
        <td><button class="btn-action-sm" onclick="alert('Initiating call action for ${c.customer}...')">${c.action}</button></td>
      </tr>
    `).join('');
  },

  // Sidebar Tab Navigation
  bindNavigation: function() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const tabId = item.getAttribute('data-tab');
        if (tabId) this.switchTab(tabId);
      });
    });

    // Theme Toggle
    const themeBtn = document.getElementById('btn-theme-toggle');
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        document.body.classList.toggle('pbi-theme');
      });
    }

    // Copilot Drawer Toggle
    const copilotBtn = document.getElementById('btn-copilot-toggle');
    const copilotFloat = document.getElementById('copilot-floating-btn');
    const closeCopilot = document.getElementById('btn-close-copilot');

    if (copilotBtn) copilotBtn.addEventListener('click', () => this.toggleCopilot());
    if (copilotFloat) copilotFloat.addEventListener('click', () => this.toggleCopilot());
    if (closeCopilot) closeCopilot.addEventListener('click', () => this.toggleCopilot(false));
  },

  switchTab: function(tabId) {
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelectorAll('.view-container').forEach(v => v.classList.remove('active'));

    const activeNav = document.querySelector(`.nav-item[data-tab="${tabId}"]`);
    const activeView = document.getElementById(tabId);

    if (activeNav) activeNav.classList.add('active');
    if (activeView) activeView.classList.add('active');
  },

  toggleCopilot: function(forceState) {
    const drawer = document.getElementById('copilot-drawer');
    if (!drawer) return;
    if (typeof forceState === 'boolean') {
      drawer.classList.toggle('open', forceState);
    } else {
      drawer.classList.toggle('open');
    }
  },

  updateStreamLogConsole: function(data) {
    const consoleEl = document.getElementById('pipeline-console-body');
    const recordsEl = document.getElementById('stream-records-count');
    const rateEl = document.getElementById('stream-rate-val');
    const latencyEl = document.getElementById('stream-latency-val');

    if (recordsEl) recordsEl.innerText = data.totalRecords.toLocaleString();
    if (rateEl) rateEl.innerText = data.rate + ' req/s';
    if (latencyEl) latencyEl.innerText = data.latency + ' ms';

    if (!consoleEl) return;

    const lineDiv = document.createElement('div');
    lineDiv.className = 'log-line';
    lineDiv.innerHTML = `
      <span class="log-time">[${data.timestamp}]</span>
      <span class="log-topic">[${data.topic}]</span>
      <span class="${data.isAlert ? 'log-alert' : 'log-msg'}">${data.message}</span>
    `;

    consoleEl.appendChild(lineDiv);
    if (consoleEl.children.length > 50) consoleEl.removeChild(consoleEl.firstChild);
    consoleEl.scrollTop = consoleEl.scrollHeight;
  },

  bindModals: function() {
    const closeBtn = document.getElementById('btn-close-modal');
    const backdrop = document.getElementById('modal-backdrop');
    if (closeBtn) closeBtn.addEventListener('click', () => this.closeModal());
    if (backdrop) backdrop.addEventListener('click', () => this.closeModal());
  },

  openCustomerModal: function(custId) {
    const modal = document.getElementById('customer-modal');
    const backdrop = document.getElementById('modal-backdrop');
    const content = document.getElementById('customer-modal-content');

    const customer = PORTFOLIO_DATA.topHighRiskCustomers.find(c => c.id === custId) || PORTFOLIO_DATA.topHighRiskCustomers[0];
    const riskModel = MLEngine.calculateCustomerRisk(customer);

    if (content) {
      content.innerHTML = `
        <h3 style="font-family: var(--font-heading); font-size: 1.3rem; margin-bottom: 12px;">Customer 360° Profile - ${customer.name} (${customer.id})</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
          <div style="background: rgba(255,255,255,0.04); padding: 12px; border-radius: 8px;">
            <p style="color: var(--text-muted); font-size: 0.8rem;">Relationship Manager</p>
            <p style="font-weight: 700; font-size: 1rem;">${customer.rm} (${customer.branch})</p>
          </div>
          <div style="background: rgba(255,255,255,0.04); padding: 12px; border-radius: 8px;">
            <p style="color: var(--text-muted); font-size: 0.8rem;">Portfolio Value (AUM)</p>
            <p style="font-weight: 700; font-size: 1rem; color: #10b981;">${customer.aum}</p>
          </div>
        </div>
        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); padding: 14px; border-radius: 8px; margin-bottom: 16px;">
          <h4 style="color: #ef4444; font-size: 0.95rem; margin-bottom: 4px;"><i class="fas fa-exclamation-triangle"></i> ML Default Risk Assessment</h4>
          <p style="font-size: 0.85rem;">Calculated Probability of Default (PD): <strong>${riskModel.probDefaultPct}</strong> | Risk Score: <strong>${riskModel.riskScore}/100</strong></p>
          <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 4px;">Primary Risk Driver: High revolving credit utilization & no contact for ${customer.lastContact}.</p>
        </div>
        <button class="btn-copilot-trigger" style="width: 100%; justify-content: center;" onclick="App.closeModal(); AICopilot.handleSendMessage('Draft retention script for ${customer.name}')">
          <i class="fas fa-brain"></i> Ask AI Copilot to Draft Retention Action Plan
        </button>
      `;
    }

    if (modal) modal.style.display = 'block';
    if (backdrop) backdrop.style.display = 'block';
  },

  closeModal: function() {
    const modal = document.getElementById('customer-modal');
    const backdrop = document.getElementById('modal-backdrop');
    if (modal) modal.style.display = 'none';
    if (backdrop) backdrop.style.display = 'none';
  }
};

document.addEventListener('DOMContentLoaded', () => App.init());
