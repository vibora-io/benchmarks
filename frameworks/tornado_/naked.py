import logging
import signal
import sys
import tornado.web
import tornado.httpserver
import tornado.ioloop
from multiprocessing import cpu_count


class MyHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        self.write('OK')
        self.finish()


if __name__=='__main__':
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
