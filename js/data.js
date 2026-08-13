/* ==========================================================================
   AI-POWERED PORTFOLIO INTELLIGENCE PLATFORM - DATASET ENGINE
   ========================================================================== */

const PORTFOLIO_DATA = {
  baselineKPIs: {
    totalCustomers: 12568,
    totalAUM: 1824570000, // ₹ 1,82,45,70,000
    revenueGenerated: 423725000, // ₹ 42,37,25,000
    highRiskCustomers: 482,
    churnRate: 6.85,
    callsDueToday: 128
  },

  monthlyRevenueTrend: [
    { month: 'Apr 2024', rev: 2.8, formatted: '₹2.8M' },
    { month: 'May 2024', rev: 3.1, formatted: '₹3.1M' },
    { month: 'Jun 2024', rev: 2.9, formatted: '₹2.9M' },
    { month: 'Jul 2024', rev: 3.4, formatted: '₹3.4M' },
    { month: 'Aug 2024', rev: 3.6, formatted: '₹3.6M' },
    { month: 'Sep 2024', rev: 4.1, formatted: '₹4.1M' },
    { month: 'Oct 2024', rev: 3.9, formatted: '₹3.9M' },
    { month: 'Nov 2024', rev: 4.3, formatted: '₹4.3M' },
    { month: 'Dec 2024', rev: 4.6, formatted: '₹4.6M' },
    { month: 'Jan 2025', rev: 4.8, formatted: '₹4.8M' },
    { month: 'Feb 2025', rev: 5.1, formatted: '₹5.1M' },
    { month: 'Mar 2025', rev: 5.3, formatted: '₹5.3M' }
  ],

  productDistribution: [
    { product: 'Home Loan', pct: 35, color: '#2563eb', aum: '₹ 63.86 Cr' },
    { product: 'Credit Card', pct: 20, color: '#10b981', aum: '₹ 36.49 Cr' },
    { product: 'Mutual Funds', pct: 18, color: '#f59e0b', aum: '₹ 32.84 Cr' },
    { product: 'Insurance', pct: 15, color: '#8b5cf6', aum: '₹ 27.37 Cr' },
    { product: 'Personal Loan', pct: 12, color: '#06b6d4', aum: '₹ 21.89 Cr' }
  ],

  loanPipeline: [
    { stage: 'Leads', count: 2100, pct: '100%', class: 'leads' },
    { stage: 'Application', count: 1600, pct: '76.2%', class: 'application' },
    { stage: 'Verification', count: 1200, pct: '57.1%', class: 'verification' },
    { stage: 'Approved', count: 980, pct: '46.6%', class: 'approved' },
    { stage: 'Disbursed', count: 850, pct: '40.5%', class: 'disbursed' }
  ],

  rmPerformance: [
    { rm: 'RM A', name: 'Anand Sharma', revenue: 9.8, branch: 'North Branch', customers: 2840, aum: '₹ 42.5 Cr' },
    { rm: 'RM B', name: 'Bhavna Patel', revenue: 7.6, branch: 'South Branch', customers: 2410, aum: '₹ 36.8 Cr' },
    { rm: 'RM C', name: 'Chetan Verma', revenue: 6.4, branch: 'West Branch',  customers: 2150, aum: '₹ 31.2 Cr' },
    { rm: 'RM D', name: 'Deepak Reddy', revenue: 4.9, branch: 'East Branch',  customers: 1890, aum: '₹ 24.5 Cr' },
    { rm: 'RM E', name: 'Esha Gupta',   revenue: 3.7, branch: 'North Branch', customers: 1460, aum: '₹ 18.2 Cr' }
  ],

  riskDistribution: [
    { category: 'High Risk', count: 482, pct: 8.7, color: '#ef4444' },
    { category: 'Medium Risk', count: 2216, pct: 17.6, color: '#f59e0b' },
    { category: 'Low Risk', count: 9870, pct: 73.7, color: '#10b981' }
  ],

  topHighRiskCustomers: [
    { id: 'CUST-101', name: 'Amit Verma',     aum: '₹ 28,45,000', rawAum: 2845000, riskScore: 92, pd: '89%', rm: 'RM A', branch: 'North Branch', product: 'Home Loan', lastContact: '45 Days Ago' },
    { id: 'CUST-102', name: 'Rajesh Kumar',   aum: '₹ 35,20,000', rawAum: 3520000, riskScore: 89, pd: '85%', rm: 'RM B', branch: 'South Branch', product: 'Personal Loan', lastContact: '38 Days Ago' },
    { id: 'CUST-103', name: 'Sunil Sharma',   aum: '₹ 22,10,000', rawAum: 2210000, riskScore: 88, pd: '83%', rm: 'RM A', branch: 'North Branch', product: 'Credit Card', lastContact: '30 Days Ago' },
    { id: 'CUST-104', name: 'Neha Singh',     aum: '₹ 18,75,000', rawAum: 1875000, riskScore: 86, pd: '80%', rm: 'RM C', branch: 'West Branch', product: 'Mutual Funds', lastContact: '28 Days Ago' },
    { id: 'CUST-105', name: 'Vikram Patel',   aum: '₹ 26,80,000', rawAum: 2680000, riskScore: 85, pd: '79%', rm: 'RM D', branch: 'East Branch', product: 'Insurance', lastContact: '25 Days Ago' },
    { id: 'CUST-106', name: 'Manoj Tiwari',   aum: '₹ 31,60,000', rawAum: 3160000, riskScore: 83, pd: '77%', rm: 'RM B', branch: 'South Branch', product: 'Home Loan', lastContact: '22 Days Ago' },
    { id: 'CUST-107', name: 'Pooja Mehta',    aum: '₹ 17,90,000', rawAum: 1790000, riskScore: 82, pd: '75%', rm: 'RM E', branch: 'North Branch', product: 'Personal Loan', lastContact: '20 Days Ago' },
    { id: 'CUST-108', name: 'Anil Gupta',     aum: '₹ 19,40,000', rawAum: 1940000, riskScore: 81, pd: '74%', rm: 'RM C', branch: 'West Branch', product: 'Mutual Funds', lastContact: '19 Days Ago' },
    { id: 'CUST-109', name: 'Rohit Agarwal',  aum: '₹ 16,30,000', rawAum: 1630000, riskScore: 80, pd: '72%', rm: 'RM A', branch: 'North Branch', product: 'Credit Card', lastContact: '15 Days Ago' },
    { id: 'CUST-110', name: 'Karan Malhotra', aum: '₹ 15,20,000', rawAum: 1520000, riskScore: 79, pd: '70%', rm: 'RM D', branch: 'East Branch', product: 'Insurance', lastContact: '14 Days Ago' }
  ],

  callPriorities: [
    { customer: 'Rahul Mehta', priority: 'High', icon: 'fa-arrow-up', reason: 'High Risk & No Contact for 45 Days', aum: '₹ 22,50,000', riskScore: 91, lastContact: '45 Days Ago', action: 'Call Today', rm: 'RM A' },
    { customer: 'Sneha Kapoor', priority: 'High', icon: 'fa-arrow-up', reason: 'Loan Renewal Due in 7 Days', aum: '₹ 18,20,000', riskScore: 68, lastContact: '2 Days Ago', action: 'Discuss Renewal', rm: 'RM B' },
    { customer: 'Vivek Sharma', priority: 'Medium', icon: 'fa-arrow-up', reason: 'Cross Sell Opportunity', aum: '₹ 9,80,000', riskScore: 55, lastContact: '5 Days Ago', action: 'Offer Insurance', rm: 'RM C' },
    { customer: 'Karan Singh', priority: 'Medium', icon: 'fa-arrow-up', reason: 'High Value Customer', aum: '₹ 34,60,000', riskScore: 40, lastContact: '10 Days Ago', action: 'Relationship Check-in', rm: 'RM D' },
    { customer: 'Anjali Verma', priority: 'Low', icon: 'fa-arrow-down', reason: 'Regular Follow-up', aum: '₹ 6,70,000', riskScore: 25, lastContact: '3 Days Ago', action: 'General Check-in', rm: 'RM E' }
  ],

  churnTrend: [
    { month: 'Apr 2024', rate: 7.8 },
    { month: 'Jun 2024', rate: 7.2 },
    { month: 'Aug 2024', rate: 7.6 },
    { month: 'Oct 2024', rate: 7.1 },
    { month: 'Dec 2024', rate: 6.9 },
    { month: 'Feb 2025', rate: 6.3 }
  ],

  branches: ['North Branch', 'South Branch', 'West Branch', 'East Branch'],
  products: ['Home Loan', 'Credit Card', 'Mutual Funds', 'Insurance', 'Personal Loan']
};
