import { NextResponse } from "next/server";
import { failedPayments } from "@/lib/mock-data";
import { analyzePayment } from "@/lib/recovery-engine";

export async function POST() {
  const recommendations = failedPayments.map((payment) => ({
    paymentId: payment.id,
    customer: payment.customer,
    recommendation: analyzePayment(payment)
  }));

  return NextResponse.json({
    status: "queued",
    recommendations
  });
}
