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

-- ENTITY -------------------------------------------------
drop table if exists entity;

create table entity (
  id integer primary key autoincrement,
  type text not null,
  extid integer not null,
  charid text not null,
  name text null
);

insert into entity (id, type, extid, charid, name)
values (1, 'APPL', 1, 'appl_1', 'APPL 1');

insert into entity (id, type, extid, charid, name)
values (2, 'APPL', 2, 'appl_2', 'APPL 2');

insert into entity (id, type, extid, charid, name)
values (3, 'APPL', 3, 'appl_3', 'APPL 3');

insert into entity (id, type, extid, charid, name)
values (4, 'CTX', 4, 'ctx_4', 'CTX 4');

insert into entity (id, type, extid, charid, name)
values (5, 'CTX', 5, 'ctx_5', 'CTX 5');

insert into entity (id, type, extid, charid, name)
values (6, 'CTX', 6, 'ctx_6', 'CTX 6');

insert into entity (id, type, extid, charid, name)
values (7, 'CTX', 7, 'ctx_7', 'CTX 7');

insert into entity (id, type, extid, charid, name)
values (8, 'CTX', 8, 'ctx_8', 'CTX 8');

insert into entity (id, type, extid, charid, name)
values (9, 'MTYP', 9, 'mtyp_9', 'MTYP 9');

insert into entity (id, type, extid, charid, name)
values (10, 'MTYP', 10, 'mtyp_10', 'MTYP 10');

insert into entity (id, type, extid, charid, name)
values (11, 'MTYP', 11, 'mtyp_11', 'MTYP 11');

insert into entity (id, type, extid, charid, name)
values (12, 'TASK', 12, 'mtyp_12', 'MTYP 12');

insert into entity (id, type, extid, charid, name)
values (13, 'TASK', 13, 'mtyp_13', 'MTYP 13');

insert into entity (id, type, extid, charid, name)
values (14, 'TASK', 14, 'mtyp_14', 'MTYP 14');

insert into entity (id, type, extid, charid, name)
values (15, 'TASK', 15, 'mtyp_15', 'MTYP 15');

insert into entity (id, type, extid, charid, name)
values (16, 'TASK', 16, 'mtyp_16', 'MTYP 16');

insert into entity (id, type, extid, charid, name)
values (17, 'WFC', 17, 'wfc_17', 'WFC 17');

insert into entity (id, type, extid, charid, name)
values (18, 'WFC', 18, 'wfc_18', 'WFC 18');

insert into entity (id, type, extid, charid, name)
values (19, 'WFC', 19, 'wfc_19', 'WFC 19');

insert into entity (id, type, extid, charid, name)
values (20, 'WFC', 20, 'wfc_20', 'WFC 20');

-- ENTITY_APPL --------------------------------------------
drop table if exists entity_appl;

create table entity_appl (
  entity_id integer primary key
);

insert into entity_appl (entity_id) values (1);
insert into entity_appl (entity_id) values (2);
insert into entity_appl (entity_id) values (3);

drop view if exists entity_appl_v;

create view entity_appl_v as
  select e.id as id,
         e.type as type,
         e.extid as extid,
         e.charid as charid,
         e.name as name
    from entity e
    join entity_appl a on e.id = a.entity_id and e.type = 'APPL';

-- ENTITY_CTX ---------------------------------------------
drop table if exists entity_ctx;

create table entity_ctx (
  entity_id integer primary key,
  parent_id text,
  is_parent text,
  group_id integer,
  global_order_by integer
);

insert into entity_ctx (entity_id, parent_id, is_parent, group_id, global_order_by)
values (4, null, null, 100, 4);

insert into entity_ctx (entity_id, parent_id, is_parent, group_id, global_order_by)
values (5, null, null, 100, 5);

insert into entity_ctx (entity_id, parent_id, is_parent, group_id, global_order_by)
values (6, null, '+', 101, 4);

insert into entity_ctx (entity_id, parent_id, is_parent, group_id, global_order_by)
values (7, null, null, 101, 5);

insert into entity_ctx (entity_id, parent_id, is_parent, group_id, global_order_by)
values (8, null, '+', 101, 6);

drop view if exists entity_ctx_v;

create view entity_ctx_v as
  select e.id as id,
         e.type as type,
         e.extid as extid,
         e.charid as charid,
         e.name as name,
         c.parent_id as parent_id,
         c.is_parent as is_parent,
         c.group_id as group_id,
         c.global_order_by as global_order_by
    from entity e
    join entity_ctx c on e.id = c.entity_id and e.type = 'CTX';

-- ENTITY_MTYP --------------------------------------------
drop table if exists entity_mtyp;

create table entity_mtyp (
  entity_id integer primary key,
  grp text
);

insert into entity_mtyp (entity_id, grp)
values (9, 'TRX');

insert into entity_mtyp (entity_id, grp)
values (10, 'OBJ');

insert into entity_mtyp (entity_id, grp)
values (11, 'TRX');

drop view if exists entity_mtyp_v;

create view entity_mtyp_v as
  select e.id as id,
         e.type as type,
         e.extid as extid,
         e.charid as charid,
         e.name as name,
         m.grp as grp
    from entity e
    join entity_mtyp m on e.id = m.entity_id and e.type = 'MTYP';

-- ENTITY_TASK --------------------------------------------
drop table if exists entity_task;

create table entity_task (
  entity_id integer primary key,
  type text,
  meta_out_id integer
);

insert into entity_task (entity_id, type, meta_out_id)
values (12, 'program', 2222);

insert into entity_task (entity_id, type, meta_out_id)
values (13, 'program', 3333);

insert into entity_task (entity_id, type, meta_out_id)
values (14, 'report', 4444);

insert into entity_task (entity_id, type, meta_out_id)
values (15, 'report', 5555);

insert into entity_task (entity_id, type, meta_out_id)
values (16, 'report', 6666);

drop view if exists entity_task_v;

create view entity_task_v as
  select e.id as id,
         e.type as type,
         e.extid as extid,
         e.charid as charid,
         e.name as name,
         t.type as type,
         t.meta_out_id as meta_out_id
    from entity e
    join entity_task t on e.id = t.entity_id and e.type = 'TASK';

-- ENTITY_WFC ---------------------------------------------
drop table if exists entity_wfc;

create table entity_wfc (
  entity_id integer primary key,
  meta_typ_id integer,
  wfc_action_id integer,
  status_id integer
);

drop table if exists wfc_status;

create table wfc_status (
  meta_typ_id integer,
  status_id integer,
  charid text,
  name text
);

insert into entity_wfc (entity_id, meta_typ_id, wfc_action_id, status_id)
values (17, 1, 1, 10);

insert into entity_wfc (entity_id, meta_typ_id, wfc_action_id, status_id)
values (18, 1, 2, 11);

insert into entity_wfc (entity_id, meta_typ_id, wfc_action_id, status_id)
values (19, 45, 1, 10);

insert into entity_wfc (entity_id, meta_typ_id, wfc_action_id, status_id)
values (20, 45, 2, 11);

insert into wfc_status (meta_typ_id, status_id, charid, name)
values (1, 10, 'status_1_10', 'Status 10 (1)');

insert into wfc_status (meta_typ_id, status_id, charid, name)
values (1, 11, 'status_1_11', 'Status 11 (1)');

insert into wfc_status (meta_typ_id, status_id, charid, name)
values (45, 10, 'status_45_10', 'Status 10 (45)');

insert into wfc_status (meta_typ_id, status_id, charid, name)
values (45, 11, 'status_45_11', 'Status 11 (45)');

drop view if exists entity_wfc_v;

create view entity_wfc_v as
  select e.id as id,
         e.type as type,
         e.extid as extid,
         e.charid as charid,
         e.name as name,
         w.meta_typ_id as meta_typ_id,
         w.wfc_action_id as wfc_action_id,
         w.status_id as status_id,
         ws.charid as status_charid,
         ws.name as status_name
    from entity e
    left join wfc_status ws on ws.meta_typ_id = w.meta_typ_id and ws.status_id = w.status_id
    join entity_wfc w on e.id = w.entity_id and e.type = 'WFC';

-- ACCESS CODE - ENTITY -----------------------------------
drop table if exists acode_entity;

create table acode_entity (
  acode_id integer not null,
  entity_id integer not null
);

insert into acode_entity (acode_id, entity_id) values (2, 1);
insert into acode_entity (acode_id, entity_id) values (2, 2);
insert into acode_entity (acode_id, entity_id) values (2, 3);
insert into acode_entity (acode_id, entity_id) values (3, 2);
insert into acode_entity (acode_id, entity_id) values (3, 3);
insert into acode_entity (acode_id, entity_id) values (3, 4);
