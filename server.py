# server.py

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sys import argv

from midi import save_midi_file

"""
Author: David Goldstein
Date : 12/13/18
License : MIT

Simple server for creating and storing midi files
"""

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        try:
            save_midi_file()
        except Exception as e:
            self.wfile.write(str(e))

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":


    try:
        port = int(argv[1])
        print "server running on port " + str(port)
        if len(argv) == 2:
            run(port=port)

    except KeyboardInterrupt:
        print 'shutting down'