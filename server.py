# server.py

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sys import argv
import json

from midi import save_midi_file, push_to_s3


"""
Author: David Goldstein
Date : 12/13/18
License : MIT

Simple server for creating and storing midi files
"""

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        try:
            fileName = "my file in folder"
            save_midi_file(fileName)
            print "uploading '" + fileName + "' to s3"
            url = push_to_s3(fileName)
            data = {
                'url' : url
            }
            print data
            self.wfile.write(data)
        except Exception as e:
            self.wfile.write("Error : " + str(e))
            self.send_response(500)
            raise e

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # set headers
        self._set_headers()
        # try to parse body
        body = None
        try :
            bodyAsString = self.rfile.read(int(self.headers['Content-Length']))
            body = json.loads(bodyAsString)
        except Exception as e:
            self.wfile.write("Error : " + str(e))
            self.send_response(500)
            raise e

        self.send_response(200)            
        self.end_headers()

        self.wfile.write(body)
        
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