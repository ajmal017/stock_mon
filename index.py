import os,logging

import tornado.web
import tornado.ioloop
import tornado.options
from tornado import gen
import tornado.httpserver

import momoko

from base_handler import BaseHandler
from tick_data import TickDataHandler
from new_stocks import NewStockHandler
from new_high import NewHighHandler
from rpcserver_tornado import RPCServer

db_database = os.environ.get('SM_TEST_DB', 'sm_test')
db_user = os.environ.get('SM_TEST_USER', 'postgres')
db_password = os.environ.get('SM_TEST_PASSWORD', 'Reuters1')
db_host = os.environ.get('SM_TEST_HOST', 'localhost')
db_port = os.environ.get('SM_TEST_PORT', 5432)
enable_hstore = True if os.environ.get('SM_TEST_HSTORE', False) == '1' else False
dsn = 'dbname=%s user=%s password=%s host=%s port=%s' % (
    db_database, db_user, db_password, db_host, db_port)

assert (db_database or db_user or db_password or db_host or db_port) is not None, (
    'Environment variables for the examples are not set. Please set the following '
    'variables: SM_TEST_DB, SM_TEST_USER, SM_TEST_PASSWORD, '
    'SM_TEST_HOST, SM_TEST_PORT')

def init_log():
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='./stock_mon.log',
                filemode='w')
    logger = logging.getLogger()
    logging.info("Current log level is : %s", logging.getLevelName(logger.getEffectiveLevel()))

class OverviewHander(BaseHandler):
        def get(self):
            self.write("""
<ul>
    <li><a href="/query">A single query</a></li>
    <li><a href="/get-new-stock">Get new issued stocks</a></li>
    <li><a href="/connection">Manual connection management</a></li>
</ul>
        """)
            self.finish()

class ConnectionHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        self.http_connection_closed = False
        super(ConnectionHandler, self).__init__(*args, **kwargs)

    @gen.coroutine
    def get(self):
        try:
            connection = yield self.db.getconn()
            with self.db.manage(connection):
                for i in range(5):
                    if self.http_connection_closed:
                        break
                    cursor = yield connection.execute("SELECT pg_sleep(1);")
                    self.write('Query %d results: %s<br>\n' % (i+1, cursor.fetchall()))
                    self.flush()
        except Exception as error:
            self.write(str(error))

        self.finish()

    def on_connection_close(self):
        self.http_connection_closed = True

class QueryHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        if self.db.server_version >= 90200:
            try:
                cursor = yield self.db.execute('SELECT \'{"a": "b", "c": "d"}\'::json;')
                self.write("Query results: %s<br>" % cursor.fetchall())
            except Exception as error:
                self.write(str(error))
        else:
            self.write("json is not enabled")

        self.finish()        
        
def main():
    init_log()
    try:
        tornado.options.parse_command_line()
        application = tornado.web.Application([
                (r'/', OverviewHander),
                (r'/get-tick-data', TickDataHandler),
                (r'/get-new-stock', NewStockHandler),
                (r'/get-new-high', NewHighHandler),
                (r'/query', QueryHandler),
                (r'/connection', ConnectionHandler)
        ], debug = True )

        ioloop = tornado.ioloop.IOLoop.instance()
        application.db = momoko.Pool(
            dsn=dsn,
            size=1,
            max_size=3,
            ioloop=ioloop,
            setsession=("SET TIME ZONE UTC",),
            raise_connect_errors=False,
        )
        
        # this is a one way to run ioloop in sync
        future = application.db.connect()
        ioloop.add_future(future, lambda f: ioloop.stop())
        ioloop.start()

        if enable_hstore:
            future = application.db.register_hstore()
            # This is the other way to run ioloop in sync
            ioloop.run_sync(lambda: future)

        if application.db.server_version >= 90200:
            future = application.db.register_json()
            # This is the other way to run ioloop in sync
            ioloop.run_sync(lambda: future)
        # create http server
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(6888, 'localhost')
        # create json rpc server
        rpc_server = RPCServer()
        rpc_server.listen(8001)
        
        ioloop.start()

    except KeyboardInterrupt:
        print('Exit')

if __name__ == "__main__":
    main()
