-- Enable necessary extensions
create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";

-- Create tables with RLS
create table if not exists public.users (
    id uuid primary key default uuid_generate_v4(),
    email text unique not null,
    name text not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

create table if not exists public.mind_maps (
    id uuid primary key default uuid_generate_v4(),
    title text not null,
    owner_id uuid references public.users(id) not null,
    template_id uuid,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

create table if not exists public.nodes (
    id uuid primary key default uuid_generate_v4(),
    mind_map_id uuid references public.mind_maps(id) not null,
    content text not null,
    position jsonb not null default '{"x": 0, "y": 0}'::jsonb,
    style jsonb,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

create table if not exists public.collaborations (
    id uuid primary key default uuid_generate_v4(),
    mind_map_id uuid references public.mind_maps(id) not null,
    user_id uuid references public.users(id) not null,
    permission text not null check (permission in ('view', 'edit', 'admin')),
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    unique(mind_map_id, user_id)
);

-- Enable Row Level Security
alter table public.users enable row level security;
alter table public.mind_maps enable row level security;
alter table public.nodes enable row level security;
alter table public.collaborations enable row level security;

-- Create RLS Policies

-- Users can read their own profile
create policy "Users can read own profile"
    on public.users for select
    using (auth.uid() = id);

-- Mind maps access policies
create policy "Users can read own mind maps"
    on public.mind_maps for select
    using (auth.uid() = owner_id);

create policy "Users can read shared mind maps"
    on public.mind_maps for select
    using (
        exists (
            select 1 from public.collaborations
            where mind_map_id = id
            and user_id = auth.uid()
        )
    );

create policy "Users can create mind maps"
    on public.mind_maps for insert
    with check (auth.uid() = owner_id);

create policy "Users can update own mind maps"
    on public.mind_maps for update
    using (auth.uid() = owner_id)
    with check (auth.uid() = owner_id);

-- Nodes access policies
create policy "Users can read nodes of accessible mind maps"
    on public.nodes for select
    using (
        exists (
            select 1 from public.mind_maps
            where id = mind_map_id
            and (
                owner_id = auth.uid()
                or exists (
                    select 1 from public.collaborations
                    where mind_map_id = mind_maps.id
                    and user_id = auth.uid()
                )
            )
        )
    );

create policy "Users can modify nodes of own mind maps"
    on public.nodes for all
    using (
        exists (
            select 1 from public.mind_maps
            where id = mind_map_id
            and owner_id = auth.uid()
        )
    );

create policy "Collaborators can modify nodes"
    on public.nodes for all
    using (
        exists (
            select 1 from public.collaborations
            where mind_map_id = nodes.mind_map_id
            and user_id = auth.uid()
            and permission in ('edit', 'admin')
        )
    );

-- Create indexes
create index if not exists idx_mind_maps_owner on public.mind_maps(owner_id);
create index if not exists idx_nodes_mind_map on public.nodes(mind_map_id);
create index if not exists idx_collaborations_user on public.collaborations(user_id);
create index if not exists idx_collaborations_mind_map on public.collaborations(mind_map_id);

-- Create functions for real-time subscriptions
create or replace function public.handle_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql security definer;

-- Create triggers for updated_at
create trigger handle_updated_at_users
    before update on public.users
    for each row execute procedure public.handle_updated_at();

create trigger handle_updated_at_mind_maps
    before update on public.mind_maps
    for each row execute procedure public.handle_updated_at();

create trigger handle_updated_at_nodes
    before update on public.nodes
    for each row execute procedure public.handle_updated_at(); 