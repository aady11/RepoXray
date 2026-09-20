import { NextResponse } from "next/server";
import { failedPayments } from "@/lib/mock-data";

export async function GET() {
  return NextResponse.json({ data: failedPayments });
}
