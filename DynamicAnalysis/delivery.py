from cuckoo.core.database import Database
from cuckoo.misc import decide_cwd
import time
import subprocess
import os
import signal
import threading
import requests

CUCKOO_DIR = "~/.cuckoo"
decide_cwd(CUCKOO_DIR)
CREATE_SNAPSHOT = "VBoxManage snapshot User1 take cuckoo"
REMOVE_SNAPSHOT = "VBoxManage snapshot User1 delete cuckoo"
CALL_CUCKOO = "cuckoo submit "
KILL_CUCKOO = "ps -ef | grep cuckoo | awk '{print $2}' | xargs kill"

def threaded(func):
    subprocess.call(func, shell=True)


def my_call(func):
    # newpid = os.fork()
    # if newpid == 0:
    #     subprocess.call(func, shell=True)
    #     exit()
    # else:
    #     return newpid
    t = threading.Thread(target=threaded, args=(func,))
    t.start()
    # thread.start_new_thread(threaded, func)
    return 0


def investigate(file_path):
    # Clone our Clean snapshot
    my_call("VBoxManage startvm User1")
    time.sleep(52)
    subprocess.call(CREATE_SNAPSHOT, shell=True)
    time.sleep(2)

    task_id = -1
    my_call("cuckoo")
    # web = my_call("cuckoo api")
    # TODO implement
    # Send the file to cuckoo
    time.sleep(2)
    db = Database()
    db.connect()
    task_id = db.add_path(file_path)
    # a = subprocess.check_output(CALL_CUCKOO + file_path, shell= True)
    #a = subprocess.call(CALL_CUCKOO + file_path, shell=True)
    print "The id is " + str(task_id)
    # wait until it finishes running    subprocess.check_output(CREATE_SNAPSHOT)
    status = None
    while status != 'reported':
        lst = db.list_tasks()
        status = lst[0].status
        time.sleep(1)
    print "Reported"

    # THIS IS NOT THE CUCKOO PID!!!!
    # os.kill(newpid, signal.SIGTERM)
    # according to the ID, get the reports from this system.
    subprocess.call(REMOVE_SNAPSHOT, shell=True)
    # subprocess.call(KILL_CUCKOO, shell=True)
    kp = subprocess.Popen(["ps", "-ef"], stdout=subprocess.PIPE)
    grep = subprocess.Popen(["grep", "cuckoo"],stdin=kp.stdout, stdout=subprocess.PIPE)
    awk = subprocess.Popen(["awk", "{print $2}"],stdin=grep.stdout, stdout=subprocess.PIPE)
    kill = subprocess.Popen(["xargs", "kill"],stdin=awk.stdout, stdout=subprocess.PIPE)
    kp.stdout.close()
    grep.stdout.close()
    awk.stdout.close()
    return task_id
#
# for i in "abcdefghijklmnopqrstuvwxyz":
#     try:
#         investigate("/home/user/Desktop/sandboxing/ransomwares/" + i)
#     except:
#         print "Skipping..."

# Stages:    Save file.
#            Investigate
#            Grade
#            Signatures
#            return all to server.