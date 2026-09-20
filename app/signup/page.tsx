import Link from "next/link";
import { ArrowRight } from "lucide-react";

export default function SignupPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-cloud px-6 py-12">
      <div className="w-full max-w-lg rounded-lg border border-slate-200 bg-white p-8 shadow-soft">
        <div>
          <div className="text-2xl font-semibold text-ink">Start Revix</div>
          <p className="mt-2 text-sm text-slate-500">Create a demo workspace for subscription recovery pilots.</p>
        </div>
        <form action="/api/auth/login" method="post" className="mt-8 grid gap-4">
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Company name</span>
            <input name="company" defaultValue="Acme Subscriptions" className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2.5 outline-none ring-cobalt/20 transition focus:ring-4" />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Work email</span>
            <input name="email" type="email" defaultValue="founder@acme.example" className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2.5 outline-none ring-cobalt/20 transition focus:ring-4" />
          </label>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Password</span>
            <input name="password" type="password" defaultValue="revixdemo" className="mt-2 w-full rounded-lg border border-slate-200 px-3 py-2.5 outline-none ring-cobalt/20 transition focus:ring-4" />
          </label>
          <button className="inline-flex items-center justify-center gap-2 rounded-lg bg-ink px-4 py-3 text-sm font-semibold text-white transition hover:bg-graphite">
            Create workspace
            <ArrowRight className="h-4 w-4" />
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-500">
          Already have access?{" "}
          <Link href="/login" className="font-semibold text-cobalt">
            Sign in
          </Link>
        </p>
      </div>
    </main>
  );
}
