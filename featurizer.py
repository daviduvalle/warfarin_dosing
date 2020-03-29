import numpy as np
import csv
from collections import defaultdict
import constants
import re


class Featurizer():
    def __init__(self):
        self.LABELS = []
        self.NUM_ROWS = 0
        self.NUM_COLS = 0
        self.NUM_COLS_INITIALIZED = False

    def compute(self):
        data, labels, columns_dict, values_dict = self.__load_data()

        # preprocess the diseases
        disease_dict = {}
        key_to_disease_string = {}
        for k in values_dict[constants.DISEASE_LABEL]:
            diseases = map(str.lower, map(str.strip, k.split(';')))
            key_to_disease_string[values_dict[constants.DISEASE_LABEL][k]] = k
            for d in diseases:
                if d not in disease_dict:
                    disease_dict[d] = len(disease_dict)

        self.NUM_ROWS = 5528
        if not self.NUM_COLS_INITIALIZED:
            print('columns {}'.format(len(columns_dict)))
            for k in columns_dict:
                if k in constants.FLOAT_LABELS:
                    #print('Col increase by one {}'.format(k))
                    self.NUM_COLS += 1
                elif k not in constants.IGNORE_LABELS:
                    self.NUM_COLS += len(values_dict[k].items())
                    #print('Col increase by {} due {}'.format(len(values_dict[k].items()), k))
            self.NUM_COLS_INITIALIZED = True

            if constants.INCLUDE_DISEASES:
                self.NUM_COLS += len(disease_dict)

        index_labels = {}
        for k in columns_dict:
            index_labels[columns_dict[k]] = k

        linearized_data = np.zeros((self.NUM_ROWS, self.NUM_COLS))
        print("SHAPE OF DATA:", linearized_data.shape)
        for i, d in enumerate(data):
            write_index = 0
            for j, val in enumerate(d):
                # print('j:{} label: {} val: {}'.format(j, index_labels[j], val))
                if index_labels[j] in constants.FLOAT_LABELS:
                    linearized_data[i, write_index] = val
                    write_index += 1
                elif index_labels[j] == constants.DISEASE_LABEL:
                    diseases = map(str.lower, map(str.strip, key_to_disease_string[val].split(';')))
                    for dis in diseases:
                        linearized_data[i, write_index + disease_dict[dis]] = 1
                    write_index += len(disease_dict)
                elif index_labels[j] in constants.IGNORE_LABELS:
                    continue
                else:
                    assert val == int(val), 'Value must be a value index'
                    linearized_data[i, write_index + int(val)] = 1
                    write_index += len(values_dict[index_labels[j]].items())
            assert write_index == self.NUM_COLS
        return linearized_data, labels

    def __load_data(self):
        with open(constants.WARFARIN_FILE_PATH) as csv_file:
            reader = csv.reader(csv_file, skipinitialspace=True)
            data = []
            labels = []

            rows_parsed = 0
            columns_dict = {}
            values_dict = defaultdict(lambda: {'NA': 0})
            #values_dict = defaultdict(dict)
            label_index = -1
            ignore_columns_past_index = float('inf')

            weights = []
            heights = []

            for i, r in enumerate(reader):
                # Process columns
                if i == 0:
                    for i, c in enumerate(r[1:]):

                        # We got 64 columns
                        print('i: {}, value {}'.format(i, c))

                        if c == constants.LABELS_COLUMN:
                            label_index = i
                        elif c == '':
                            ignore_columns_past_index = min(ignore_columns_past_index, i)
                        else:
                            columns_dict[c] = len(columns_dict)
                            self.LABELS.append(c)
                elif r[0] != '':  # check that subject ID is present
                    rows_parsed += 1
                    row = []
                    adjust = 0
                    add_data = True
                    for i, col_val in enumerate(r[1:]):
                        if i == 65:
                            print('HACK')
                        col_val = col_val.strip()
                        if col_val == 'N/A' or col_val == '':
                            col_val = 'NA'
                        if i == label_index:
                            if col_val == 'NA':
                                add_data = False
                                break
                            label = float(col_val)
                            adjust = 1
                        elif i < ignore_columns_past_index:
                            if self.LABELS[i - adjust] in constants.FLOAT_LABELS:
                                if self.LABELS[i - adjust] == 'Age':
                                    try:
                                        col_val = float(col_val[0])
                                    except:
                                        # age could've been NA or a random date
                                        col_val = 0
                                else:
                                    try:
                                        col_val = float(col_val)
                                    except:
                                        col_val = 0
                                    if col_val != 0:
                                        if self.LABELS[i - adjust] == 'Height (cm)':
                                            heights.append(col_val)
                                        elif self.LABELS[i - adjust] == 'Weight (kg)':
                                            weights.append(col_val)
                                        else:
                                            raise Exception('Should not happen')
                                row.append(col_val)
                                label_class = self.LABELS[i - adjust]
                                if col_val not in values_dict[label_class]:
                                    values_dict[label_class][col_val] = len(values_dict[label_class])
                            else:
                                # Fix warfarin indication here
                                label_class = self.LABELS[i - adjust]
                                if label_class == 'Indication for Warfarin Treatment':
                                    tokens = re.split(r';|or|,', col_val)
                                    for token in tokens:
                                        if token not in values_dict[label_class]:
                                            values_dict[label_class][token] = len(values_dict[label_class])
                                    row.append(values_dict[label_class][token])
                                else:
                                    if col_val not in values_dict[label_class]:
                                        values_dict[label_class][col_val] = len(values_dict[label_class])
                                    row.append(values_dict[label_class][col_val])

                    if add_data:
                        data.append(row)
                        labels.append(label)

            assert len(values_dict.keys()) == len(
                columns_dict.keys()), "length of non-float values and total columns dicts should match"

            data = np.array(data)
            labels = np.array(labels)

            #for d in data:
            #    print(len(d))


            avg_height = np.mean(heights)
            avg_weight = np.mean(weights)
            # Fill missing data with averages
            for i in range(data.shape[0]):
                if data[i][columns_dict['Height (cm)']] == 0:
                    data[i][columns_dict['Height (cm)']] = avg_height
                if data[i][columns_dict['Weight (kg)']] == 0:
                    data[i][columns_dict['Weight (kg)']] = avg_weight

            return data, labels, columns_dict, values_dict


if __name__ == '__main__':
    featurizer = Featurizer()
    data, labels = featurizer.compute()