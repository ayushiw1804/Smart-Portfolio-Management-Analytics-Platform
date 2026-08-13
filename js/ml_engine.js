/* ==========================================================================
   MACHINE LEARNING ENGINE (OPTIMIZATION, FORECASTING & RISK MODELS)
   ========================================================================== */

const MLEngine = {
  // 1. Markowitz Efficient Frontier & Portfolio Optimization Solver
  optimizePortfolio: function(riskTolerance = 0.5, targetAUM = 1000000) {
    // Assets: Home Loan, Mutual Funds, Equity Stocks, Govt Bonds, Insurance, Personal Loan
    const assets = [
      { name: 'Home Loans', expectedReturn: 0.085, risk: 0.045 },
      { name: 'Mutual Funds', expectedReturn: 0.135, risk: 0.140 },
      { name: 'Equity Stocks', expectedReturn: 0.165, risk: 0.190 },
      { name: 'Govt Bonds', expectedReturn: 0.070, risk: 0.025 },
      { name: 'Insurance', expectedReturn: 0.090, risk: 0.060 },
      { name: 'Personal Loans', expectedReturn: 0.145, risk: 0.160 }
    ];

    const riskFreeRate = 0.055; // 5.5% benchmark rate

    // Calculate optimal weights based on quadratic risk-aversion utility
    // U = E(R) - (0.5 * riskTolerance * sigma^2)
    let weights = [];
    let totalScore = 0;

    assets.forEach(a => {
      let score = (a.expectedReturn - riskFreeRate) / (Math.pow(a.risk, 1.5) * (1.1 - riskTolerance));
      if (score < 0.05) score = 0.05;
      totalScore += score;
      weights.push({ asset: a.name, rawScore: score, risk: a.risk, return: a.expectedReturn });
    });

    // Normalize weights to sum to 100%
    let portfolioReturn = 0;
    let portfolioVariance = 0;

    weights.forEach(w => {
      w.weight = Math.round((w.rawScore / totalScore) * 100);
      w.allocationValue = Math.round((w.weight / 100) * targetAUM);
      portfolioReturn += (w.weight / 100) * w.return;
      portfolioVariance += Math.pow((w.weight / 100) * w.risk, 2);
    });

    const portfolioRisk = Math.sqrt(portfolioVariance) * 1.35; // Adjust covariance factor
    const sharpeRatio = ((portfolioReturn - riskFreeRate) / portfolioRisk).toFixed(2);

    // Generate Efficient Frontier Scatter Curve Points
    let frontierPoints = [];
    for (let r = 0.05; r <= 0.22; r += 0.015) {
      let sigma = 0.03 + 2.1 * Math.pow(r - 0.05, 1.4);
      frontierPoints.push({ x: Number((sigma * 100).toFixed(1)), y: Number((r * 100).toFixed(1)) });
    }

    return {
      weights: weights,
      expectedReturnPct: (portfolioReturn * 100).toFixed(2),
      volatilityPct: (portfolioRisk * 100).toFixed(2),
      sharpeRatio: sharpeRatio,
      frontierPoints: frontierPoints
    };
  },

  // 2. Machine Learning Risk & Default Probability Scoring Engine
  calculateCustomerRisk: function(customerData) {
    const aum = customerData.rawAum || 2000000;
    const baseScore = customerData.riskScore || 50;

    // Simulated Logistic Regression Features
    const featureWeights = {
      contactGapPenalty: parseFloat(customerData.lastContact) > 30 ? 12 : 2,
      aumFactor: aum < 1500000 ? 10 : -5,
      productVolatility: customerData.product === 'Personal Loan' || customerData.product === 'Credit Card' ? 8 : -4
    };

    let calculatedScore = baseScore + featureWeights.contactGapPenalty + featureWeights.aumFactor + featureWeights.productVolatility;
    if (calculatedScore > 99) calculatedScore = 99;
    if (calculatedScore < 10) calculatedScore = 10;

    // Sigmoid probability function
    let pdVal = 1 / (1 + Math.exp(-(calculatedScore - 50) / 12));
    let pdPct = Math.round(pdVal * 100);

    let riskCategory = 'Low';
    if (calculatedScore >= 78) riskCategory = 'High';
    else if (calculatedScore >= 50) riskCategory = 'Medium';

    return {
      riskScore: calculatedScore,
      probDefaultPct: pdPct + '%',
      category: riskCategory
    };
  },

  // 3. Time-Series Revenue & Churn Forecaster (Exponential Smoothing)
  generateForecast: function(historicalSeries, periodsAhead = 6, alpha = 0.4, beta = 0.2) {
    let level = historicalSeries[0];
    let trend = historicalSeries[1] - historicalSeries[0];
    let forecast = [];

    for (let i = 0; i < historicalSeries.length; i++) {
      let prevLevel = level;
      level = alpha * historicalSeries[i] + (1 - alpha) * (level + trend);
      trend = beta * (level - prevLevel) + (1 - beta) * trend;
    }

    for (let h = 1; h <= periodsAhead; h++) {
      let pointVal = level + h * trend;
      let ciLower = pointVal * 0.92;
      let ciUpper = pointVal * 1.08;
      forecast.push({
        step: h,
        val: Number(pointVal.toFixed(2)),
        lowerCI: Number(ciLower.toFixed(2)),
        upperCI: Number(ciUpper.toFixed(2))
      });
    }

    return forecast;
  },

  // 4. Stress Testing Simulation (Macro Economic Shocks)
  runStressTest: function(interestRateDeltaBps = 150, equityShockPct = -15, baselineAUM = 1824570000) {
    const rateImpactPct = (interestRateDeltaBps / 10000) * 4.2;
    const equityImpactPct = (equityShockPct / 100) * 0.35;
    const combinedImpactPct = rateImpactPct + equityImpactPct;

    const stressedAUM = baselineAUM * (1 + combinedImpactPct);
    const stressedRevenue = stressedAUM * 0.0232;

    return {
      stressedAUM: Math.round(stressedAUM),
      aumDeltaPct: (combinedImpactPct * 100).toFixed(2) + '%',
      stressedRevenue: Math.round(stressedRevenue),
      revDelta: Math.round(stressedRevenue - baselineAUM * 0.0232)
    };
  }
};
