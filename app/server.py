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
    db.row_factory = dict_factory
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
    db.row_factory = dict_factory
    cur = db.execute('select * from acode order by id')
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
    role_id = request.args.get('role_id')
    acode_id = request.args.get('acode_id')
    db.row_factory = dict_factory
    if role_id and acode_id:
        cur = db.execute('select * from role_acode where role_id = :role_id and acode_id = :acode_id',
                         {'role_id': role_id, 'acode_id': acode_id})
    elif role_id:
        cur = db.execute('select * from role_acode where role_id = :role_id', {'role_id': role_id})
    elif acode_id:
        cur = db.execute('select * from role_acode where acode_id = :acode_id', {'acode_id': acode_id})
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
    return jsonify(data)


@app.route('/api/data', methods=['PUT'])
def put_data():
    if not request.json:
        abort(400)
    cur = db.cursor()
    cur.execute('delete from role')
    for role in request.json["role"]:
        cur.execute('insert into role (id, extid, charid, name) values (?, ?, ?, ?)',
                    [role['extid'], role['extid'], role['charid'], role['name']])
    cur.execute('delete from acode')
    for acode in request.json["acode"]:
        cur.execute('insert into acode (id, extid, charid, name) values (?, ?, ?, ?)',
                    [acode['id'], acode['extid'], acode['charid'], acode['name']])
    cur.execute('delete from role_acode')
    for role_acode in request.json["role_acode"]:
        cur.execute('insert into role_acode (role_id, acode_id) values (?, ?)',
                    [role_acode['role_id'], role_acode['acode_id']])
    db.commit()
    return jsonify({}), 201

