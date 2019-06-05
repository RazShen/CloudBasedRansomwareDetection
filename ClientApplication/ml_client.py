import socket                   # Import socket module


def send_file_to_server(filename):
    s = socket.socket()             # Create a socket object
    host = "172.18.26.244"  #Ip address that the TCPServer  is there
    port = 12312                     # Reserve a port for your service every new transfer wants a new port or you must wait.
    s.connect((host, port))
    f = open(filename, 'rb')
    l = f.read(2048)
    print("Started sending data")
    while (l):
        s.sendall(l)
       # print('Sent ', repr(l))
        l = f.read(2048)
    print("Stopped sending data")
    print("Receiving machine learning analysis results")
    result = s.recv(100)
    print("Result of machine learning analysis: " + result.decode("UTF-8"))
    s.close()
    print('Done with Machine learning analysis')
    return result.decode("UTF-8")
