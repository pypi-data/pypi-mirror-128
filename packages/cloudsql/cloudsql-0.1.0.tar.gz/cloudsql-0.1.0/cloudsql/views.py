from flask import request, jsonify, abort
import json
import sqlite3

from . import sqlite as db
from . import utilities as ut

from . import auth


@auth.request_is_authenticated
def tables(context):

    conn = db.get_db(context['sqlitepath'])
    
    if request.method == 'GET':
        tables = db.get_tables(conn)
        return jsonify(tables)

    if request.method == 'POST':
        data = json.loads(request.data)
        name = data['name']
        schema = data['schema']
        string_schema = ', '.join(list(map( lambda x: f'{x[0]} {x[1]}', schema.items())))
        query = f'CREATE TABLE {name} ({string_schema});'
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        return '', 200


@auth.request_is_authenticated
def table(context, name):
    
    conn = db.get_db(context['sqlitepath'])

    if name in db.get_tables(conn):

        if request.method == 'GET':

            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            columns, args = ut.parse_args(request.args)

            if not columns:
                columns = '*'
            
            if args:
                conditions = ' AND '.join(map(lambda x: f'{x}=:{x}', args.keys()))
                query = f'SELECT {columns} FROM {name} WHERE {conditions};'
                c.execute(query, args)

            else:
                query = f'SELECT {columns} FROM {name};'
                c.execute(query)
            
            result = []
            for row in c.fetchall():
                result.append(dict(row))
            
            return jsonify(result)

        if request.method == 'POST':
            data = json.loads(request.data)
            query = f'''INSERT INTO {name} ({", ".join([k for k in data.keys()])}) VALUES ({", ".join(["?" for _ in data])})'''
            c = conn.cursor()
            c.execute(query, list(data.values()))
            conn.commit()
            return '', 200

        if request.method == 'DELETE':
            query = f'DROP TABLE {name};'
            c = conn.cursor()
            c.execute(query)
            return ''

    else:
        abort(404)

