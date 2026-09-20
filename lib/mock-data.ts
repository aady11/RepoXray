import type { Activity, FailedPayment } from "@/lib/types";

export const failedPayments: FailedPayment[] = [
  {
    id: "fp_1001",
    customer: "Maya Chen",
    company: "Northstar CRM",
    email: "maya@northstarcrm.example",
    amount: 499,
    currency: "USD",
    failureReason: "insufficient_funds",
    retryCount: 1,
    lastFailedAt: "2026-05-10T06:14:00.000Z",
    nextRetryAt: "2026-05-11T05:00:00.000Z",
    retryStatus: "queued",
    recoveryProbability: 74,
    churnRisk: 31,
    preferredChannel: "smart_retry",
    behaviorTag: "Pays successfully after payroll"
  },
  {
    id: "fp_1002",
    customer: "Arjun Mehta",
    company: "OpsPilot",
    email: "arjun@opspilot.example",
    amount: 1299,
    currency: "USD",
    failureReason: "bank_timeout",
    retryCount: 0,
    lastFailedAt: "2026-05-10T07:42:00.000Z",
    nextRetryAt: "2026-05-10T09:42:00.000Z",
    retryStatus: "retrying",
    recoveryProbability: 82,
    churnRisk: 18,
    preferredChannel: "smart_retry",
    behaviorTag: "High intent admin activity"
  },
  {
    id: "fp_1003",
    customer: "Elena Rodriguez",
    company: "Ledgerly",
    email: "elena@ledgerly.example",
    amount: 249,
    currency: "USD",
    failureReason: "expired_card",
    retryCount: 2,
    lastFailedAt: "2026-05-09T19:18:00.000Z",
    nextRetryAt: "2026-05-10T08:15:00.000Z",
    retryStatus: "needs_action",
    recoveryProbability: 61,
    churnRisk: 48,
    preferredChannel: "payment_link",
    behaviorTag: "Card changed last quarter"
  },
  {
    id: "fp_1004",
    customer: "Noah Bennett",
    company: "CloudDesk",
    email: "noah@clouddesk.example",
    amount: 899,
    currency: "USD",
    failureReason: "authentication_required",
    retryCount: 1,
    lastFailedAt: "2026-05-09T13:22:00.000Z",
    nextRetryAt: "2026-05-10T10:00:00.000Z",
    retryStatus: "queued",
    recoveryProbability: 69,
    churnRisk: 36,
    preferredChannel: "payment_link",
    behaviorTag: "Owner approves invoices manually"
  },
  {
    id: "fp_1005",
    customer: "Priya Shah",
    company: "SignalForms",
    email: "priya@signalforms.example",
    amount: 179,
    currency: "USD",
    failureReason: "upi_peak_failure",
    retryCount: 3,
    lastFailedAt: "2026-05-08T16:05:00.000Z",
    nextRetryAt: "2026-05-10T12:30:00.000Z",
    retryStatus: "at_risk",
    recoveryProbability: 47,
    churnRisk: 66,
    preferredChannel: "whatsapp",
    behaviorTag: "Responds faster to mobile nudges"
  },
  {
    id: "fp_1006",
    customer: "Liam Carter",
    company: "MetricNest",
    email: "liam@metricnest.example",
    amount: 399,
    currency: "USD",
    failureReason: "bank_timeout",
    retryCount: 1,
    lastFailedAt: "2026-05-08T09:50:00.000Z",
    nextRetryAt: "2026-05-08T11:50:00.000Z",
    retryStatus: "recovered",
    recoveryProbability: 88,
    churnRisk: 12,
    preferredChannel: "smart_retry",
    behaviorTag: "Recovered on quiet retry"
  }
];

export const activity: Activity[] = [
  {
    id: "act_1",
    customer: "Arjun Mehta",
    event: "Smart retry queued after processor timeout",
    channel: "smart_retry",
    time: "12 min ago",
    impact: "+$1,299 expected"
  },
  {
    id: "act_2",
    customer: "Elena Rodriguez",
    event: "Payment update link delivered",
    channel: "payment_link",
    time: "38 min ago",
    impact: "Card update pending"
  },
  {
    id: "act_3",
    customer: "Priya Shah",
    event: "WhatsApp recovery reminder scheduled",
    channel: "whatsapp",
    time: "1 hr ago",
    impact: "High churn risk"
  },
  {
    id: "act_4",
    customer: "Liam Carter",
    event: "Retry succeeded and invoice marked paid",
    channel: "smart_retry",
    time: "2 hrs ago",
    impact: "+$399 recovered"
  }
];

export const insightCards = [
  "Customers paying after salary dates recover 28% more successfully.",
  "WhatsApp reminders outperform email by 19% for repeated failures.",
  "UPI-style failures spike during peak traffic hours and recover better overnight.",
  "Expired-card retries should switch to payment update links before the third attempt."
];
