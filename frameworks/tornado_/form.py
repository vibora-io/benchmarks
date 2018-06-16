import sys
import ujson
import tornado.web
import tornado.httpserver
import tornado.ioloop
from multiprocessing import cpu_count


class MyHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def post(self):
        self.write(ujson.dumps({'count': len(self.request.files)}))
        self.finish()


if __name__=='__main__':
    import logging
    import signal
    app = tornado.web.Application([(r'/', MyHandler)], autoreload=False)


    def sig_handler(sig, x):
        tornado.ioloop.IOLoop.instance().add_callback(shutdown)


    def shutdown():
        server.stop()
        io_loop = tornado.ioloop.IOLoop.instance()
        io_loop.stop()


    server = tornado.httpserver.HTTPServer(app)
    server.bind(sys.argv[2])
    server.start(cpu_count())

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    tornado.ioloop.IOLoop.current().start()

