"use client";

import { useState } from "react";
import { Play, RotateCcw } from "lucide-react";

export function StripeSimulator() {
  const [state, setState] = useState<"idle" | "running" | "complete">("idle");

  async function runSimulation() {
    setState("running");
    await fetch("/api/stripe/webhook/simulate", { method: "POST" });
    setState("complete");
  }

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-base font-semibold text-ink">Stripe sandbox simulation</h2>
          <p className="text-sm text-slate-500">Trigger a mock `invoice.payment_failed` event and run recovery analysis.</p>
        </div>
        <button
          onClick={runSimulation}
          disabled={state === "running"}
          className="inline-flex w-fit items-center gap-2 rounded-lg bg-ink px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-graphite disabled:cursor-not-allowed disabled:opacity-70"
        >
          {state === "running" ? <RotateCcw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
          {state === "running" ? "Analyzing" : "Run failed payment"}
        </button>
      </div>
      {state === "complete" && (
        <div className="mt-4 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm font-medium text-emerald-800">
          Webhook received, failed transaction stored, AI recommendation generated, workflow queued.
        </div>
      )}
    </section>
  );
}
