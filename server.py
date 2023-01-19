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

METHOD = 0
PATH = 1
ROOT = "./www"

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        try:
            self.data = self.request.recv(1024).strip()
            print ("Got a request of: %s\n" % self.data)

            request_string_components = self.data.decode("utf-8").split(" ")

            if request_string_components[METHOD] != "GET":
                self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n\r\n",'utf-8'))
                return

            data = ""
            content_type = ""

            path = ROOT + request_string_components[PATH]
            if os.path.exists(path):
                print("it sexisjfs")
                if os.path.isdir(path):
                    files = os.listdir(path)
                    if "index.html" not in resources:
                        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n",'utf-8'))
                        return 
                    data = "READ FILE and determien file type"
                elif os.path.isfile(path):
                    # serve file
                    print("\nIt is a normal file")  

            resources = os.listdir(ROOT + request_string_components[PATH])

            print(resources)

            self.request.sendall(bytearray(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html><html></html>",'utf-8'))
        except Exception as e:
            print(e)
            self.request.sendall(bytearray("HTTP/1.1 500 Internal Server Error\r\n\r\n",'utf-8'))

 
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
