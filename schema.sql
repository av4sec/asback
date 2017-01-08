-- ROLE ---------------------------------------------------
drop table if exists role;

create table role (
  id integer primary key autoincrement,
  extid integer not null,
  charid text not null,
  name text not null
);

-- ACCESS CODE --------------------------------------------
drop table if exists acode;

create table acode (
  id integer primary key autoincrement,
  extid integer not null,
  charid text not null,
  name text not null
);

-- ROLE - ACCESS CODE -------------------------------------
drop table if exists role_acode;

create table role_acode (
  role_id integer not null,
  acode_id integer not null
);
