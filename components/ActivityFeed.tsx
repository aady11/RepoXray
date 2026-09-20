import { activity } from "@/lib/mock-data";

export function ActivityFeed() {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <h2 className="text-base font-semibold text-ink">Recent recovery activity</h2>
      <div className="mt-5 space-y-4">
        {activity.map((item) => (
          <div key={item.id} className="flex gap-3">
            <div className="mt-1 h-2.5 w-2.5 rounded-full bg-mint" />
            <div className="min-w-0">
              <p className="text-sm font-semibold text-ink">{item.customer}</p>
              <p className="text-sm leading-6 text-slate-500">{item.event}</p>
              <p className="mt-1 text-xs font-medium text-slate-400">
                {item.time} · {item.impact}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
