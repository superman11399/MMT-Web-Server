import socket
import os
dirname = os.path.dirname(__file__)

HOST, PORT = '127.0.0.1', 8082

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.bind((HOST, PORT))
my_socket.listen(2)

print('Serving on port ', PORT)

while True:
    connection, address = my_socket.accept()
    request = connection.recv(1024).decode('utf-8')
    print(request)
    string_list = request.split(' ')  # Split request from spaces

    try:
        method = string_list[0]
        requesting_file = string_list[1]
        # print('Client request ', requesting_file)

        myfile = requesting_file.split('?')[0]  # After the "?" symbol not relevent here
        myfile = myfile.lstrip('/')

        if (myfile == ''):
            myfile = os.path.join(dirname, 'index.html')  # Load index file as default
        else:
            myfile = os.path.join(dirname, myfile)
        header = 'HTTP/1.1 200 OK\n'
        if (request.find("uname") > 0):
            x = request.split("uname=")
            name = x[1].split('&')
            user = name[0]
            pwd = name[1].split('=')[1]
            if (user == 'admin' and pwd == 'admin'):
                header = 'HTTP/1.1 301 Moved Permanently\nLocation: http://127.0.0.1:8082/info.html\n'
                myfile = os.path.join(dirname, 'info.html')
            else:
                header = 'HTTP/1.1 301 Moved Permanently\nLocation: http://127.0.0.1:8082/404.html\n'
                myfile = os.path.join(dirname,'404.html')
        file = open(myfile, 'rb')  # open file , r => read , b => byte format
        response = file.read()
        file.close()

        if (myfile.endswith(".jpg")):
            mimetype = 'image/jpg'
        elif (myfile.endswith(".css")):
            mimetype = 'text/css'
        elif (myfile.endswith(".png")):
            mimetype = 'image/png'
        else:
            mimetype = 'text/html'

        header += 'Content-Type: ' + str(mimetype) + '\n\n'

    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not foundssss</h3><p>Go back to home page</p></center></body></html>'.encode(
            'utf-8')

    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()