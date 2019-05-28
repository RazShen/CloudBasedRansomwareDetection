import socket  # Import socket module
import json
import signatures
import delivery
import retrieve_analysis

# cloud based ransomware detection

PATH = 'inspect.exe'
port = 12317  # Reserve a port for your service every new transfer wants a new port or you must wait.
s = socket.socket()  # Create a socket object
host = "172.18.37.79"  # Get local machine name
s.bind((host, port))  # Bind to the port
s.listen(5)  # Now wait for client connection.
print('Server listening....')

while True:
    conn, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    print('Start receiving file from', addr)
    with open(PATH, 'wb') as f:
        print('Temp exe file opened')
        print('receiving data...')

        while True:
            try:
                conn.settimeout(5.0)
                data = conn.recv(2048)
                # print('data=%s', (data))

                # write data to a file
                f.write(data)
            except socket.timeout:
                break
    print('Finished receiving file from', addr)

    # sbx_scanning_results = get_result_of_bytes_file('hex_bytes_to_inspect')
    this_id = delivery.investigate(PATH)
    grade, signatures, screen = retrieve_analysis.get_grade_by_id(this_id)
    if not grade:
        grade = 0
    if not signatures:
        signatures = ""
    if not screen:
        screen = ""
    print("Sandbox analyzing results is: " + str(grade))
    conn.send(str(grade))
    print('Done sending result')

    # do this only if found ransomware, else send " "
    print('Start sending signatures results to the user')
    signatures_to_send = "\n".join(signatures)
    print(signatures_to_send)
    signatures_to_send = "{:<4000}".format(signatures_to_send)
    print(len(signatures_to_send.encode('utf-8')))
    conn.send(str(signatures_to_send))
    print('Finished sending signatures results to the user')

    print('Start sending screeshot to user')
    scrnsht = open(screen, 'rb')
    l = scrnsht.read(2048)
    while (l):
        conn.sendall(l)
        l = scrnsht.read(2048)
    print('Finished sending screenshot to user')
    conn.close()
