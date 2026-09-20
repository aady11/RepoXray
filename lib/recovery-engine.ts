import type { FailedPayment, RecoveryRecommendation } from "@/lib/types";

const reasonCopy: Record<FailedPayment["failureReason"], string> = {
  insufficient_funds: "Insufficient funds",
  bank_timeout: "Bank timeout",
  expired_card: "Expired card",
  upi_peak_failure: "UPI peak traffic failure",
  authentication_required: "Authentication required"
};

export function formatFailureReason(reason: FailedPayment["failureReason"]) {
  return reasonCopy[reason];
}

export function analyzePayment(payment: FailedPayment): RecoveryRecommendation {
  // This deterministic rules engine simulates the product's AI layer for demos.
  // In production, these rules would be enriched with customer cohorts and model scores.
  if (payment.failureReason === "insufficient_funds") {
    return {
      label: "Retry after salary-cycle window",
      timing: "Next business day at 10:30 AM",
      channel: "smart_retry",
      probabilityLift: 28,
      rationale: "Customers in this cohort recover more often after payroll deposits clear."
    };
  }

  if (payment.failureReason === "bank_timeout") {
    return {
      label: "Short retry after processor stability check",
      timing: "Retry in 2 hours",
      channel: "smart_retry",
      probabilityLift: 17,
      rationale: "Timeouts are usually transient and perform best with a fast, quiet retry."
    };
  }

  if (payment.failureReason === "expired_card") {
    return {
      label: "Request payment method update",
      timing: "Send update link now",
      channel: "payment_link",
      probabilityLift: 22,
      rationale: "Retrying an expired card wastes attempts; a low-friction update link is better."
    };
  }

  if (payment.retryCount >= 3) {
    return {
      label: "Escalate to WhatsApp reminder",
      timing: "Send at 6:00 PM local time",
      channel: "whatsapp",
      probabilityLift: 19,
      rationale: "Repeated failures need a higher-attention channel before the subscriber churns."
    };
  }

  if (payment.failureReason === "authentication_required") {
    return {
      label: "Send SCA authentication prompt",
      timing: "Send secure link immediately",
      channel: "payment_link",
      probabilityLift: 24,
      rationale: "The customer must approve the transaction before another billing attempt."
    };
  }

  return {
    label: "Avoid peak traffic retry",
    timing: "Retry after 11:30 PM",
    channel: "email",
    probabilityLift: 13,
    rationale: "UPI-like failures cluster during traffic spikes; delayed retry improves odds."
  };
}

export function scorePortfolio(payments: FailedPayment[]) {
  const failedTotal = payments.reduce((sum, payment) => sum + payment.amount, 0);
  const recovered = payments
    .filter((payment) => payment.retryStatus === "recovered")
    .reduce((sum, payment) => sum + payment.amount, 0);
  const likelyRecoverable = payments.reduce(
    (sum, payment) => sum + payment.amount * (payment.recoveryProbability / 100),
    0
  );

  return {
    totalFailedPayments: payments.length,
    failedTotal,
    recoveredRevenue: recovered,
    retrySuccessRate: Math.round((payments.filter((p) => p.retryStatus === "recovered").length / payments.length) * 100),
    churnRiskScore: Math.round(payments.reduce((sum, payment) => sum + payment.churnRisk, 0) / payments.length),
    likelyRecoverable: Math.round(likelyRecoverable)
  };
}
