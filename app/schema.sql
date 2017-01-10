-- ROLE ---------------------------------------------------
drop table if exists role;

create table role (
  id integer primary key autoincrement,
  extid integer not null,
  charid text not null,
  name text null
);

insert into role (extid, charid, name)
values (10, 'role_10', 'Role 10');

insert into role (extid, charid, name)
values (11, 'role_11', 'Role 11');

insert into role (extid, charid, name)
values (12, 'role_12', 'Role 12');

-- ACCESS CODE --------------------------------------------
drop table if exists acode;

create table acode (
  id integer primary key autoincrement,
  extid integer not null,
  charid text not null,
  name text null
);

insert into acode (extid, charid, name)
values (100, 'acode_100', 'Access Code 100');

insert into acode (extid, charid, name)
values (101, 'acode_101', 'Access Code 101');

insert into acode (extid, charid, name)
values (102, 'acode_102', 'Access Code 102');

insert into acode (extid, charid, name)
values (103, 'acode_103', 'Access Code 103');

insert into acode (extid, charid, name)
values (104, 'acode_104', 'Access Code 104');

-- ROLE - ACCESS CODE -------------------------------------
drop table if exists role_acode;

create table role_acode (
  role_id integer not null,
  acode_id integer not null
);

insert into role_acode (role_id, acode_id) values (2, 1);
insert into role_acode (role_id, acode_id) values (2, 2);
insert into role_acode (role_id, acode_id) values (2, 3);
insert into role_acode (role_id, acode_id) values (3, 2);
insert into role_acode (role_id, acode_id) values (3, 3);
insert into role_acode (role_id, acode_id) values (3, 4);

