import json
import Gradings
import string

CUCKOO_DIR = "/home/user/.cuckoo/"

WEIGHT = {'sig': 0.35, 'string': 0.1, 'file': 0.2, 'behave': 0.35}


def retrieve_json(task_id):
    analysis_path = CUCKOO_DIR + "storage/analyses/" + str(task_id)
    json_path = analysis_path + "/reports/report.json"
    with open(json_path, 'r') as my_json_report:
        js = my_json_report.read()
        dict = json.loads(js)
        my_json_report.close()
    return dict


def grade(intel, task_id):
    strings_grade = Gradings.grade_strings(intel['strings'])  #
    behaviour_grade = Gradings.grade_behaviour(intel['behavior'])
    files_grade = Gradings.grade_hashed_files(CUCKOO_DIR + "storage/analyses/" + str(task_id) + "/files/")
    signatures_grades, signatures = Gradings.grade_signatures(intel)

    return int(signatures_grades * WEIGHT['sig'] + files_grade * WEIGHT['file'] + behaviour_grade * WEIGHT[
        'behave'] + strings_grade * WEIGHT['string']), signatures


def get_grade_by_id(task_id):
    try:
        dict = retrieve_json(task_id)
        my_grade, sig = grade(dict, task_id)
        return my_grade, sig, dict['screenshots'][-1]['path']
    except:
        print "Skipping..."

