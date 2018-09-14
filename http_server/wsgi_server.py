import socket
import sys
import StringIO


class WSGIServer(object):
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(self, server_address):
        self.server_socket = server_socket = socket.socket(self.address_family, self.socket_type)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(server_address)
        server_socket.listen(self.request_queue_size)

        host, port = self.server_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self.headers_set = []
        self.request_method = ""
        self.path = ""
        self.request_version = ""
        self.application = None

    def set_app(self, app):
        self.application = app

    def serve_forever(self):
        server_socket = self.server_socket
        while True:
            self.client_connection, client_address = server_socket.accept()
            self.handle_one_request()

    def parse_request(self, text):
        """
        GET / HTTP/1.1
        Host: localhost:8888
        Connection: keep-alive
        User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36
        Upgrade-Insecure-Requests: 1
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
        Accept-Encoding: gzip, deflate, br
        Accept-Language: zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2
        """
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip("\r\n")
        self.request_method, self.path, self.request_version = request_line.split()


    def handle_one_request(self):
        self.request_data = request_data = self.client_connection.recv(1024)
        print ''.join(
            '< {line}\n'.format(line=line)
            for line in request_data.splitlines()
        )
        print "request: ", self.request_data

        self.parse_request(request_data)

        env = self.get_environ()

        result = self.application(env, self.start_response)

        self.finish_response(result)

    def get_environ(self):
        env = {}
        env["wsgi.version"] = (1, 0)
        env["wsgi.url_scheme"] = "http"
        env["wsgi.input"] = StringIO.StringIO(self.request_data)
        env["wsgi.errors"] = sys.stderr
        env["wsgi.multithread"] = False
        env["wsgi.multiprocess"] = False
        env["wsgi.run_once"] = False
        env["REQUEST_METHOD"] = self.request_method
        env["PATH_INFO"] = self.path
        env["SERVER_NAME"] = self.server_name
        env["SERVER_PORT"] = str(self.server_port)
        return env

    def start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ("Date", "Fri, 11 May 2018 18:00:00 GMT"),
            ("Server", "WSGIServer 0.2")
        ]
        self.headers_set = [status, response_headers + server_headers]

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = "HTTP/1.1 {status}\r\n".format(status=status)
            for header in response_headers:
                response += "{0}: {1}\r\n".format(*header)
            response += "\r\n"
            for data in result:
                response += data

            print "".join("> {line}\n".format(line=line) for line in response.splitlines())

            self.client_connection.sendall(response)
        finally:
            self.client_connection.close()


SERVER_ADDRESS = (HOST, PORT) = '', 8888


def make_server(server_address, app):
    server = WSGIServer(server_address)
    server.set_app(app)
    return server


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Provide a WSGI application object as module:callable")

    # flaskapp:app
    app_path = sys.argv[1]
    module, application = app_path.split(":")
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print "WSGIServer: Serving HTTP on port {port} ...\n".format(port=PORT)
    httpd.serve_forever()



