import { ActivityFeed } from "@/components/ActivityFeed";
import { AnalyticsChart } from "@/components/AnalyticsChart";
import { InsightsPanel } from "@/components/InsightsPanel";
import { PaymentTable } from "@/components/PaymentTable";
import { StatCard } from "@/components/StatCard";
import { StripeSimulator } from "@/components/StripeSimulator";
import { WorkflowPanel } from "@/components/WorkflowPanel";
import { money } from "@/components/format";
import { failedPayments } from "@/lib/mock-data";
import { scorePortfolio } from "@/lib/recovery-engine";
import { AlertTriangle, Banknote, Gauge, TrendingUp } from "lucide-react";

export default function DashboardPage() {
  const score = scorePortfolio(failedPayments);

  return (
    <main className="min-h-screen bg-cloud">
      <nav className="border-b border-slate-200 bg-white/85 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-ink text-sm font-bold text-white">R</div>
            <div>
              <p className="text-lg font-semibold text-ink">Revix</p>
              <p className="text-xs font-medium text-slate-500">Recovery intelligence</p>
            </div>
          </div>
          <div className="hidden items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 sm:flex">
            Stripe sandbox connected
            <span className="h-2 w-2 rounded-full bg-mint" />
          </div>
        </div>
      </nav>

      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <header className="flex flex-col gap-5 pb-8 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase text-cobalt">Failed payment recovery platform</p>
            <h1 className="mt-3 max-w-3xl text-4xl font-semibold leading-tight text-ink">
              Turn failed subscription payments into intelligent recovery workflows.
            </h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">
              Revix simulates failed-payment intake, AI retry recommendations, workflow automation, and recovery analytics for investor demos and pilot validation.
            </p>
          </div>
          <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <p className="text-xs font-semibold uppercase text-slate-400">Likely recoverable</p>
            <p className="mt-1 text-2xl font-semibold text-ink">{money(score.likelyRecoverable)}</p>
          </div>
        </header>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Total failed payments" value={String(score.totalFailedPayments)} delta={`${money(score.failedTotal)} currently at risk`} tone="coral" icon={AlertTriangle} />
          <StatCard label="Recovered revenue" value={money(score.recoveredRevenue)} delta="Recovered from automated retries" tone="green" icon={Banknote} />
          <StatCard label="Retry success rate" value={`${score.retrySuccessRate}%`} delta="Across active sandbox workflows" tone="blue" icon={TrendingUp} />
          <StatCard label="Churn risk score" value={`${score.churnRiskScore}/100`} delta="Weighted by retry fatigue and behavior" tone="dark" icon={Gauge} />
        </section>

        <div className="mt-6">
          <StripeSimulator />
        </div>

        <section className="mt-6 grid gap-6 xl:grid-cols-[1.35fr_0.65fr]">
          <AnalyticsChart />
          <InsightsPanel />
        </section>

        <section className="mt-6 grid gap-6 xl:grid-cols-[1fr_0.82fr]">
          <WorkflowPanel />
          <ActivityFeed />
        </section>

        <div className="mt-6">
          <PaymentTable payments={failedPayments} />
        </div>
      </div>
    </main>
  );
}
