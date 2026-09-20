export type FailureReason =
  | "insufficient_funds"
  | "bank_timeout"
  | "expired_card"
  | "upi_peak_failure"
  | "authentication_required";

export type WorkflowChannel = "email" | "whatsapp" | "payment_link" | "smart_retry";

export type RetryStatus = "queued" | "retrying" | "recovered" | "needs_action" | "at_risk";

export type FailedPayment = {
  id: string;
  customer: string;
  company: string;
  email: string;
  amount: number;
  currency: "USD";
  failureReason: FailureReason;
  retryCount: number;
  lastFailedAt: string;
  nextRetryAt: string;
  retryStatus: RetryStatus;
  recoveryProbability: number;
  churnRisk: number;
  preferredChannel: WorkflowChannel;
  behaviorTag: string;
};

export type RecoveryRecommendation = {
  label: string;
  timing: string;
  channel: WorkflowChannel;
  probabilityLift: number;
  rationale: string;
};

export type Activity = {
  id: string;
  customer: string;
  event: string;
  channel: WorkflowChannel;
  time: string;
  impact: string;
};
