/* ==========================================================================
   AI COPILOT AGENT & INTELLIGENCE COMMAND CENTER
   ========================================================================== */

const AICopilot = {
  init: function() {
    this.bindEvents();
  },

  bindEvents: function() {
    const sendBtn = document.getElementById('btn-send-chat');
    const chatInput = document.getElementById('chat-input');
    const suggestions = document.querySelectorAll('.chip-suggestion');

    if (sendBtn && chatInput) {
      sendBtn.addEventListener('click', () => this.handleSendMessage());
      chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') this.handleSendMessage();
      });
    }

    suggestions.forEach(chip => {
      chip.addEventListener('click', (e) => {
        const text = e.target.innerText;
        if (chatInput) chatInput.value = text;
        this.handleSendMessage();
      });
    });
  },

  handleSendMessage: function() {
    const input = document.getElementById('chat-input');
    if (!input || !input.value.trim()) return;

    const userMsg = input.value.trim();
    this.appendMessage('user', userMsg);
    input.value = '';

    // Show typing status indicator
    this.appendTypingIndicator();

    setTimeout(() => {
      this.removeTypingIndicator();
      const response = this.generateAIResponse(userMsg);
      this.appendMessage('system', response.html);
    }, 900);
  },

  appendMessage: function(sender, contentHtml) {
    const body = document.getElementById('copilot-messages');
    if (!body) return;

    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message ${sender}`;

    msgDiv.innerHTML = `
      <div class="chat-bubble">${contentHtml}</div>
      <div class="chat-meta">${sender === 'user' ? 'You' : 'AI Copilot'} • ${timeStr}</div>
    `;

    body.appendChild(msgDiv);
    body.scrollTop = body.scrollHeight;
  },

  appendTypingIndicator: function() {
    const body = document.getElementById('copilot-messages');
    if (!body) return;

    const typingDiv = document.createElement('div');
    typingDiv.id = 'copilot-typing';
    typingDiv.className = 'chat-message system';
    typingDiv.innerHTML = `<div class="chat-bubble" style="color: #94a3b8; font-style: italic;"><i class="fas fa-circle-notch fa-spin"></i> AI Copilot is analyzing portfolio data...</div>`;
    body.appendChild(typingDiv);
    body.scrollTop = body.scrollHeight;
  },

  removeTypingIndicator: function() {
    const el = document.getElementById('copilot-typing');
    if (el) el.remove();
  },

  generateAIResponse: function(query) {
    const lower = query.toLowerCase();

    if (lower.includes('top performer') || lower.includes('rm performance') || lower.includes('best rm')) {
      return {
        html: `
          <strong>📊 Relationship Manager Performance Insights:</strong><br>
          • <strong>RM A (Anand Sharma)</strong> leads with <strong>₹9.8M</strong> in revenue across 2,840 customers (Branch: North Branch).<br>
          • <strong>RM B (Bhavna Patel)</strong> is #2 with <strong>₹7.6M</strong>.<br>
          • <em>Recommendation:</em> Cross-pollinate Mutual Fund cross-selling strategies from RM A to RM D & E.
        `
      };
    } else if (lower.includes('amit verma') || lower.includes('optimize')) {
      const opt = MLEngine.optimizePortfolio(0.6, 2845000);
      return {
        html: `
          <strong>🧠 ML Portfolio Optimization for Amit Verma (₹28.45 Lakhs):</strong><br>
          Target Risk-Adjusted Allocation:<br>
          • Home Loans: <strong>${opt.weights[0].weight}%</strong> (₹${opt.weights[0].allocationValue.toLocaleString('en-IN')})<br>
          • Mutual Funds: <strong>${opt.weights[1].weight}%</strong> (₹${opt.weights[1].allocationValue.toLocaleString('en-IN')})<br>
          • Govt Bonds: <strong>${opt.weights[3].weight}%</strong> (₹${opt.weights[3].allocationValue.toLocaleString('en-IN')})<br>
          Expected Portfolio Return: <strong>${opt.expectedReturnPct}%</strong> | Sharpe Ratio: <strong>${opt.sharpeRatio}</strong><br>
          <button class="btn-action-sm" style="margin-top:6px;" onclick="App.switchTab('optimization-tab')">Open ML Optimizer Canvas</button>
        `
      };
    } else if (lower.includes('forecast') || lower.includes('q3') || lower.includes('revenue forecast')) {
      return {
        html: `
          <strong>📈 Revenue Forecasting Engine (Holt-Winters ML):</strong><br>
          • Q1 2025 Projected Revenue: <strong>₹5.3M / mo</strong><br>
          • Q2 2025 Projected Revenue: <strong>₹5.75M / mo</strong> (95% CI: ₹5.4M - ₹6.1M)<br>
          • Q3 2025 Projected Revenue: <strong>₹6.20M / mo</strong><br>
          Monthly churn rate is expected to drop further from <strong>6.85% to 5.9%</strong> by Q3.
        `
      };
    } else if (lower.includes('high risk') || lower.includes('call') || lower.includes('rahul mehta')) {
      return {
        html: `
          <strong>🚨 Action Priority: Top High-Risk Account</strong><br>
          Customer: <strong>Rahul Mehta</strong> (AUM: ₹22.50 Lakhs | Risk Score: 91 | PD: 89%)<br>
          Reason: <em>High Risk & No Contact for 45 Days</em><br>
          Suggested Script: "Good morning Mr. Mehta, calling from your Wealth Desk to review your portfolio risk exposure and discuss tax-saver SIP options..."<br>
          <button class="btn-action-sm" style="margin-top:6px;" onclick="App.openCustomerModal('CUST-101')">View Customer 360 Profile</button>
        `
      };
    } else if (lower.includes('stress test') || lower.includes('rate hike')) {
      const stress = MLEngine.runStressTest(200, -15);
      return {
        html: `
          <strong>🛡️ Macro Stress Test Result (+200bps Rate Hike & -15% Equity Drop):</strong><br>
          • Baseline AUM: ₹182.45 Cr → Stressed AUM: <strong>₹${(stress.stressedAUM / 10000000).toFixed(2)} Cr</strong> (${stress.aumDeltaPct})<br>
          • Annualized Revenue Impact: <strong>-₹${Math.abs(Math.round(stress.revDelta / 100000))} Lakhs</strong><br>
          <button class="btn-action-sm" style="margin-top:6px;" onclick="App.switchTab('risk-tab')">Open Risk Analytics View</button>
        `
      };
    } else {
      return {
        html: `
          I have analyzed your query across real-time transaction logs and portfolio models.<br>
          • Total Portfolio AUM: <strong>₹1,82,45,70,000</strong><br>
          • Active High Risk Accounts: <strong>482 customers</strong><br>
          You can ask me to optimize client portfolios, forecast quarterly revenues, run stress tests, or generate call scripts for RMs!
        `
      };
    }
  }
};
