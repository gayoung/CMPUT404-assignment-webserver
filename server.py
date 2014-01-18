import SocketServer
# coding: utf-8

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


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        
        #confirm the request type (should be GET)
        requestType = self.data.split(" ")[0]
        
        #get relative path of requested file
        requestFile = self.data.split(" ")[1]
        
        if(requestType == "GET"):
            self.do_get(requestFile)
    
    #req_file --> relative path of requested file
    #
    # This method process the request to serve a file in either ./www/ or ./www/deep directories
    # and sends the request to the server
    def do_get(self, req_file):
        cssFlag = 0
        
        # adding www to pathing
        if(req_file == "/") | (req_file == "http://127.0.0.1:8080/") | (req_file == "http://127.0.0.1:8080/index.html") |(req_file == "/index.html"):
            req_file  = "www/index.html"
        elif(req_file == "/base.css"):
            cssFlag = 1
            req_file  = "www/base.css"
        elif (req_file == "/deep/index.html") | (req_file == "/deep/"):
            req_file  = "www/deep/index.html"
        elif(req_file == "/deep/deep.css"):
            cssFlag = 1
            req_file  = "www/deep/deep.css"
        else:
            req_file = ""
        
        #load file
        try:
            req_file_ob = open(req_file, 'rb')
            fileContent = req_file_ob.read()
            req_file_ob.close()
            
            if(cssFlag == 1):
                self.sendHeader(200, 'text/css', fileContent)
            else:
                self.sendHeader(200, 'text/html', fileContent)
            self.request.send("\r\n")
            self.request.send(fileContent)
            self.request.close()
        
        # file is not found so give a 404 error
        except Exception as e: 
            self.sendHeader(404, 'text/html', '')
            
    # This method generates the request header to send to the server
    #
    # reqtype is needed to distinguish 404 errors
    # contentType specifies if the file being served is CSS or HTML file
    # fileconent specifies the content to be served (to specify content-length)
    def sendHeader(self, reqtype, contentType, filecontent):        
        # file was not found so generate a 404 error
        if(reqtype == 404):
            self.request.send("HTTP/1.1 404 Not Found \r\n")
        else:
            self.request.send("HTTP/1.1 200 OK \r\n")
            
        self.request.send("Content-Type: "+contentType+"; encoding=utf-8\r\n")
        self.request.send("Content-Length: " + str(len(filecontent)) + "\r\n")
        self.request.send("Connection: keep-alive\r\n")
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)
    
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.server_activate()
    
    server.serve_forever()