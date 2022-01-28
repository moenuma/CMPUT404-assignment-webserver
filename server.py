#  coding: utf-8 
import socketserver
import os

# Copyright 2022 Abram Hindle, Eddie Antonio Santos, Moe Numasawa
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()

        # empty data
        if not self.data:
            return

        print ("Got a request of: %s\n" % self.data)

        parse_data = self.data.decode("utf-8").split("\r\n")
        method, path, http = parse_data[0].split(" ")

        wwwdir = "www" + path
        header = ""

        # Methods it cannot handle
        if method != "GET":
            header = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            self.request.sendall(header.encode())

        # if the given path is a directory
        if os.path.isdir(wwwdir):
            # path doesn't end with /
            if wwwdir[-1] != '/':
                header = "HTTP/1.1 301 Moved Permanently\r\n"
                header += f"Location: http://127.0.0.1:8080{path}/\r\n\r\n"
                wwwdir += '/'

            wwwdir += "index.html"

        # reads a file requested
        try:
            f = open(wwwdir, 'rb')
            response = f.read()
            f.close()
            header += "HTTP/1.1 200 OK\r\n"

            # mime-type
            if wwwdir.endswith('html'):
                mimetype = "text/html"
            elif wwwdir.endswith('css'):
                mimetype = "text/css"
            
            header += "Content-Type: " + mimetype + "\r\n\r\n"
            all_response = header.encode() + response
        
        # no file found
        except Exception as e:
            header = "HTTP/1.1 404 Not Found\r\n\r\n"
            all_response = header.encode()

        self.request.sendall(all_response)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()