import pandas as pd


def load_data():
    return pd.read_csv('../data/warfarin.csv')


def remove_unused(raw_data):
    missing_data_indices = raw_data[raw_data['Therapeutic Dose of Warfarin'].isna()].index
    raw_data.drop(missing_data_indices, inplace=True)
    assert len(raw_data) == 5528, 'should have 5528 usable records'


def fill_missing_data(raw_data):
    print('Original data size {}'.format(len(raw_data)))
    missing_count = 0
    white_counter = 0
    asian_counter = 0
    black_counter = 0
    rs9923231 = 'VKORC1 genotype: -1639 G>A (3673); chr16:31015190; rs9923231; C/T'
    rs2359612 = 'VKORC1 genotype: 2255C>T (7566); chr16:31011297; rs2359612; A/G'
    rs9934438 = 'VKORC1 genotype: 1173 C>T(6484); chr16:31012379; rs9934438; A/G'
    rs8050894 = 'VKORC1 genotype: 1542G>C (6853); chr16:31012010; rs8050894; C/G'

    for i, row in raw_data.iterrows():
        current = row[rs9923231]
        if pd.isna(current):

            missing_count += 1
            race = row['Race']
            if race != 'Black or African American' and race != 'Unknown' and row[rs2359612] == 'C/C':
                if race == 'White':
                    white_counter += 1
                if race == 'Asian':
                    asian_counter += 1
                if race == 'Black or African American':
                    black_counter += 1
                raw_data.at[i, rs9923231] = 'G/G'
            elif race != 'Black or African American' and race != 'Unknown' and row[rs2359612] == 'T/T':
                if race == 'White':
                    white_counter += 1
                if race == 'Asian':
                    asian_counter += 1
                if race == 'Black or African American':
                    black_counter += 1
                raw_data.at[i, rs9923231] = 'A/A'
            elif race != 'Black or African American' and race != 'Unknown' and row[rs2359612] == 'C/T':
                if race == 'White':
                    white_counter += 1
                if race == 'Asian':
                    asian_counter += 1
                if race == 'Black or African American':
                    black_counter += 1
                raw_data.at[i, rs9923231] = 'A/G'
            elif row[rs9934438] == 'C/C':
                if race == 'White':
                    white_counter += 1
                if race == 'Asian':
                    asian_counter += 1
                if race == 'Black or African American':
                    black_counter += 1
                raw_data.at[i, rs9923231] = 'G/G'
            elif row[rs9934438] == 'T/T':
                if race == 'White':
                    white_counter += 1
                if race == 'Asian':
                    asian_counter += 1
                if race == 'Black or African American':
                    black_counter += 1
                raw_data.at[i, rs9923231] = 'A/A'
            elif row[rs9934438] == 'C/T':
                if race == 'White':
                    white_counter += 1
                if race == 'Asian':
                    asian_counter += 1
                if race == 'Black or African American':
                    black_counter += 1
                raw_data.at[i, rs9923231] = 'A/G'
            elif race != 'Black or African American' and race != 'Unknown' and row[rs8050894] == 'G/G':
                if race == 'White':
                    white_counter += 1
                if race == 'Asian':
                    asian_counter += 1
                if race == 'Black or African American':
                    black_counter += 1
                raw_data.at[i, rs9923231] = 'G/G'
            elif race != 'Black or African American' and race != 'Unknown' and row[rs8050894] == 'C/C':
                if race == 'White':
                    white_counter += 1
                if race == 'Asian':
                    asian_counter += 1
                if race == 'Black or African American':
                    black_counter += 1
                raw_data.at[i, rs9923231] = 'A/A'
            elif race != 'Black or African American' and race != 'Unknown' and row[rs8050894] == 'C/G':
                if race == 'White':
                    white_counter += 1
                if race == 'Asian':
                    asian_counter += 1
                if race == 'Black or African American':
                    black_counter += 1
                raw_data.at[i, rs9923231] = 'A/G'


    print('Filled for Whites {:.2f}%'.format(white_counter * 100 / missing_count))
    print('Filled for Asians {:.2f}%'.format(asian_counter * 100 / missing_count))
    print('Filled for African American {:.2f}%'.format(asian_counter * 100 / missing_count))
    print('Total missing count {}'.format(missing_count))
    print('Writing to file: ../data/warfarin_filled.csv')
    raw_data.to_csv('../data/warfarin_filled.csv', index=False)


def main():
    raw_data = load_data()
    remove_unused(raw_data)
    fill_missing_data(raw_data)


if __name__ == '__main__':
    main()