import socket                   # Import socket module

signatures_list = ""


def send_file_to_server(filename):
    global signatures_list
    s = socket.socket()             # Create a socket object
    host = "172.18.37.81"  #Ip address that the TCPServer  is there
    port = 12317                    # Reserve a port for your service every new transfer wants a new port or you must wait.
    s.connect((host, port))
    f = open(filename, 'rb')
    l = f.read(2048)
    print("Started sending data")
    while (l):
        s.sendall(l)
       # print('Sent ', repr(l))
        l = f.read(2048)
    print("Stopped sending data")
    print("Receiving Sandbox analysis results...")
    result = s.recv(2)
    print("Chances of being a Ransomware by Sandbox analysis: " + result.decode("UTF-8"))
    print("Receiving signatures list ")
    raw_sign_list = s.recv(4000)
    print("Finished receiving signatures list ")
    signatures_list = str(raw_sign_list.decode("UTF-8")).rstrip().split("\n")
    print(raw_sign_list)
    print("Receiving Sandbox Screenshot...")
    with open("cuckoo_output.jpg", 'wb') as scrnsht:
        while True:
            try:
                s.settimeout(5.0)
                data = s.recv(2048)
                if not data:
                    break
            except socket.timeout:
                break
            scrnsht.write(data)
    print("Finished Receiving Sandbox Screenshot...")

    s.close()
    print('Done with Sandbox analysis')
    return int(result.decode("UTF-8")), signatures_list
