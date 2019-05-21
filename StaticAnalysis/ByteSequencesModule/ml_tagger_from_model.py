import joblib
import opcodes_utils
import ml_utils
import sys

def load_model(model_path):
    xg_model = joblib.load(model_path)
    return xg_model

#Replace a set of multiple sub strings with a new string in main string.
def replace_multiple(main_string, to_be_replaced, new_string):
    # Iterate over the strings to be replaced
    for elem in to_be_replaced :
        # Check if string is in the main string
        if elem in main_string :
            # Replace the string
            main_string = main_string.replace(elem, new_string)
    return  main_string

def get_all_ngrams_from_file(n_gram_file_path):
    # get all ngrams
    all_ngrams = []
    with open(n_gram_file_path, "r") as n_grams_file:
        for line in n_grams_file:
            line = replace_multiple(line, "()' \n","")
            line = tuple(line.split(","))
            all_ngrams.append(line)
    return all_ngrams
    
def predict(xg_model, feature_vector):
    preds = xg_model.predict(feature_vector)
    return preds

def get_result_of_bytes_file(bytes_file_name):
# command line args- xg_model path, all_ngrams_path, path to file bytes
    n_grams_file = "model_data/all_ngrams"
    all_n_grams = get_all_ngrams_from_file(n_grams_file)
    op_codes_list = opcodes_utils.get_opcodes_from_hexa_bytes(bytes_file_name)
    n_grams_list = ml_utils.make_ngrams_from_opcodes(op_codes_list, 4)
    feature_vector = ml_utils.make_feature_vector(n_grams_list, all_n_grams)
    xg_model = load_model("model_data/xg_model")
    prediction = predict(xg_model, feature_vector)
    return prediction[0]