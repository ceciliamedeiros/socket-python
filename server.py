import socket
import os
from urllib.error import HTTPError

files_path = os.getcwd()

#Função que ira iniciar o servidor
def start_server():
        host = '192.168.1.115' 
        port = 8080
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(5)

        print("Server is listening on:" + str(host) + ':' + str(port))
        
        while True:
            
            ws, addr = sock.accept()
            request = ws.recv(2000).decode('utf-8')
        
            #Separa a requisição
            arr = request.split(' ')

            #Obtém o método HTTP
            method_http = arr[0]
            #Obtém o patch
            if len(arr) > 1:
                patch = arr[1]

            file = patch.split('?')[0].lstrip('/')
            if(file == ''):
                file = 'homepage.html'

            header = 'HTTP/1.1 200 OK\n'
            try:
                #r: read | b: byte format
                f = open(files_path + '/views/' + file,'rb')
                response = f.read()
 
                header = 'HTTP/1.1 200 OK\r\n'
 
                if(file.endswith(".jpg")):
                    content_type = 'image/jpg'
                elif(file.endswith(".css")):
                    content_type = 'text/css'
                elif(file.endswith(".png")):
                    content_type = 'image/png'
                else:
                    content_type = 'text/html'
 
                header += 'Content-Type: ' + str(content_type) + '\r\n\r\n'
 
            except Exception as e:
                header = 'HTTP/1.1 404 Not Found\n\n'
                response = '<html><body><center><h3>Error 404: File not found</h3><p>This page does not exist</p></center></body></html>'.encode('utf-8')    
            
            final_response = header.encode('utf-8')
            final_response += response
            ws.send(final_response)
            ws.close() 


start_server()
