import socket
import os
dirname = os.path.dirname(__file__)

HOST, PORT = '127.0.0.1', 8082

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.bind((HOST, PORT))
my_socket.listen(1)

print('Serving on port ', PORT)

while True:
    connection, address = my_socket.accept()
    request = connection.recv(1024).decode('utf-8')
    print(request)
    string_list = request.split(' ')  # Split request from spaces

    method = string_list[0]
    #print(method)
    requesting_file = string_list[1]
    #print(requesting_file)

    # print('Client request ', requesting_file)

    myfile = requesting_file.split('?')[0]  # After the "?" symbol not relevent here
    myfile = myfile.lstrip('/')

    if (myfile == ''):
        myfile = os.path.join(dirname,'index.html')   # Load index file as default
    else:
         myfile = os.path.join(dirname,myfile)
    try:
        if (request.find("uname") > 0):
            x = request.split("uname=")
            name = x[1].split('&')
            user = name[0]
            pwd = name[1].split('=')[1]
            if (user == 'admin' and pwd == 'admin'):
                myfile = os.path.join(dirname,'info.html')
            else:
                myfile = os.path.join(dirname,'404.html')
        file = open(myfile, 'rb')  # open file , r => read , b => byte format
        response = file.read()
        file.close()

        header = 'HTTP/1.1 200 OK\n'

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
