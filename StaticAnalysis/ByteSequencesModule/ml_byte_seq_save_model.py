"""
Here we implement the model for learning.
"""
import ml_utils 
import opcodes_utils
import xgboost as xgb
from time import time
import numpy as np
import joblib

def learn_with_XGBClassifier(train_data, train_lbl, test_examples, test_lbl, lr=0.22,n_esti=40,seed=123):
    train_time = time()
    xg_cl = xgb.XGBClassifier(objective='multi:softmax', num_class= 2, learning_rate=lr,
                                    n_estimators=n_esti, seed=seed)
    xg_cl.fit(train_data, train_lbl)
    train_time = time() - train_time
    test_time = time()
    preds = xg_cl.predict(test_examples)
    test_time = time() - test_time
    accuracy = float(np.sum(preds == test_lbl)) / test_lbl.shape[0]
    joblib.dump(xg_cl, "model_data/xg_model")
    return {"train time: ": train_time, "test time: ": test_time, "accuracy: ": accuracy*100}

files_path = "real_data"
opcodes_path = "model_data/opcodes"
n_grams_file_path = "model_data/all_ngrams"
file_name_and_list_of_op_codes_dict = opcodes_utils.get_dict_filename_op_codes(files_path, opcodes_path)
file_name_and_feature_vector_dict = ml_utils.features_vector(file_name_and_list_of_op_codes_dict, 4, n_grams_file_path)
file_name_and_true_label_dict = ml_utils.read_labels(files_path)
numpy_features, numpy_lables = ml_utils.feature_label_arrays(file_name_and_feature_vector_dict, file_name_and_true_label_dict)
X_train, X_test, y_train, y_test = ml_utils.seperate_to_train_and_test(numpy_features,numpy_lables)
print (learn_with_XGBClassifier(np.array(X_train), np.array(y_train), np.array(X_test), np.array(y_test)))

pass
