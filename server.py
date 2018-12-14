# server.py

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sys import argv
import json
import uuid
import os

from midi import create_midi_file, push_to_s3


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

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # set headers
        self._set_headers()
        # try to parse body
        body = None
        values = None
        fileName = str(uuid.uuid1()) + ".mid"
        bpm = None
        outputRange = None
        songBeatLength = None
        try :
            # parse data
            bodyAsString = self.rfile.read(int(self.headers['Content-Length']))
            body = json.loads(bodyAsString)
            values = body["data"]["result"][0]["values"]
            # parse settings
            bpm = body["songSettings"]["bpm"]
            outputRange = body["songSettings"]["outputRange"]
            songBeatLength = body["songSettings"]["songBeatLength"]
        except Exception as e:
            self.wfile.write("Error : " + str(e))
            self.send_response(500)
            raise e

        # create midi file
        try:
            createdFile = create_midi_file(fileName, bpm=bpm, data=values, outputRange=outputRange)
        except Exception as e:
            self.wfile.write("Could not create midi file : " + str(e))
            self.send_response(500)
            raise e

        url = None
        try:
            url = push_to_s3(fileName)
        except Exception as e:
            self.wfile.write("Could not create midi file : " + str(e))
            self.send_response(500)
            raise e            

        print "pushed to s3 {}".format(url)     

        self.wfile.write(url)

        # remove created file
        os.remove(fileName)
        
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