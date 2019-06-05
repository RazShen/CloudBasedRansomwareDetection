import socket                   # Import socket module
import ml_tagger_from_model
# cloud based ransomware detection
port = 12312                    # Reserve a port for your service every new transfer wants a new port or you must wait.
s = socket.socket()             # Create a socket object
host = "172.18.26.244"   # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.
print('Server listening....')


while True:
    conn, addr = s.accept()     # Establish connection with client.
    print('Got connection from', addr)
    print('Start receiving file from', addr)
    with open('hex_bytes_to_inspect', 'wb') as f:
        print('Temp bytes file opened')
        print('receiving data...')

        while True:
            try:
                conn.settimeout(5.0)
                data = conn.recv(2048)
                #print('data=%s', (data))
                
                # write data to a file
                f.write(data)
            except socket.timeout:
                break
    print('Finished receiving file from', addr)
    ml_scanning_results = ml_tagger_from_model.get_result_of_bytes_file('hex_bytes_to_inspect')
    print("Machine learning scanning results is: " + ml_scanning_results)
    conn.send('Result is: ' + ml_scanning_results)
    print('Done sending result')

    conn.close()