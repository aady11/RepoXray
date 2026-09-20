import { Mail, MessageCircle, RefreshCcw, ShieldCheck } from "lucide-react";

const workflows = [
  {
    title: "Smart retry",
    detail: "Retry attempts are queued by failure reason, customer behavior, and predicted cash availability.",
    icon: RefreshCcw,
    metric: "74% median recovery probability"
  },
  {
    title: "Email recovery",
    detail: "Branded reminder email with invoice context and a secure payment update link.",
    icon: Mail,
    metric: "31 active sequences"
  },
  {
    title: "WhatsApp reminder",
    detail: "Higher-attention nudge for repeat failures and customers who respond better on mobile.",
    icon: MessageCircle,
    metric: "19% lift vs email"
  },
  {
    title: "Payment update link",
    detail: "Hosted card update flow for expired cards, SCA, and authentication-required failures.",
    icon: ShieldCheck,
    metric: "22% lift on card failures"
  }
];

export function WorkflowPanel() {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <h2 className="text-base font-semibold text-ink">Recovery workflows</h2>
      <div className="mt-5 grid gap-3">
        {workflows.map((workflow) => (
          <div key={workflow.title} className="rounded-lg border border-slate-200 p-4">
            <div className="flex items-start gap-3">
              <div className="rounded-lg bg-slate-100 p-2 text-graphite">
                <workflow.icon className="h-4 w-4" />
              </div>
              <div>
                <h3 className="font-semibold text-ink">{workflow.title}</h3>
                <p className="mt-1 text-sm leading-6 text-slate-500">{workflow.detail}</p>
                <p className="mt-3 text-xs font-semibold uppercase text-cobalt">{workflow.metric}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
