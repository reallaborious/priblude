import sys

p=sys.version_info[0]

if p == 2:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
else:
    from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        response_message = "It works with python " + str(p)
        if p == 2:
            self.wfile.write(response_message)
        else:
            self.wfile.write(response_message.encode())
        
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Serving HTTP on port {port}...'.format(port=port))
    httpd.serve_forever()

if __name__ == '__main__':
    run()
