#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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

# https://emalsha.wordpress.com/2016/11/24/how-create-http-server-using-python-socket-part-ii/
# https://stackoverflow.com/questions/4246762/python-code-to-consolidate-css-into-html/23190429


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        parse_data = self.data.decode("utf-8").split("\r\n")
        method, path, http = parse_data[0].split(" ")
        path = "www" + path
        header = ""

        if method != "GET" and method != "POST":
            header = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            self.request.sendall(header.encode())

        if os.path.isdir(path):
            if path[-1] != '/':
                header = "HTTP/1.1 301 Moved Permanently\r\n"
                path += '/'

            path += "index.html"

        try:
            
            file = open(path, 'rb')
            response = file.read()
            header += "HTTP/1.1 200 OK\r\n"
            if path.endswith('html'):
                mimetype = "text/html"
            elif path.endswith('css'):
                mimetype = "text/css"
            header += "Content-Type: " + mimetype + "\r\n\r\n"
            all_response = header.encode() + response
        
        except Exception as e:
            header = "HTTP/1.1 404 Not Found\r\n\r\n"
            all_response = header.encode()

        print(all_response)
        self.request.sendall(all_response)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
