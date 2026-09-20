import { analyzePayment, formatFailureReason } from "@/lib/recovery-engine";
import type { FailedPayment } from "@/lib/types";
import { money, shortDate } from "@/components/format";

const statusClasses: Record<FailedPayment["retryStatus"], string> = {
  queued: "bg-blue-50 text-blue-700 ring-blue-100",
  retrying: "bg-amber-50 text-amber-700 ring-amber-100",
  recovered: "bg-emerald-50 text-emerald-700 ring-emerald-100",
  needs_action: "bg-violet-50 text-violet-700 ring-violet-100",
  at_risk: "bg-rose-50 text-rose-700 ring-rose-100"
};

export function PaymentTable({ payments }: { payments: FailedPayment[] }) {
  return (
    <section className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
      <div className="flex flex-col gap-2 border-b border-slate-200 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-base font-semibold text-ink">Failed payment queue</h2>
          <p className="text-sm text-slate-500">AI-ranked recovery actions for current subscription failures.</p>
        </div>
        <span className="w-fit rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
          Live sandbox data
        </span>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-[980px] w-full text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase text-slate-500">
            <tr>
              <th className="px-5 py-3 font-semibold">Customer</th>
              <th className="px-5 py-3 font-semibold">Amount</th>
              <th className="px-5 py-3 font-semibold">Failure reason</th>
              <th className="px-5 py-3 font-semibold">Retry status</th>
              <th className="px-5 py-3 font-semibold">Recovery probability</th>
              <th className="px-5 py-3 font-semibold">Next retry timing</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {payments.map((payment) => {
              const recommendation = analyzePayment(payment);
              return (
                <tr key={payment.id} className="align-top">
                  <td className="px-5 py-4">
                    <div className="font-semibold text-ink">{payment.customer}</div>
                    <div className="text-xs text-slate-500">{payment.company}</div>
                  </td>
                  <td className="px-5 py-4 font-semibold text-ink">{money(payment.amount)}</td>
                  <td className="px-5 py-4">
                    <div className="font-medium text-slate-700">{formatFailureReason(payment.failureReason)}</div>
                    <div className="mt-1 text-xs text-slate-500">{payment.behaviorTag}</div>
                  </td>
                  <td className="px-5 py-4">
                    <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ${statusClasses[payment.retryStatus]}`}>
                      {payment.retryStatus.replace("_", " ")}
                    </span>
                  </td>
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-3">
                      <div className="h-2 w-24 rounded-full bg-slate-100">
                        <div
                          className="h-2 rounded-full bg-mint"
                          style={{ width: `${payment.recoveryProbability}%` }}
                        />
                      </div>
                      <span className="font-semibold text-slate-700">{payment.recoveryProbability}%</span>
                    </div>
                  </td>
                  <td className="px-5 py-4">
                    <div className="font-medium text-slate-700">{recommendation.timing}</div>
                    <div className="mt-1 text-xs text-slate-500">{shortDate(payment.nextRetryAt)}</div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}
