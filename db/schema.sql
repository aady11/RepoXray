create table organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  stripe_account_id text,
  created_at timestamptz not null default now()
);

create table users (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references organizations(id) on delete cascade,
  email text not null unique,
  password_hash text not null,
  created_at timestamptz not null default now()
);

create table failed_payments (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references organizations(id) on delete cascade,
  stripe_invoice_id text,
  stripe_customer_id text,
  customer_name text not null,
  customer_email text not null,
  amount_cents integer not null,
  currency text not null default 'usd',
  failure_reason text not null,
  retry_count integer not null default 0,
  retry_status text not null default 'queued',
  recovery_probability integer not null,
  churn_risk integer not null,
  next_retry_at timestamptz,
  created_at timestamptz not null default now()
);

create table recovery_workflows (
  id uuid primary key default gen_random_uuid(),
  failed_payment_id uuid not null references failed_payments(id) on delete cascade,
  channel text not null,
  recommendation text not null,
  status text not null default 'queued',
  probability_lift integer not null,
  created_at timestamptz not null default now()
);

create table recovery_events (
  id uuid primary key default gen_random_uuid(),
  failed_payment_id uuid references failed_payments(id) on delete set null,
  event_type text not null,
  payload jsonb not null default '{}',
  created_at timestamptz not null default now()
);
