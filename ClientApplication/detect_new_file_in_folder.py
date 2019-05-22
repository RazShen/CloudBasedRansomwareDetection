import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import notification_manager
import ml_exe_to_hexbytes
import ml_client
import sbx_client
import os


SEARCH_DIR = ""

class Watcher:
    def __init__(self, dir_name):
        global SEARCH_DIR

        self.observer = Observer()
        self.dir = dir_name
        SEARCH_DIR = dir_name

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.dir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            # send the file using the FTP server
            # get results and notify accordingly
            full_path_event = SEARCH_DIR + "\\" +os.path.basename(event.src_path)

            saved_bytes_fname = ml_exe_to_hexbytes.get_hexdump_output(full_path_event)
            # ml_result = ml_client.send_file_to_server(saved_bytes_fname)
            sbx_result, signature_list = sbx_client.send_file_to_server(full_path_event)
            # signature_list = ["doing1", "doing2", "doing3"]
            # if ml_result.__contains__("1") and float(sbx_result)*0.01 >= 0.8:
            if float(sbx_result) * 0.01 >= 0.8:
                notification_manager.notify(os.path.basename(event.src_path), signature_list)


