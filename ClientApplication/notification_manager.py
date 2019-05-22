import webbrowser
import fileinput
from shutil import copyfile
from time import sleep
import os

def notify(file_name,signature_list):
    signature_list_to_present = ["\t<li>" + sign + "</li>" for sign in signature_list]
    signature_list_to_present = "\n".join(signature_list_to_present)
    print(file_name)
    copyfile("maliciousFileFound.html", "present.html")
    with fileinput.FileInput("present.html", inplace=True) as file:
        for line in file:
            print(line.replace("<filename>", file_name), end='')
    copyfile("present.html", "present_final.html")

    with fileinput.FileInput("present_final.html", inplace=True) as file:
        for line in file:
            print(line.replace("<signature_list>", signature_list_to_present), end='')
    url = "present_final.html"
    webbrowser.open_new_tab(url)
    sleep(15)
    os.remove("present.html")
    os.remove("present_final.html")