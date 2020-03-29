import pandas as pd
import string
import matplotlib.pyplot as plt
import numpy as np


class FixedDose():
    def __init__(self, data):
        self.data = data
        self.regret_dict = {}
        self.incorrect = {}

    def compute_performance_score(self):
        hits = 0
        current_regret = 0
        incorrect_count = 0

        for i, row in self.data.iterrows():
            real_dose = float(row['Therapeutic Dose of Warfarin'])

            if 21 <= real_dose <= 49:
                hits += 1
                regret = 0
            else:
                regret = 1
                incorrect_count += 1

            current_regret += regret
            self.regret_dict[i] = current_regret
            if i == 0:
                self.incorrect[i] = incorrect_count / 1
            else:
                self.incorrect[i] = incorrect_count / i

        print('Fixed dose performance score: {:.2f}%'.format(hits * 100 / len(self.data)))

    def get_performance(self):
        return (self.regret_dict, self.incorrect)


class ClinicalDosingAlgorithm():
    def __init__(self, data):
        self.data = data
        self.regret_dict = {}
        self.incorrect = {}

    def compute_performance_score(self):
        hits = 0
        current_regret = 0
        incorrect_count = 0
        total = 0

        for i, row in self.data.iterrows():

            if row['PharmGKB Subject ID'] == 'PA126718538':
                t = ''

            age = row['Age']
            # Be strict about missing data
            if pd.isna(age):
                continue

            if '-' in age:
                age_range = age.split('-')
                age = int(age_range[0]) / 10
            else:
                age = int(age.strip(string.punctuation)) / 10

            height = row['Height (cm)']

            if pd.isna(height):
                continue

            weight = row['Weight (kg)']

            if pd.isna(weight):
                continue

            race = row['Race']

            asian = african_american = unknown = 0
            if race == 'Asian':
                asian = 1
            elif race == 'Black or African American':
                african_american = 1
            elif race == 'Unknown':
                unknown = 1

            enzyme_inducer = 0
            carbamazepine = row['Carbamazepine (Tegretol)']
            phenytoin = row['Phenytoin (Dilantin)']
            rifampin = row['Rifampin or Rifampicin']

            if (not pd.isna(carbamazepine) and float(carbamazepine) > 0) or \
                    (not pd.isna(phenytoin) and float(phenytoin) > 0) or \
                    (not pd.isna(rifampin) and float(rifampin) > 0):
                enzyme_inducer = 1

            amiodarone = row['Amiodarone (Cordarone)']

            amiodarone = 0
            if not pd.isna(amiodarone) and float(amiodarone) > 0:
                amiodarone = 1

            # Dose can be computed
            value = (
                4.0376
                - 0.2546 * age
                + 0.0118 * height
                + 0.0134 * weight
                - 0.6752 * asian
                + 0.4060 * african_american
                + 0.0443 * unknown
                + 1.2799 * enzyme_inducer
                - 0.5695 * amiodarone
            )

            value = value ** 2
            real = float(row['Therapeutic Dose of Warfarin'])

            def convert_dose(raw_number):
                if raw_number < 21:
                    return 0
                elif 21 <= raw_number <= 49:
                    return 1
                else:
                    return 2

            real_value = convert_dose(real)
            model_value = convert_dose(value)

            if real_value == model_value:
                hits += 1
                regret = 0
            else:
                regret = 1
                incorrect_count += 1

            total += 1

            current_regret += regret
            self.regret_dict[i] = current_regret
            if i == 0:
                self.incorrect[i] = incorrect_count / 1
            else:
                self.incorrect[i] = incorrect_count / i


        print('Clinical Dosing performance scores: {:.2f}%'.format(hits * 100 / total))

    def get_performance(self):
        return (self.regret_dict, self.incorrect)


if __name__ == '__main__':
    print('Baselines performance\n')
    data = pd.read_csv('../data/warfarin_filled.csv')

    #fixedDose = FixedDose(data)
    #fixedDose.compute_performance_score()
    #regret, incorrect = fixedDose.get_performance()

    clinicalDosing = ClinicalDosingAlgorithm(data)
    clinicalDosing.compute_performance_score()
    #regret, incorrect = clinicalDosing.get_performance()

    '''
    x_data = np.array(list(regret.keys()))
    x_values = np.array(list(regret.values()))
    x2_data = np.array(list(incorrect.keys()))
    x2_values = np.array(list(incorrect.values()))

    plt.suptitle('Clinical dosing')
    #plt.plot(x_data, x_values, label='incorrect')
    plt.plot(x2_data, x2_values, label='incorrect')
    plt.xlabel('timestep')
    plt.ylabel('incorrect')
    plt.legend()
    plt.show()
    '''




