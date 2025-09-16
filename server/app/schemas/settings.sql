-- users_form_settings.sql

create extension if not exists "pgcrypto";

create table if not exists crypto_settings (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  indicators text[] not null default array[]::text[],
  candle_patterns text[] not null default array[]::text[],
  time_ranges text[] not null default array[]::text[],
  time_frames text[] not null default array[]::text[],
  currencies text[] not null default array[]::text[],
  created_at timestamptz default now()
);

alter table crypto_settings
  add constraint name_min_length check (char_length(name) >= 2);

create function check_nonempty_arrays() returns trigger as $$
begin
  if array_length(NEW.indicators, 1) < 1 then
    raise exception 'At least one indicator must be selected';
  end if;
  if array_length(NEW.candle_patterns, 1) < 1 then
    raise exception 'At least one candle pattern must be selected';
  end if;
  if array_length(NEW.time_ranges, 1) < 1 then
    raise exception 'At least one time range must be selected';
  end if;
  if array_length(NEW.time_frames, 1) < 1 then
    raise exception 'At least one time frame must be selected';
  end if;
  if array_length(NEW.currencies, 1) < 1 then
    raise exception 'At least one currency must be selected';
  end if;
  return NEW;
end;
$$ language plpgsql;

create trigger validate_arrays
  before insert or update on crypto_settings
  for each row execute function check_nonempty_arrays();
