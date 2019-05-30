import io
import json

# search for signatures indicating the behavior of the executable (search in signaturesdb.json)
def calculate_signatures_score_and_get_matched_signatures(signature_fp, report_json):
    with open(signature_fp, 'r') as signatures_json:
        sj = signatures_json.read()
        signatures_json_dict = json.loads(sj)
        total_score = 0
        matched_signatures = []
        for signature in signatures_json_dict["full_ransomware_related_signature_list"]:
            severity = signatures_json_dict["full_ransomware_related_signature_list"][signature]["severity"]
            description = signatures_json_dict["full_ransomware_related_signature_list"][signature]["description"]
            for existing_signature in report_json["signatures"]:
                raw_name = existing_signature["description"]
                clear_name = result = ''.join([i for i in raw_name if not i.isdigit()])
                clear_name = clear_name.replace("  "," ")
                if (raw_name == description or clear_name == description):
                    matched_signatures.append(description)
                    total_score += severity
        return total_score, matched_signatures



# report_json_path = "report.json"
# with open(report_json_path, 'r') as my_json_report:
#     js =my_json_report.read()
#     report_dict = json.loads(js)
#     signatures_score, matched_signatures = calculate_signatures_score_and_get_matched_signatures("ransom_signatures_with_severity.json", report_dict)    
#     print(signatures_score)
#     print matched_signatures

