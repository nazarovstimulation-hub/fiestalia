-- Fiestalia · esquema de base de datos para Supabase (Postgres)
-- Ejecutar en: Supabase → SQL Editor → New query → Run
-- Región recomendada del proyecto: Frankfurt (eu-central-1) para alojar en la UE.

create extension if not exists pgcrypto;

-- ───────────────────────── Tablas ─────────────────────────
create table if not exists public.albums (
  code            text primary key,
  admin_key_hash  text not null,
  name            text not null,
  event_date      date,
  event_type      text default 'boda',
  organizer_name  text not null,
  organizer_email text not null,
  welcome         text default '',
  plan            text not null default 'gratis',
  requested_plan  text default 'gratis',
  photo_limit     int  not null default 50,
  uploads_open    boolean not null default true,
  moderation      boolean not null default false,
  selfie_enabled  boolean not null default false,
  paid_at         timestamptz,
  stripe_session  text,
  created_at      timestamptz not null default now(),
  expires_at      timestamptz not null default now() + interval '1 month'
);

create table if not exists public.photos (
  id            uuid primary key,
  album_code    text not null references public.albums(code) on delete cascade,
  uploader_name text not null default 'Invitado',
  type          text not null default 'image',
  mime          text,
  size          bigint default 0,
  width         int,
  height        int,
  duration      numeric,
  hidden        boolean not null default false,
  storage_path  text not null,
  thumb_path    text,
  created_at    timestamptz not null default now()
);
create index if not exists photos_album_idx on public.photos(album_code, created_at desc);

-- Vista pública del álbum (sin el hash de la clave de administración)
create or replace view public.albums_public as
  select code, name, event_date, event_type, organizer_name, welcome, plan, photo_limit,
         uploads_open, moderation, selfie_enabled, created_at, expires_at
  from public.albums;

-- ───────────────────────── Seguridad (RLS) ─────────────────────────
alter table public.albums enable row level security;
alter table public.photos enable row level security;

-- Cualquiera (anon) puede crear un álbum; nadie puede leer la tabla albums directamente
-- (se lee a través de la vista albums_public o de la función album_admin).
drop policy if exists albums_insert on public.albums;
create policy albums_insert on public.albums for insert to anon, authenticated with check (true);

-- Las fotos visibles se pueden leer; las ocultas solo vía album_admin / listado del panel
drop policy if exists photos_select on public.photos;
create policy photos_select on public.photos for select to anon, authenticated using (true);
-- Inserciones, cambios y borrados solo a través de las funciones de abajo (security definer).

grant select on public.albums_public to anon, authenticated;
grant insert on public.albums to anon, authenticated;
grant select on public.photos to anon, authenticated;

-- ───────────────────────── Funciones ─────────────────────────
create or replace function public.album_admin(p_code text, p_key text)
returns json language plpgsql security definer set search_path = public as $$
declare a albums%rowtype;
begin
  select * into a from albums where code = p_code;
  if not found then return null; end if;
  if a.admin_key_hash <> encode(digest(p_key, 'sha256'), 'hex') then return null; end if;
  return to_json((select r from (select a.code, a.name, a.event_date, a.event_type, a.organizer_name, a.organizer_email,
                   a.welcome, a.plan, a.requested_plan, a.photo_limit, a.uploads_open, a.moderation, a.selfie_enabled,
                   a.paid_at, a.created_at, a.expires_at) r));
end $$;

create or replace function public.album_update(p_code text, p_key text, p_patch jsonb)
returns json language plpgsql security definer set search_path = public as $$
declare a albums%rowtype;
begin
  select * into a from albums where code = p_code;
  if not found or a.admin_key_hash <> encode(digest(p_key, 'sha256'), 'hex') then
    raise exception 'Clave de administración no válida';
  end if;
  update albums set
    name           = coalesce(nullif(p_patch->>'name', ''), name),
    event_date     = case when p_patch ? 'event_date' then nullif(p_patch->>'event_date', '')::date else event_date end,
    welcome        = coalesce(p_patch->>'welcome', welcome),
    uploads_open   = coalesce((p_patch->>'uploads_open')::boolean, uploads_open),
    moderation     = coalesce((p_patch->>'moderation')::boolean, moderation),
    selfie_enabled = coalesce((p_patch->>'selfie_enabled')::boolean, selfie_enabled)
  where code = p_code;
  return album_admin(p_code, p_key);
end $$;

-- Un invitado registra una foto ya subida a Storage. Comprueba límites.
create or replace function public.photo_add(
  p_id uuid, p_code text, p_uploader text, p_type text, p_mime text, p_size bigint,
  p_width int, p_height int, p_duration numeric, p_path text, p_thumb text)
returns json language plpgsql security definer set search_path = public as $$
declare a albums%rowtype; n int; p photos%rowtype;
begin
  select * into a from albums where code = p_code;
  if not found then raise exception 'Álbum no encontrado'; end if;
  if not a.uploads_open then raise exception 'Subidas cerradas'; end if;
  if a.expires_at < now() then raise exception 'Álbum caducado'; end if;
  select count(*) into n from photos where album_code = p_code;
  if n >= a.photo_limit then raise exception 'LIMIT'; end if;
  if p_path not like p_code || '/%' then raise exception 'Ruta no válida'; end if;
  insert into photos (id, album_code, uploader_name, type, mime, size, width, height, duration, hidden, storage_path, thumb_path)
  values (p_id, p_code, left(coalesce(nullif(trim(p_uploader), ''), 'Invitado'), 40), p_type, p_mime, p_size, p_width, p_height, p_duration, a.moderation, p_path, p_thumb)
  returning * into p;
  return to_json(p);
end $$;

create or replace function public.photo_set_hidden(p_code text, p_key text, p_id uuid, p_hidden boolean)
returns void language plpgsql security definer set search_path = public as $$
begin
  if album_admin(p_code, p_key) is null then raise exception 'Clave de administración no válida'; end if;
  update photos set hidden = p_hidden where id = p_id and album_code = p_code;
end $$;

-- Borra la fila y devuelve las rutas de Storage a eliminar (el cliente las borra con la política de abajo)
create or replace function public.photo_delete(p_code text, p_key text, p_id uuid)
returns text[] language plpgsql security definer set search_path = public as $$
declare paths text[];
begin
  if album_admin(p_code, p_key) is null then raise exception 'Clave de administración no válida'; end if;
  select array_remove(array[storage_path, thumb_path], null) into paths from photos where id = p_id and album_code = p_code;
  delete from photos where id = p_id and album_code = p_code;
  return coalesce(paths, '{}');
end $$;

-- Llamada por el webhook de Stripe (service role) para activar un plan
create or replace function public.album_set_plan(p_code text, p_plan text, p_limit int, p_months int, p_session text)
returns void language plpgsql security definer set search_path = public as $$
begin
  update albums set plan = p_plan, photo_limit = p_limit, paid_at = now(), stripe_session = p_session,
    expires_at = now() + make_interval(months => p_months)
  where code = p_code;
end $$;

grant execute on function public.album_admin(text, text) to anon, authenticated;
grant execute on function public.album_update(text, text, jsonb) to anon, authenticated;
grant execute on function public.photo_add(uuid, text, text, text, text, bigint, int, int, numeric, text, text) to anon, authenticated;
grant execute on function public.photo_set_hidden(text, text, uuid, boolean) to anon, authenticated;
grant execute on function public.photo_delete(text, text, uuid) to anon, authenticated;
revoke execute on function public.album_set_plan(text, text, int, int, text) from anon, authenticated;

-- ───────────────────────── Tiempo real ─────────────────────────
-- Supabase → Database → Replication → activar la tabla "photos" (o ejecutar):
alter publication supabase_realtime add table public.photos;

-- ───────────────────────── Storage ─────────────────────────
-- Crear el bucket "media" como PÚBLICO (Storage → New bucket → Public).
-- Las rutas son impredecibles (código del álbum + uuid), así que el acceso
-- equivale a tener el enlace del álbum. Políticas del bucket:
insert into storage.buckets (id, name, public, file_size_limit)
  values ('media', 'media', true, 209715200) on conflict (id) do nothing;

drop policy if exists media_read on storage.objects;
create policy media_read on storage.objects for select to anon, authenticated using (bucket_id = 'media');

drop policy if exists media_insert on storage.objects;
create policy media_insert on storage.objects for insert to anon, authenticated
  with check (bucket_id = 'media' and exists (select 1 from public.albums a where a.code = split_part(name, '/', 1) and a.uploads_open));

-- El borrado de objetos lo hace el cliente tras photo_delete; se permite dentro del bucket.
-- (Para endurecerlo, mover el borrado a una Edge Function con service role.)
drop policy if exists media_delete on storage.objects;
create policy media_delete on storage.objects for delete to anon, authenticated using (bucket_id = 'media');

-- ───────────────────────── Limpieza de álbumes caducados ─────────────────────────
-- Programar (Database → Cron) una vez al día:
--   select cron.schedule('fiestalia-cleanup', '0 4 * * *', $$ delete from public.albums where expires_at < now() - interval '30 days' $$);
-- Los objetos de Storage huérfanos se eliminan con la Edge Function "cleanup" (pendiente) o a mano.
