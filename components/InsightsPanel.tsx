import { Brain, Sparkles } from "lucide-react";
import { insightCards } from "@/lib/mock-data";

export function InsightsPanel() {
  return (
    <section className="rounded-lg border border-slate-200 bg-ink p-5 text-white shadow-sm">
      <div className="flex items-center gap-3">
        <div className="rounded-lg bg-white/10 p-2">
          <Brain className="h-5 w-5 text-emerald-300" />
        </div>
        <div>
          <h2 className="text-base font-semibold">AI insights</h2>
          <p className="text-sm text-slate-300">Portfolio-level patterns from failed-payment behavior.</p>
        </div>
      </div>
      <div className="mt-5 space-y-3">
        {insightCards.map((insight) => (
          <div key={insight} className="flex gap-3 rounded-lg bg-white/[0.07] p-3 ring-1 ring-white/10">
            <Sparkles className="mt-0.5 h-4 w-4 shrink-0 text-emerald-300" />
            <p className="text-sm leading-6 text-slate-100">{insight}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
