from flask import g, jsonify

from . import views as v


class CloudSQL():

    def __init__(self, dbpath, url_prefix='', api_key=None):
        self.url_prefix = url_prefix
        self.db_context = {'sqlitepath': dbpath}
        if api_key:
            self.db_context['api_key'] =  api_key


    def serve(self, app):
        
        @app.route(f'{self.url_prefix}/tables', methods=['GET', 'POST'])
        def tables():
            return v.tables(self.db_context)

        @app.route(f'{self.url_prefix}/table/<name>', methods=['GET', 'POST', 'DELETE'])
        def table(name):
            return v.table(self.db_context, name)

        @app.teardown_appcontext
        def close_connection(exception):
            db = getattr(g, '_database', None)
            if db is not None:
                db.close()

        @app.errorhandler(Exception)
        def handle_error(e):
            print(e)
            return jsonify(error=str(e))
