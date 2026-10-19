-- АКС, Stage 1: структура каталога и безопасная основа админки.
-- Эта миграция не импортирует товары и не переключает публичный сайт на Supabase.
-- Применять в Supabase SQL Editor или через Supabase CLI после проверки.

begin;

create extension if not exists pgcrypto;

create table if not exists public.catalog_categories (
  id uuid primary key default gen_random_uuid(),
  parent_id uuid references public.catalog_categories(id) on delete restrict,
  name text not null check (length(btrim(name)) between 1 and 160),
  slug text not null unique check (slug ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$'),
  sort_order integer not null default 0 check (sort_order >= 0),
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.catalog_products (
  id text primary key check (id ~ '^[A-Za-z0-9][A-Za-z0-9._-]{1,127}$'),
  sku text,
  name text not null check (length(btrim(name)) between 1 and 300),
  brand text check (brand is null or length(btrim(brand)) <= 160),
  model text check (model is null or length(btrim(model)) <= 200),
  category_id uuid not null references public.catalog_categories(id) on delete restrict,
  subcategory_id uuid references public.catalog_categories(id) on delete restrict,
  price_tjs numeric(12,2) check (
    price_tjs is null or (price_tjs >= 0 and price_tjs <= 100000000)
  ),
  specifications jsonb not null default '{}'::jsonb check (
    jsonb_typeof(specifications) = 'object'
  ),
  main_image text,
  is_published boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint catalog_products_subcategory_parent_check check (
    subcategory_id is null or subcategory_id <> category_id
  )
);

create table if not exists public.catalog_product_images (
  id uuid primary key default gen_random_uuid(),
  product_id text not null references public.catalog_products(id) on delete cascade,
  storage_path text not null check (length(btrim(storage_path)) between 1 and 1000),
  alt_text text,
  sort_order integer not null default 0 check (sort_order >= 0),
  is_primary boolean not null default false,
  created_at timestamptz not null default now(),
  unique (product_id, storage_path)
);

create table if not exists public.catalog_admins (
  user_id uuid primary key references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);

comment on table public.catalog_categories is
  'Категории каталога АКС; не связана с заказами или складом.';
comment on table public.catalog_products is
  'Товары каталога АКС. id сохраняет совместимость с product.html?id=PRODUCT_ID.';
comment on column public.catalog_products.price_tjs is
  'Цена в сомони (TJS); NULL означает, что цена еще не загружена.';
comment on column public.catalog_products.specifications is
  'Характеристики товара в JSONB-объекте.';
comment on table public.catalog_product_images is
  'Пути объектов Supabase Storage или подготовленные локальные пути изображений.';
comment on table public.catalog_admins is
  'Белый список пользователей Supabase Auth, которым разрешено редактирование каталога.';

create or replace function public.touch_catalog_updated_at()
returns trigger
language plpgsql
as $function$
begin
  new.updated_at = now();
  return new;
end;
$function$;

create or replace function public.prevent_catalog_product_id_change()
returns trigger
language plpgsql
as $function$
begin
  if new.id <> old.id then
    raise exception 'Идентификатор товара нельзя изменить: %', old.id
      using errcode = '42501';
  end if;
  return new;
end;
$function$;

create or replace function public.is_catalog_admin()
returns boolean
language sql
stable
security definer
set search_path = public
as $function$
  select exists (
    select 1
    from public.catalog_admins
    where user_id = auth.uid()
  );
$function$;

drop trigger if exists catalog_categories_updated_at on public.catalog_categories;
create trigger catalog_categories_updated_at
before update on public.catalog_categories
for each row execute function public.touch_catalog_updated_at();

drop trigger if exists catalog_products_updated_at on public.catalog_products;
create trigger catalog_products_updated_at
before update on public.catalog_products
for each row execute function public.touch_catalog_updated_at();

drop trigger if exists catalog_products_id_guard on public.catalog_products;
create trigger catalog_products_id_guard
before update on public.catalog_products
for each row execute function public.prevent_catalog_product_id_change();

create unique index if not exists catalog_products_sku_unique
  on public.catalog_products (lower(btrim(sku)))
  where sku is not null and length(btrim(sku)) > 0;

create index if not exists catalog_categories_parent_sort
  on public.catalog_categories (parent_id, sort_order, name);

create index if not exists catalog_categories_active
  on public.catalog_categories (is_active, sort_order, name);

create index if not exists catalog_products_category
  on public.catalog_products (category_id, subcategory_id);

create index if not exists catalog_products_published
  on public.catalog_products (is_published, updated_at desc);

create index if not exists catalog_products_brand
  on public.catalog_products (brand);

create index if not exists catalog_product_images_product_sort
  on public.catalog_product_images (product_id, sort_order);

create unique index if not exists catalog_product_images_one_primary
  on public.catalog_product_images (product_id)
  where is_primary;

alter table public.catalog_categories enable row level security;
alter table public.catalog_products enable row level security;
alter table public.catalog_product_images enable row level security;
alter table public.catalog_admins enable row level security;

drop policy if exists catalog_categories_public_read on public.catalog_categories;
create policy catalog_categories_public_read
on public.catalog_categories
for select
to anon, authenticated
using (is_active or public.is_catalog_admin());

drop policy if exists catalog_categories_admin_insert on public.catalog_categories;
create policy catalog_categories_admin_insert
on public.catalog_categories
for insert
to authenticated
with check (public.is_catalog_admin());

drop policy if exists catalog_categories_admin_update on public.catalog_categories;
create policy catalog_categories_admin_update
on public.catalog_categories
for update
to authenticated
using (public.is_catalog_admin())
with check (public.is_catalog_admin());

drop policy if exists catalog_categories_admin_delete on public.catalog_categories;
create policy catalog_categories_admin_delete
on public.catalog_categories
for delete
to authenticated
using (public.is_catalog_admin());

drop policy if exists catalog_products_public_read on public.catalog_products;
create policy catalog_products_public_read
on public.catalog_products
for select
to anon, authenticated
using (is_published or public.is_catalog_admin());

drop policy if exists catalog_products_admin_insert on public.catalog_products;
create policy catalog_products_admin_insert
on public.catalog_products
for insert
to authenticated
with check (public.is_catalog_admin());

drop policy if exists catalog_products_admin_update on public.catalog_products;
create policy catalog_products_admin_update
on public.catalog_products
for update
to authenticated
using (public.is_catalog_admin())
with check (public.is_catalog_admin());

drop policy if exists catalog_products_admin_delete on public.catalog_products;
create policy catalog_products_admin_delete
on public.catalog_products
for delete
to authenticated
using (public.is_catalog_admin());

drop policy if exists catalog_product_images_public_read on public.catalog_product_images;
create policy catalog_product_images_public_read
on public.catalog_product_images
for select
to anon, authenticated
using (
  public.is_catalog_admin()
  or exists (
    select 1
    from public.catalog_products p
    where p.id = product_id and p.is_published
  )
);

drop policy if exists catalog_product_images_admin_insert on public.catalog_product_images;
create policy catalog_product_images_admin_insert
on public.catalog_product_images
for insert
to authenticated
with check (public.is_catalog_admin());

drop policy if exists catalog_product_images_admin_update on public.catalog_product_images;
create policy catalog_product_images_admin_update
on public.catalog_product_images
for update
to authenticated
using (public.is_catalog_admin())
with check (public.is_catalog_admin());

drop policy if exists catalog_product_images_admin_delete on public.catalog_product_images;
create policy catalog_product_images_admin_delete
on public.catalog_product_images
for delete
to authenticated
using (public.is_catalog_admin());

drop policy if exists catalog_admins_self_read on public.catalog_admins;
create policy catalog_admins_self_read
on public.catalog_admins
for select
to authenticated
using (user_id = auth.uid());

-- Запись администратора добавляется владельцем вручную через защищенный SQL Editor.
-- Для catalog_admins намеренно нет клиентских INSERT/UPDATE/DELETE-политик.

grant select on public.catalog_categories to anon, authenticated;
grant insert, update, delete on public.catalog_categories to authenticated;

grant select on public.catalog_products to anon, authenticated;
grant insert, update, delete on public.catalog_products to authenticated;

grant select on public.catalog_product_images to anon, authenticated;
grant insert, update, delete on public.catalog_product_images to authenticated;

grant select on public.catalog_admins to authenticated;
grant execute on function public.is_catalog_admin() to anon, authenticated;

-- Отдельное публичное хранилище только для изображений каталога.
-- Если bucket уже существует, его текущая настройка не меняется.
insert into storage.buckets (id, name, public)
values ('catalog-images', 'catalog-images', true)
on conflict (id) do nothing;

drop policy if exists catalog_images_public_read on storage.objects;
create policy catalog_images_public_read
on storage.objects
for select
to public
using (bucket_id = 'catalog-images');

drop policy if exists catalog_images_admin_insert on storage.objects;
create policy catalog_images_admin_insert
on storage.objects
for insert
to authenticated
with check (
  bucket_id = 'catalog-images'
  and public.is_catalog_admin()
);

drop policy if exists catalog_images_admin_update on storage.objects;
create policy catalog_images_admin_update
on storage.objects
for update
to authenticated
using (
  bucket_id = 'catalog-images'
  and public.is_catalog_admin()
)
with check (
  bucket_id = 'catalog-images'
  and public.is_catalog_admin()
);

drop policy if exists catalog_images_admin_delete on storage.objects;
create policy catalog_images_admin_delete
on storage.objects
for delete
to authenticated
using (
  bucket_id = 'catalog-images'
  and public.is_catalog_admin()
);

commit;
