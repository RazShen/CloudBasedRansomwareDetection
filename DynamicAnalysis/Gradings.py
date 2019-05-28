import string
import re
import os
import json

STRINGS_DB = "stringsdb"
REG_DB = "regdb"
FILE_API = "fileAPIdb"
REG_API = "regAPIdb"
CRYPT_API = "cryptAPIdb"
SIGNATURES = "signaturesdb.json"
VOLUME = 1000


def read_db(filename):
    try:
        f = open(filename, 'r')
        content = f.read()
        lines = content.split("\n")
        db = [x.split(";")[2] for x in lines if x]
        f.close()
        return db
    except:
        print "Error reading or parsing the file " + filename + ". Exiting..."
        exit()


def check_string(my_str, suspected):
    for suspect in suspected:
        if suspect.find(my_str) != -1 or my_str.find(suspect) != -1:
            return True
    return False


def load_calls(arr, filename):
    try:
        f = open(filename, 'r')
        content = f.read()
        lines = content.split("\n")
        arr.extend([string.lower(l) for l in lines])
    except:
        print "Error reading or parsing the file " + filename + ". Exiting..."
        exit()


def grade_behaviour(behaviour_dict):
    try:
        reg_keys = behaviour_dict['summary']['regkey_written']
        reg_grade = grade_strings(reg_keys, REG_DB)
    except:
        reg_grade = 0
    file_api = [0]
    crypt_api = [0]
    reg_api = [0]

    load_calls(file_api, FILE_API)
    load_calls(crypt_api, CRYPT_API)
    load_calls(reg_api, REG_API)

    api_calls = behaviour_dict['apistats']
    for group in api_calls:
        for call in api_calls[group]:
            my_call = string.lower(call)
            if my_call in file_api:
                file_api[0] += api_calls[group][call]
            if my_call in crypt_api:
                crypt_api[0] += api_calls[group][call]
            if my_call in reg_api:
                reg_api[0] += api_calls[group][call]
    return min(min(file_api[0] / 150, 50) + min(reg_api[0] / 3, 25) + min(crypt_api[0] / 100, 15) + min(reg_grade,10), 100)


def grade_strings(strings_arr, db=STRINGS_DB):
    strings_arr = [string.lower(str(x)) for x in strings_arr]
    suspecious_strings_list = read_db(db)
    suspecious_strings_list = [string.lower(x) for x in suspecious_strings_list]
    suspected = [x for x in strings_arr if check_string(x, suspecious_strings_list)]
    count_suspected = len(suspected)
    return min(100, 3.5 * count_suspected)


def get_num_of_hashed_files(folder_path):
    l = os.listdir(folder_path)
    c = 0
    for item in l:
        result = re.search(r"[0-9a-f]{10}", item)
        if (result):
            # print item
            c += 1
    # print "There are " + str(c) + " items with hash-based file name"
    return c


def grade_hashed_files(path):
    hashed_files = get_num_of_hashed_files(path)
    # 1000 hashed files(which is more the bait) would give 100
    return min(100, hashed_files / 10)

def grade_signatures(report):
    with open(SIGNATURES, 'r') as signatures_json:
        sj = signatures_json.read()
        signatures_json_dict = json.loads(sj)

        total_score = 0
        matched_signatures = []
        for signature in signatures_json_dict["full_ransomware_related_signature_list"]:
            severity = signatures_json_dict["full_ransomware_related_signature_list"][signature]["severity"]
            description = signatures_json_dict["full_ransomware_related_signature_list"][signature]["description"]
            for existing_signature in report["signatures"]:
                raw_name = existing_signature["description"]
                clear_name = result = ''.join([i for i in raw_name if not i.isdigit()])
                clear_name = clear_name.replace("  "," ")
                if (raw_name == description or clear_name == description):
                    matched_signatures.append(description)
                    total_score += severity
        return total_score, matched_signatures