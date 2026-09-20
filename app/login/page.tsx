import Link from "next/link";
import { ArrowRight, CheckCircle2 } from "lucide-react";

export default function LoginPage() {
  return (
    <main className="grid min-h-screen grid-cols-1 bg-cloud lg:grid-cols-[0.95fr_1.05fr]">
      <section className="flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-md rounded-lg border border-slate-200 bg-white p-8 shadow-soft">
          <div className="mb-8">
            <div className="text-2xl font-semibold text-ink">Revix</div>
            <p className="mt-2 text-sm text-slate-500">Sign in to your recovery intelligence workspace.</p>
          </div>
          <form action="/api/auth/login" method="post" className="space-y-4">
            <label className="block">
              <span className="text-sm font-medium text-slate-700">Work email</span>
              <input
                name="email"
                type="email"
                defaultValue="founder@demo.revix"
                className="mt-2 w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 outline-none ring-cobalt/20 transition focus:ring-4"
              />
            </label>
            <label className="block">
              <span className="text-sm font-medium text-slate-700">Password</span>
              <input
                name="password"
                type="password"
                defaultValue="revixdemo"
                className="mt-2 w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 outline-none ring-cobalt/20 transition focus:ring-4"
              />
            </label>
            <button className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white transition hover:bg-graphite">
              Open dashboard
              <ArrowRight className="h-4 w-4" />
            </button>
          </form>
          <p className="mt-6 text-center text-sm text-slate-500">
            New pilot workspace?{" "}
            <Link href="/signup" className="font-semibold text-cobalt">
              Create an account
            </Link>
          </p>
        </div>
      </section>
      <section className="grid-pattern hidden items-center px-10 lg:flex">
        <div className="max-w-xl">
          <p className="text-sm font-semibold uppercase text-cobalt">AI-powered failed payment recovery</p>
          <h1 className="mt-4 text-5xl font-semibold leading-tight text-ink">Recover subscription revenue before failed payments become churn.</h1>
          <div className="mt-8 grid gap-3">
            {[
              "Smart retry timing based on failure reason and customer behavior",
              "Automated email, WhatsApp, and payment update workflows",
              "Investor-demo friendly analytics that update from sandbox events"
            ].map((item) => (
              <div key={item} className="flex items-center gap-3 rounded-lg bg-white/80 p-3 text-sm font-medium text-slate-700 ring-1 ring-slate-200">
                <CheckCircle2 className="h-4 w-4 text-mint" />
                {item}
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
