import socket
import os
dirname = os.path.dirname(__file__) # Get dir of present file

HOST, PORT = '127.0.0.1', 8082      # Declare HOST address, using port

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.bind((HOST, PORT))
my_socket.listen(2)

print('Server is on! Serving at port ', PORT)

while True:
    connection, address = my_socket.accept()
    request = connection.recv(1024).decode('utf-8') #Get request
    print(request)
    string_list = request.split(' ')  # Split request from spaces

    try:
        method = string_list[0]      # Method = (GET,POST)
        requesting_file = string_list[1]
        myfile = requesting_file.split('?')[0]  # After the "?" symbol not relevent here
        myfile = myfile.lstrip('/') #Delete the '/' symbol
        
        if (method == "GET"):       #when the method is GET
            if (myfile == ''):      #if the address have no request file
                myfile = os.path.join(dirname, 'index.html')  #Load index.html file as default
                header = 'HTTP/1.1 301 Moved Permanently\nLocation: http://127.0.0.1:8082/index.html\n' #send header to redirect to index.html
            else:
                myfile = os.path.join(dirname, myfile)
                header = 'HTTP/1.1 200 OK\n'
        elif (method == "POST"):    #when the method is POST
            if (request.find("uname") > 0):     #find uname on POST request
                x = request.split("uname=")
                name = x[1].split('&')
                user = name[0]                  #get username on POST request
                pwd = name[1].split('=')[1]     #get password on POST request
                if (user == 'admin' and pwd == 'admin'):    #check if username and password are correct?
                    header = 'HTTP/1.1 301 Moved Permanently\nLocation: http://127.0.0.1:8082/info.html\n'  #redirect to info.html
                    myfile = os.path.join(dirname, 'info.html')
                else:
                    header = 'HTTP/1.1 301 Moved Permanently\nLocation: http://127.0.0.1:8082/404.html\n'   #redirect to 404.html
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
        header = 'HTTP/1.1 301 Moved Permanently\nLocation: http://127.0.0.1:8082/404.html\n'   #handle exception: redirect to 404.html
        myfile = os.path.join(dirname,'404.html')
        file = open(myfile, 'rb')  # open file , r => read , b => byte format
        response = file.read()
        file.close()
        mimetype = 'text/html'
        header += 'Content-Type: ' + str(mimetype) + '\n\n'

    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()
