import os
import logging

from flask import Flask, g, jsonify, abort, request, make_response
from gevent.wsgi import WSGIServer
from .utilities import setup_logger, get_db, dict_factory
from .config import CONFIG


app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIGURATION', 'default')
app.config.from_object(CONFIG[config_name])
setup_logger()
db = get_db(app)
logger = logging.getLogger(__name__)


def main():
    try:
        http_server = WSGIServer(('0.0.0.0', 8080), app, log=logging, error_log=logging)
        http_server.serve_forever()
    except Exception as exc:
        logger.error(exc.message)
    finally:
        pass


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# -------------------------------------------------------------------------------------------------
#  ROLE
# -------------------------------------------------------------------------------------------------


@app.route('/api/role', methods=['GET'])
def get_roles():
    id = request.args.getlist('id')
    db.row_factory = dict_factory
    if len(id) > 0:
        sql = 'select * from role where id in ({0}) order by id'.format(','.join('?' for _ in id))
        cur = db.execute(sql, id)
    else:
        cur = db.execute('select * from role order by id')
    roles = cur.fetchall()
    return jsonify(roles)


@app.route('/api/role/search', methods=['GET'])
def search_roles():
    if not request.args or len(request.args) == 0:
        return ''
    name_query = '%'+request.args.get('q','')+'%'

    db.row_factory = dict_factory
    cur = db.execute('select * from role    \
        where name   like :name_query       \
           or charid like :name_query       \
           or extid  like :name_query       \
        order by id',
        {'name_query': name_query}
     )
    roles = cur.fetchall()
    return jsonify(roles)


@app.route('/api/role/<int:role_id>', methods=['GET'])
def get_role(role_id):
    db.row_factory = dict_factory
    cur = db.execute('select * from role where id = :role_id', {'role_id': role_id})
    role = cur.fetchone()
    if role is None:
        abort(404)
    else:
        return jsonify(role)


@app.route('/api/role', methods=['POST'])
def create_role():
    if not request.json or not 'extid' in request.json or not 'charid' in request.json:
        abort(400)
    cur = db.cursor()
    cur.execute('insert into role (extid, charid, name) values (?, ?, ?)',
                 [request.json['extid'], request.json['charid'], request.json.get('name', "")])
    db.commit()
    role = {
        'id': cur.lastrowid,
        'extid': request.json['extid'],
        'charid': request.json['charid'],
        'name': request.json.get('name', "")
    }
    return jsonify(role), 201


@app.route('/api/role/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    if not request.json:
        abort(400)
    if 'extid' in request.json and type(request.json['extid']) != int:
        abort(400)
    if 'charid' in request.json and type(request.json['charid']) != str:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    db.row_factory = dict_factory
    cur = db.execute('select * from role where id = :role_id', {'role_id': role_id})
    role = cur.fetchone()
    if role is None:
        abort(404)
    role['extid'] = request.json.get('extid', role['extid'])
    role['charid'] = request.json.get('charid', role['charid'])
    role['name'] = request.json.get('name', role['name'])
    cur.execute("update role set extid=?, charid=?, name=? where id=?",
                (role['extid'], role['charid'], role['name'], role_id))
    db.commit()
    return jsonify(role)


@app.route('/api/role/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    cur = db.execute('delete from role_acode where role_id = :role_id', {'role_id': role_id})
    role_acode = cur.rowcount
    cur = db.execute('delete from role where id = :role_id', {'role_id': role_id})
    db.commit()
    if cur.rowcount == 1:
        return jsonify({'result': True, 'role_acode': role_acode})
    else:
        abort(404)


# -------------------------------------------------------------------------------------------------
#  ACCESS CODE
# -------------------------------------------------------------------------------------------------


@app.route('/api/acode', methods=['GET'])
def get_acodes():
    id = request.args.getlist('id')
    db.row_factory = dict_factory
    if len(id) > 0:
        sql = 'select * from acode where id in ({0}) order by id'.format(','.join('?' for _ in id))
        cur = db.execute(sql, id)
    else:
        cur = db.execute('select * from acode order by id')
    acodes = cur.fetchall()
    return jsonify(acodes)


@app.route('/api/acode/search', methods=['GET'])
def search_acodes():
    if not request.args or len(request.args) == 0:
        return ''
    name_query = '%'+request.args.get('q','')+'%'

    db.row_factory = dict_factory
    cur = db.execute('select * from acode   \
        where name   like :name_query       \
           or charid like :name_query       \
           or extid  like :name_query       \
        order by id',
        {'name_query': name_query}
     )
    acodes = cur.fetchall()
    return jsonify(acodes)


@app.route('/api/acode/<int:acode_id>', methods=['GET'])
def get_acode(acode_id):
    db.row_factory = dict_factory
    cur = db.execute('select * from acode where id = :acode_id', {'acode_id': acode_id})
    acode = cur.fetchone()
    if acode is None:
        abort(404)
    else:
        return jsonify(acode)


@app.route('/api/acode', methods=['POST'])
def create_acode():
    if not request.json or not 'extid' in request.json or not 'charid' in request.json:
        abort(400)
    cur = db.cursor()
    cur.execute('insert into acode (extid, charid, name) values (?, ?, ?)',
                 [request.json['extid'], request.json['charid'], request.json.get('name', "")])
    db.commit()
    acode = {
        'id': cur.lastrowid,
        'extid': request.json['extid'],
        'charid': request.json['charid'],
        'name': request.json.get('name', "")
    }
    return jsonify(acode), 201


@app.route('/api/acode/<int:acode_id>', methods=['PUT'])
def update_acode(acode_id):
    if not request.json:
        abort(400)
    if 'extid' in request.json and type(request.json['extid']) != int:
        abort(400)
    if 'charid' in request.json and type(request.json['charid']) != str:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    db.row_factory = dict_factory
    cur = db.execute('select * from acode where id = :acode_id', {'acode_id': acode_id})
    acode = cur.fetchone()
    if acode is None:
        abort(404)
    acode['extid'] = request.json.get('extid', acode['extid'])
    acode['charid'] = request.json.get('charid', acode['charid'])
    acode['name'] = request.json.get('name', acode['name'])
    cur.execute("update acode set extid=?, charid=?, name=? where id=?",
                (acode['extid'], acode['charid'], acode['name'], acode_id))
    db.commit()
    return jsonify(acode)


@app.route('/api/acode/<int:acode_id>', methods=['DELETE'])
def delete_acode(acode_id):
    cur = db.execute('delete from role_acode where acode_id = :acode_id', {'acode_id': acode_id})
    role_acode = cur.rowcount
    cur = db.execute('delete from acode where id = :acode_id', {'acode_id': acode_id})
    db.commit()
    if cur.rowcount == 1:
        return jsonify({'result': True, 'role_acode': role_acode})
    else:
        abort(404)


# -------------------------------------------------------------------------------------------------
#  ROLE - ACCESS CODE RELATION
# -------------------------------------------------------------------------------------------------


@app.route('/api/role-acode', methods=['GET'])
def get_role_acode():
    role_id = request.args.getlist('role_id')
    acode_id = request.args.getlist('acode_id')
    db.row_factory = dict_factory
    if len(role_id) > 0 and len(acode_id) > 0:
        sql = 'select * from role_acode where role_id in ({0}) and acode_id in ({1})'\
            .format(','.join('?' for _ in role_id), ','.join('?' for _ in acode_id))
        cur = db.execute(sql, role_id + acode_id)
    elif len(role_id) > 0:
        sql = 'select * from role_acode where role_id in ({0})'.format(','.join('?' for _ in role_id))
        cur = db.execute(sql, role_id)
    elif len(acode_id) > 0:
        sql = 'select * from role_acode where acode_id in ({0})'.format(','.join('?' for _ in acode_id))
        cur = db.execute(sql, acode_id)
    else:
        cur = db.execute('select * from role_acode')
    roles = cur.fetchall()
    return jsonify(roles)


@app.route('/api/role-acode', methods=['POST'])
def create_role_acode():
    if not request.json or not 'role_id' in request.json or not 'acode_id' in request.json:
        abort(400)
    cur = db.cursor()
    cur.execute('insert into role_acode (role_id, acode_id) values (?, ?)',
                 [request.json['role_id'], request.json['acode_id']])
    db.commit()
    role_acode = {
        'role_id': request.json['role_id'],
        'acode_id': request.json['acode_id']
    }
    return jsonify(role_acode), 201


@app.route('/api/role-acode', methods=['DELETE'])
def delete_role_acode():
    if not request.json or not 'role_id' in request.json or not 'acode_id' in request.json:
        abort(400)
    cur = db.execute('delete from role_acode where role_id = :role_id and acode_id = :acode_id',
                     {'role_id': request.json['role_id'], 'acode_id': request.json['acode_id']})
    db.commit()
    if cur.rowcount > 0:
        return jsonify({'result': cur.rowcount})
    else:
        abort(404)


# -------------------------------------------------------------------------------------------------
#  DATA DUMP & LOAD
# -------------------------------------------------------------------------------------------------


@app.route('/api/data', methods=['GET'])
def get_data():
    db.row_factory = dict_factory
    data = dict()
    data["role"] = db.execute("select * from role order by id").fetchall()
    data["acode"] = db.execute("select * from acode order by id").fetchall()
    data["role_acode"] = db.execute("select * from role_acode order by role_id, acode_id").fetchall()
    data["entity"] = db.execute("select * from entity order by id").fetchall()
    data["entity_appl"] = db.execute("select * from entity_appl order by entity_id").fetchall()
    data["entity_ctx"] = db.execute("select * from entity_ctx order by entity_id").fetchall()
    data["entity_mtyp"] = db.execute("select * from entity_mtyp order by entity_id").fetchall()
    data["entity_task"] = db.execute("select * from entity_task order by entity_id").fetchall()
    data["entity_wfc"] = db.execute("select * from entity_wfc order by entity_id").fetchall()
    data["wfc_status"] = db.execute("select * from wfc_status order by meta_typ_id, status_id").fetchall()
    data["acode_entity"] = db.execute("select * from acode_entity order by acode_id, entity_id").fetchall()
    data["role_role"] = db.execute("select * from role_role order by role_1_id, role_2_id").fetchall()
    return jsonify(data)


@app.route('/api/data', methods=['PUT'])
def put_data():
    if not request.json:
        abort(400)
    cur = db.cursor()
    # role
    cur.execute('delete from role')
    for role in request.json["role"]:
        cur.execute('insert into role (id, extid, charid, name) values (?, ?, ?, ?)',
                    [role['id'], role['extid'], role['charid'], role['name']])
    # access code
    cur.execute('delete from acode')
    for acode in request.json["acode"]:
        cur.execute('insert into acode (id, extid, charid, name) values (?, ?, ?, ?)',
                    [acode['id'], acode['extid'], acode['charid'], acode['name']])
    # role - access code
    cur.execute('delete from role_acode')
    for role_acode in request.json["role_acode"]:
        cur.execute('insert into role_acode (role_id, acode_id) values (?, ?)',
                    [role_acode['role_id'], role_acode['acode_id']])
    # entity
    cur.execute('delete from entity')
    for entity in request.json["entity"]:
        cur.execute('insert into entity (id, type, extid, charid, name) values (?, ?, ?, ?, ?)',
                    [entity['id'], entity['type'], entity['extid'], entity['charid'], entity['name']])
    # entity: application
    cur.execute('delete from entity_appl')
    for entity in request.json["entity_appl"]:
        cur.execute('insert into entity_appl (entity_id) values (?)',
                    [entity['entity_id']])
    # entity: context action
    cur.execute('delete from entity_ctx')
    for entity in request.json["entity_ctx"]:
        cur.execute('insert into entity_ctx (entity_id, parent_id, is_parent, group_id, global_order_by) values (?, ?, ?, ?, ?)',
                    [entity['entity_id'], entity['parent_id'], entity['is_parent'], entity['group_id'], entity['global_order_by']])
    # entity: meta type
    cur.execute('delete from entity_mtyp')
    for entity in request.json["entity_mtyp"]:
        cur.execute('insert into entity_mtyp (entity_id, grp) values (?, ?)',
                    [entity['entity_id'], entity['grp']])
    # entity: task
    cur.execute('delete from entity_task')
    for entity in request.json["entity_task"]:
        cur.execute('insert into entity_task (entity_id, type, meta_out_id) values (?, ?, ?)',
                    [entity['entity_id'], entity['type'], entity['meta_out_id']])
    # entity: workflow
    cur.execute('delete from entity_wfc')
    for entity in request.json["entity_wfc"]:
        cur.execute('insert into entity_wfc (entity_id, meta_typ_id, wfc_action_id, status_id) values (?, ?, ?, ?)',
                    [entity['entity_id'], entity['meta_typ_id'], entity['wfc_action_id'], entity['status_id']])
    # workflow status
    cur.execute('delete from wfc_status')
    for entity in request.json["wfc_status"]:
        cur.execute('insert into wfc_status (meta_typ_id, status_id, charid, name) values (?, ?, ?, ?)',
                    [entity['meta_typ_id'], entity['status_id'], entity['charid'], entity['name']])
    # access code - entity
    cur.execute('delete from acode_entity')
    for acode_entity in request.json["acode_entity"]:
        cur.execute('insert into acode_entity (acode_id, entity_id) values (?, ?)',
                    [acode_entity['acode_id'], acode_entity['entity_id']])
    # role - role
    cur.execute('delete from role_role')
    for role_role in request.json["role_role"]:
        cur.execute('insert into role_role (role_1_id, role_2_id) values (?, ?)',
                    [role_role['role_1_id'], role_role['role_2_id']])
    db.commit()
    return jsonify({}), 201


# -------------------------------------------------------------------------------------------------
#  ENTITY
# -------------------------------------------------------------------------------------------------


@app.route('/api/entity', methods=['GET'])
def get_entities():
    id = request.args.getlist('id')
    db.row_factory = dict_factory
    if len(id) > 0:
        sql = 'select id, type from entity where id in ({0}) order by id'.format(','.join('?' for _ in id))
        cur = db.execute(sql, id)
    else:
        cur = db.execute('select id, type from entity order by id')
    entities = cur.fetchall()
    res = []
    for sql in ["select * from entity_{0}_v where id = {1}".format(entity['type'], entity['id']) for entity in
                entities]:
        cur = db.execute(sql)
        res.append(cur.fetchone())
    return jsonify(res)


@app.route('/api/entity/<int:id>', methods=['GET'])
def get_entity(id):
    db.row_factory = dict_factory
    cur = db.execute('select id, type from entity where id = :id', {'id': id})
    entity = cur.fetchone()
    if entity is None:
        abort(404)
    else:
        sql = "select * from entity_{0}_v where id = {1}".format(entity['type'], entity['id'])
        cur = db.execute(sql)
        entity = cur.fetchone()
        return jsonify(entity)


# -------------------------------------------------------------------------------------------------
#  ACCESS CODE - ENTITY RELATION
# -------------------------------------------------------------------------------------------------


@app.route('/api/acode-entity', methods=['GET'])
def get_acode_entity():
    acode_id = request.args.getlist('acode_id')
    entity_id = request.args.getlist('entity_id')
    db.row_factory = dict_factory
    if len(acode_id) > 0 and len(entity_id) > 0:
        sql = 'select * from acode_entity where acode_id in ({0}) and entity_id in ({1})'\
            .format(','.join('?' for _ in acode_id), ','.join('?' for _ in entity_id))
        cur = db.execute(sql, acode_id + entity_id)
    elif len(acode_id) > 0:
        sql = 'select * from acode_entity where acode_id in ({0})'.format(','.join('?' for _ in acode_id))
        cur = db.execute(sql, acode_id)
    elif len(entity_id) > 0:
        sql = 'select * from acode_entity where entity_id in ({0})'.format(','.join('?' for _ in entity_id))
        cur = db.execute(sql, entity_id)
    else:
        cur = db.execute('select * from acode_entity')
    acode_entity = cur.fetchall()
    return jsonify(acode_entity)


@app.route('/api/acode-entity', methods=['POST'])
def create_acode_entity():
    if not request.json or not 'acode_id' in request.json or not 'entity_id' in request.json:
        abort(400)
    cur = db.cursor()
    cur.execute('insert into acode_entity (acode_id, entity_id) values (?, ?)',
                 [request.json['acode_id'], request.json['entity_id']])
    db.commit()
    acode_entity = {
        'acode_id': request.json['acode_id'],
        'entity_id': request.json['entity_id']
    }
    return jsonify(acode_entity), 201


@app.route('/api/acode-entity', methods=['DELETE'])
def delete_acode_entity():
    if not request.json or not 'acode_id' in request.json or not 'entity_id' in request.json:
        abort(400)
    cur = db.execute('delete from acode_entity where acode_id = :acode_id and entity_id = :entity_id',
                     {'acode_id': request.json['acode_id'], 'entity_id': request.json['entity_id']})
    db.commit()
    if cur.rowcount > 0:
        return jsonify({'result': cur.rowcount})
    else:
        abort(404)


# -------------------------------------------------------------------------------------------------
#  ROLE - ROLE RELATION
# -------------------------------------------------------------------------------------------------


@app.route('/api/role-role', methods=['GET'])
def get_role_role():
    role_1_id = request.args.getlist('role_1_id')
    role_2_id = request.args.getlist('role_2_id')
    db.row_factory = dict_factory
    if len(role_1_id) > 0 and len(role_2_id) > 0:
        sql = 'select * from role_role where role_1_id in ({0}) and role_1_id in ({1})'\
            .format(','.join('?' for _ in role_1_id), ','.join('?' for _ in role_2_id))
        cur = db.execute(sql, role_1_id + role_2_id)
    elif len(role_1_id) > 0:
        sql = 'select * from role_role where role_1_id in ({0})'.format(','.join('?' for _ in role_1_id))
        cur = db.execute(sql, role_1_id)
    elif len(role_2_id) > 0:
        sql = 'select * from role_role where role_2_id in ({0})'.format(','.join('?' for _ in role_2_id))
        cur = db.execute(sql, role_2_id)
    else:
        cur = db.execute('select * from role_role')
    roles = cur.fetchall()
    return jsonify(roles)


@app.route('/api/role-role', methods=['POST'])
def create_role_role():
    if not request.json or not 'role_1_id' in request.json or not 'role_2_id' in request.json:
        abort(400)
    cur = db.cursor()
    cur.execute('insert into role_role (role_1_id, role_2_id) values (?, ?)',
                 [request.json['role_1_id'], request.json['role_2_id']])
    db.commit()
    role_role = {
        'role_1_id': request.json['role_1_id'],
        'role_2_id': request.json['role_2_id']
    }
    return jsonify(role_role), 201


@app.route('/api/role-role', methods=['DELETE'])
def delete_role_role():
    if not request.json or not 'role_1_id' in request.json or not 'role_2_id' in request.json:
        abort(400)
    cur = db.execute('delete from role_role where role_1_id = :role_1_id and role_2_id = :role_2_id',
                     {'role_1_id': request.json['role_1_id'], 'role_2_id': request.json['role_2_id']})
    db.commit()
    if cur.rowcount > 0:
        return jsonify({'result': cur.rowcount})
    else:
        abort(404)
