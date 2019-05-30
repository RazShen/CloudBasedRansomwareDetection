import opcodes_utils as op_utils
import csv
import os
import numpy
import random
import io
from collections import Counter
# import csv
# # Read from a csv all the answers,
# def get_file_labels(files_directory,files_list, result_file):
#     labels_dict = {row[0]: row[1] for row in csv.reader(open(files_directory + "/" + result_file, "rb"), delimiter=',')}
#     file_labels = []
#     for my_file in files_list:
#         pass
#
#

# Receive opcodes for a file and return the corresponding ngram.
def make_ngrams_from_opcodes(file_opcodes, ngram_size):
    return [tuple(file_opcodes[x:x + ngram_size]) for x in range(len(file_opcodes) - ngram_size + 1)]


# Receive an ngram list and all possible ngrams, return the corresponding feature vector
def make_feature_vector(file_ngrams, all_ngrams):
    features = [0] * len(all_ngrams)
    sum_features = 0.0
    for i in range(len(all_ngrams)):
        features[i] = file_ngrams.count(all_ngrams[i])
        sum_features += features[i]
    for i in range(len(all_ngrams)):
        features[i] = float(features[i])/sum_features
    return features


# Receive dictionary filename:opcode return dictionary filename:feature vector.
def features_vector(files_opcodes, ngram_size, n_grams_file_path):
    files_ngrams = {file_name: make_ngrams_from_opcodes(files_opcodes[file_name], ngram_size) for file_name in
                    files_opcodes}
    all_ngrams = Counter()
    for file_name in files_ngrams:
        for ngram in files_ngrams[file_name]:
            all_ngrams[ngram] += 1
    all_ngrams = all_ngrams.most_common(500)
    all_ngrams = [t[0] for t in all_ngrams]
    
    with open(n_grams_file_path, "w") as n_grams_file:
        for n_gram in all_ngrams:
            n_grams_file.write(str(n_gram)+"\n")
    files_features = {file_name: make_feature_vector(files_ngrams[file_name], all_ngrams) for file_name in
                      files_opcodes}
    return files_features


'''
read labels of the csv
'''
def read_labels(results_directory):
    file_name_and_label_dict = {}
    for line in csv.reader(open(results_directory + "/trainLabels.csv", "rb"), delimiter=","):
        if line[0] + ".bytes" in os.listdir(results_directory):
            file_name_and_label_dict[line[0]] = line[1]
    for file_name in os.listdir(results_directory):
        if file_name[:-6] not in file_name_and_label_dict and str(file_name).endswith("bytes"):
            file_name_and_label_dict[file_name[:-6]] = 0
    return file_name_and_label_dict

'''
create numpy array of the features and the labels
'''
def feature_label_arrays(feature_dictionary, label_dictionary):
    feature_array = []
    label_array = []
    for file_name in feature_dictionary.keys():
        feature_array.append(feature_dictionary[file_name])
        label_array.append(label_dictionary[file_name])
    return numpy.array(feature_array), numpy.array(label_array)

'''
randomaly seperate to train and test by the number of classes
'''
def seperate_to_train_and_test(features, labels, test_size= 0.4, num_of_classes = 2):
    test_len = int(len(features)*test_size)
    n= int(test_len/num_of_classes)
    train_ftr = list(features)
    train_lbl = list(labels)
    test_ftr = []
    test_lbl = []
    for i in range(0,num_of_classes):
        c = 0
        for x, y in zip(features, labels):
            if y == i:
                test_ftr.append(x)
                test_lbl.append(y)
                c+=1
                if c == n:
                    break
    # delete test from ftr
    for x,y in zip(test_ftr,test_lbl):
        train_ftr.remove(x)
        train_lbl.remove(y)
    # the remaining elements
    sub_len = test_len-len(test_ftr)
    for i in range(0,sub_len):
        temp = random.randint(0, len(train_ftr)-1)
        test_ftr.append(train_ftr[temp])
        test_lbl.append(train_lbl[temp])
        del train_ftr[temp]
        del train_lbl[temp]
    return train_ftr, test_ftr, train_lbl, test_lbl

