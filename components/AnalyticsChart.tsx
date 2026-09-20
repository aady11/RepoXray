const bars = [
  { label: "Mon", failed: 44, recovered: 28 },
  { label: "Tue", failed: 59, recovered: 36 },
  { label: "Wed", failed: 51, recovered: 42 },
  { label: "Thu", failed: 66, recovered: 49 },
  { label: "Fri", failed: 72, recovered: 54 },
  { label: "Sat", failed: 38, recovered: 31 },
  { label: "Sun", failed: 46, recovered: 37 }
];

export function AnalyticsChart() {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-base font-semibold text-ink">Payment recovery analytics</h2>
          <p className="text-sm text-slate-500">Failed invoices versus recovered revenue this week.</p>
        </div>
        <div className="flex gap-3 text-xs font-medium text-slate-500">
          <span className="flex items-center gap-1.5"><i className="h-2.5 w-2.5 rounded-full bg-coral" />Failed</span>
          <span className="flex items-center gap-1.5"><i className="h-2.5 w-2.5 rounded-full bg-mint" />Recovered</span>
        </div>
      </div>
      <div className="mt-8 flex h-64 items-end gap-4">
        {bars.map((bar) => (
          <div key={bar.label} className="flex flex-1 flex-col items-center gap-3">
            <div className="flex h-48 w-full items-end justify-center gap-1.5">
              <div className="w-full max-w-5 rounded-t-md bg-coral/80" style={{ height: `${bar.failed}%` }} />
              <div className="w-full max-w-5 rounded-t-md bg-mint" style={{ height: `${bar.recovered}%` }} />
            </div>
            <span className="text-xs font-medium text-slate-500">{bar.label}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
