import type { LucideIcon } from "lucide-react";

type StatCardProps = {
  label: string;
  value: string;
  delta: string;
  tone: "blue" | "green" | "coral" | "dark";
  icon: LucideIcon;
};

const toneClasses = {
  blue: "bg-blue-50 text-cobalt ring-blue-100",
  green: "bg-emerald-50 text-mint ring-emerald-100",
  coral: "bg-rose-50 text-coral ring-rose-100",
  dark: "bg-slate-100 text-graphite ring-slate-200"
};

export function StatCard({ label, value, delta, tone, icon: Icon }: StatCardProps) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-500">{label}</p>
          <p className="mt-3 text-3xl font-semibold tracking-normal text-ink">{value}</p>
        </div>
        <div className={`rounded-lg p-2.5 ring-1 ${toneClasses[tone]}`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
      <p className="mt-4 text-sm text-slate-500">{delta}</p>
    </section>
  );
}
