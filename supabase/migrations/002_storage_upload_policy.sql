-- Migración 002 · Ejecutar en proyectos creados con la versión inicial de schema.sql
-- Corrige la política de subida a Storage: la política original consultaba public.albums
-- directamente y el rol anon no tiene permiso de lectura sobre esa tabla.

create or replace function public.album_accepts_uploads(p_code text)
returns boolean language sql security definer set search_path = public stable as $$
  select exists (select 1 from albums a where a.code = p_code and a.uploads_open and a.expires_at > now());
$$;
grant execute on function public.album_accepts_uploads(text) to anon, authenticated;

drop policy if exists media_insert on storage.objects;
create policy media_insert on storage.objects for insert to anon, authenticated
  with check (bucket_id = 'media' and public.album_accepts_uploads(split_part(name, '/', 1)));
