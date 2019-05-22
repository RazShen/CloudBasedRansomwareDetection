import socket                   # Import socket module
import json
import signatures
# cloud based ransomware detection


port = 12313                    # Reserve a port for your service every new transfer wants a new port or you must wait.
s = socket.socket()             # Create a socket object
host = "172.18.27.117"   # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.
print('Server listening....')


while True:
    conn, addr = s.accept()     # Establish connection with client.
    print('Got connection from', addr)
    print('Start receiving file from', addr)
    with open('exe_to_inspect.exe', 'wb') as f:
        print('Temp exe file opened')
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
    # sbx_scanning_results = get_result_of_bytes_file('hex_bytes_to_inspect')
    sbx_scanning_results = 99
    print("Sandbox analyzing results is: " + str(sbx_scanning_results))
    conn.send(str(sbx_scanning_results))
    print('Done sending result')

    # do this only if found ransomware, else send " "
    print('Start sending signatures results to the user')
    signatures_to_send = ""
    with open("/Users/raz.shenkman/Documents/Ransomware_workspace_new/DynamicAnalysis/server/report.json", 'r') as my_json_report:
        js =my_json_report.read()
        report_dict = json.loads(js)
        signatures_score, matched_signatures = signatures.calculate_signatures_score_and_get_matched_signatures("/Users/raz.shenkman/Documents/Ransomware_workspace_new/DynamicAnalysis/server/ransom_signatures_with_severity.json", report_dict)    
        signatures_to_send = "\n".join(matched_signatures)
        print(signatures_to_send)
        signatures_to_send = "{:<4000}".format(signatures_to_send)
        print(len(signatures_to_send.encode('utf-8')))
    conn.send(str(signatures_to_send))

    print('Start sending snapshot to user')
    scrnsht = open("/Users/raz.shenkman/Documents/Ransomware_workspace_new/DynamicAnalysis/server/screenshot", 'rb')
    l = scrnsht.read(2048)
    while(l):
        conn.sendall(l)
        l = scrnsht.read(2048)
    print('Finished sending snapshot to user')


    print('Finished sending signatures results to the user')
    conn.close()