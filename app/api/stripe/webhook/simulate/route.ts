import { NextResponse } from "next/server";
import { analyzePayment } from "@/lib/recovery-engine";
import type { FailedPayment } from "@/lib/types";

export async function POST() {
  const sandboxEvent = {
    id: "evt_stripe_sandbox_001",
    type: "invoice.payment_failed",
    created: Date.now()
  };

  const failedPayment: FailedPayment = {
    id: "fp_sandbox_live",
    customer: "Simone Foster",
    company: "DemoScale",
    email: "simone@demoscale.example",
    amount: 799,
    currency: "USD",
    failureReason: "insufficient_funds",
    retryCount: 1,
    lastFailedAt: new Date().toISOString(),
    nextRetryAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
    retryStatus: "queued",
    recoveryProbability: 76,
    churnRisk: 34,
    preferredChannel: "smart_retry",
    behaviorTag: "Historically recovers after payroll"
  };

  // Prototype persistence boundary: replace this with a Prisma/Supabase insert
  // when connecting Postgres. The response mirrors the durable record shape.
  return NextResponse.json({
    received: true,
    event: sandboxEvent,
    storedTransaction: failedPayment,
    recoveryRecommendation: analyzePayment(failedPayment),
    workflow: {
      status: "queued",
      channel: "smart_retry"
    }
  });
}
