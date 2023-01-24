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

# constants
METHOD = 0
REQUEST_LINE = 0
PATH = 1
HOST_NAME = 1
HOST = 3
ROOT = "./www"

HTTP_200_STATUS = "HTTP/1.1 200 OK\r\n"
HTTP_301_STATUS = "HTTP/1.1 301 Moved Permanently\r\n"
HTTP_404_STATUS = "HTTP/1.1 404 Not Found\r\n"
HTTP_405_STATUS = "HTTP/1.1 405 Method Not Allowed\r\n"
HTTP_500_STATUS = "HTTP/1.1 500 Internal Server Error\r\n"

def get_host(s):
    components = s.split("\r\n")
    return components[0]

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        try:
            self.data = self.request.recv(1024).strip()
            # print ("Got a request of: %s\n" % self.data)

            headers = self.data.decode("utf-8").split("\r\n")
            print(headers)

            request_line = headers[REQUEST_LINE] 
            request_line_components = request_line.split(" ")

            # get host name
            host_name = ""
            for header in headers:
                if "Host: " in header:
                    host_name = header.split(" ")[HOST_NAME]
                    break

            if request_line_components[METHOD] != "GET":
                self.request.sendall(bytearray(f"{HTTP_405_STATUS}\r\n",'utf-8'))
                return

            data = ""
            content_type = ""
            content_encoding = ""
            content_len = ""

            path = request_line_components[PATH]
            uri = ROOT + path

            # clean path of parent accesses
            uri = uri.replace("../", "")

            if os.path.exists(uri):

                if os.path.isdir(uri):
                    files = set(os.listdir(uri))
                    content_type = ""
                    data = ""
                    appended_slash = False

                    # add trailing /
                    if not uri.endswith("/"):
                        appended_slash = True
                        status_code = HTTP_301_STATUS
                        location = f"Location: http://{host_name + path + '/'}\r\n"
                        self.request.sendall(bytearray(f"{status_code}Content-Type: text/html\r\n{location}",'utf-8'))
                        return

                    if "index.html" in files:
                        f = open(uri + "index.html", "r")
                        content_type = "text/html"
                        data = f.readlines()
                        f.close()

                    elif "index.htm" in files:
                        f = open(uri + "index.htm", "r")
                        content_type = "text/html"
                        data = f.readlines()
                        f.close()

                    else:
                        self.request.sendall(bytearray(f"{HTTP_404_STATUS}\r\n",'utf-8'))
                        return

                    data = "".join(data)
                    status_code = HTTP_200_STATUS
                    location = ""
                    self.request.sendall(bytearray(f"{status_code}Content-Type: text/html\r\n{location}\r\n{data}",'utf-8'))
                    return

                elif os.path.isfile(uri):
                    # serve file
                    f = open(uri, "r")
                    data = f.readlines()
                    f.close()

                    data = "".join(data)

                    if uri.endswith(".css"):
                        content_type = "text/css"
                    elif uri.endswith(".html"):
                        content_type = "text/html"

                    self.request.sendall(bytearray(f"{HTTP_200_STATUS}Content-Type: {content_type}\r\n\r\n{data}",'utf-8'))
                    return
                
                else:
                    self.request.sendall(bytearray(f"{HTTP_500_STATUS}\r\n",'utf-8'))
                    return
                    
            else:
                self.request.sendall(bytearray(f"{HTTP_404_STATUS}\r\n",'utf-8'))
                return

            self.request.sendall(bytearray(f"{HTTP_500_STATUS}Content-Type: text/html\r\n\r\n",'utf-8'))

        except Exception as e:
            print(e)
            self.request.sendall(bytearray(f"{HTTP_500_STATUS}\r\n",'utf-8'))

 
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
