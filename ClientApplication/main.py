import detect_new_file_in_folder
import sys


if __name__ == '__main__':
    folder_to_watch = ""
    if (len(sys.argv) > 1):
        w = detect_new_file_in_folder.Watcher(sys.argv[1])
        w.run()
    else:
        print("Usage is 'python main.py <folder_path_to_monitor>")
