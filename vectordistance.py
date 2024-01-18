import numpy as np
import pandas as pd
import os
from pathlib import Path
import json
import matplotlib.pyplot as plt
import seaborn as sns

grodir = r'./grofiles/'
grofiles = []


def extract_dict_from_file(filename):
    with open(filename, 'r') as f:
        first_line = f.readline().strip()
        return json.loads(first_line)


for file in os.listdir(grodir):
    if os.path.isfile(os.path.join(grodir, file)):
        grofiles.append(file)

grofiles = sorted(grofiles)

count = 0


def intermoleculardistances():
    for grofile in grofiles:
        with open('./editedfiles/edited_' + Path(grofile).stem + '.gro', 'r') as file:
            lines = file.readlines()

        lines = lines[2:-2]

        modified_lines = [line[:15] + ' ' + line[15:] if line else '' for line in lines]

        with open('./tempfiles/tempvectordistance_' + Path(grofile).stem + '.txt', 'w') as file:
            file.writelines(modified_lines)

        df2 = pd.read_csv('./tempfiles/tempvectordistance_' + Path(grofile).stem + '.txt', header=None,
                          delim_whitespace=True)
        allcarbon = df2[df2[1].str.contains('C')].reset_index(drop=True)
        df2 = df2[df2[1].isin(['C17'])].reset_index()

        data = pd.DataFrame(index=None)

        data['name'] = df2[0]
        data['x'] = df2[3]
        data['y'] = df2[4]
        data['z'] = df2[5]

        resultdata = pd.DataFrame()

        i = 0

        while i < len(data):
            current_minimum = float(10000)

            residuenum1 = data['name'].iloc[i]
            allcarbon1 = allcarbon[allcarbon[0].isin([residuenum1])].reset_index(drop=True)
            print("Current residue: " + residuenum1)

            x1 = data['x'].iloc[i]
            y1 = data['y'].iloc[i]
            z1 = data['z'].iloc[i]

            n = 0

            def distancebetweenatoms(atom1, atom2):
                d = np.sqrt(
                    pow(allcarbon1.loc[allcarbon1[1] == atom1, 3].item() - allcarbon2.loc[allcarbon2[1] == atom2, 3].item(), 2) +
                    pow(allcarbon1.loc[allcarbon1[1] == atom1, 4].item() - allcarbon2.loc[allcarbon2[1] == atom2, 4].item(), 2) +
                    pow(allcarbon1.loc[allcarbon1[1] == atom1, 5].item() - allcarbon2.loc[allcarbon2[1] == atom2, 5].item(), 2)
                )
                return d

            while n < len(data):
                res2 = data['name'].iloc[n]
                if res2 == residuenum1:
                    distance = 0

                else:
                    allcarbon2 = allcarbon[allcarbon[0].isin([res2])].reset_index(drop=True)
                    meanlist = []
                    meanlist.append(distancebetweenatoms('C17', 'C17'))
                    meanlist.append(distancebetweenatoms('C17', 'C16'))
                    meanlist.append(distancebetweenatoms('C17', 'C20'))
                    meanlist.append(distancebetweenatoms('C17', 'C21'))

                    distance = sum(meanlist) / len(meanlist)

                if distance == 0.00000000:
                    pass
                elif distance < current_minimum:
                    current_minimum = distance
                    residuenum2 = data['name'].iloc[n]
                    print("new minimum found: " + str(distance) + " with " + residuenum2)
                    x2 = data['x'].iloc[n]
                    y2 = data['y'].iloc[n]
                    z2 = data['z'].iloc[n]

                    minimumdistance = distance *10

                n += 1

            allcarbon1 = allcarbon[allcarbon[0].isin([residuenum1])].reset_index(drop=True)
            allcarbon2 = allcarbon[allcarbon[0].isin([residuenum2])].reset_index(drop=True)

            checkdistance1 = distancebetweenatoms('C17', 'C17')
            checkdistance2 = distancebetweenatoms('C17', 'C16')
            checkdistance3 = distancebetweenatoms('C17', 'C21')
            checkdistance4 = distancebetweenatoms('C17', 'C20')

            checks = [checkdistance1, checkdistance2, checkdistance3, checkdistance4]
            checks = sorted(checks)

            distancelist = []

            mol1order = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
                         'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20',
                         'C21', 'C22']

            if min(checks) == checkdistance1:
                print('checkdistance1')
                mol2order = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
                             'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20',
                             'C21', 'C22']

            elif min(checks) == checkdistance2:
                print('checkdistance2')
                mol2order = ['C2', 'C1', 'C6', 'C5', 'C4', 'C3', 'C10', 'C9', 'C8', 'C7',
                             'C14', 'C13', 'C12', 'C11', 'C18', 'C17', 'C16', 'C15', 'C22', 'C21',
                             'C20', 'C19']

            elif min(checks) == checkdistance3:
                print('checkdistance3')
                mol2order = ['C13', 'C12', 'C11', 'C9', 'C8', 'C14', 'C7', 'C5', 'C4', 'C10',
                             'C3', 'C2', 'C1', 'C6', 'C19', 'C20', 'C21', 'C22', 'C15', 'C16',
                             'C17', 'C18']

            elif min(checks) == checkdistance4:
                print('checkdistance4')
                mol2order = ['C12', 'C13', 'C14', 'C8', 'C9', 'C11', 'C10', 'C4', 'C5', 'C7',
                             'C6', 'C1', 'C2', 'C3', 'C22', 'C21', 'C20', 'C19', 'C18', 'C17',
                             'C16', 'C15']

            else:
                print("unknown")
                mol2order = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
                             'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20',
                             'C21', 'C22']

            for m in mol1order:
                distancelist.append(distancebetweenatoms(m, mol2order[mol1order.index(m)]))

            meanatomicdistance = (sum(distancelist) / len(distancelist))*10
            print(meanatomicdistance)

            if i % 100 == 0:
                print(str(i) + " molecules analysed")

            dataadd = {'res1': residuenum1,
                       'x1': x1, 'y1': y1, 'z1': z1,
                       'res2': residuenum2,
                       'x2': x2, 'y2': y2, 'z2': z2,
                       'distance': minimumdistance,
                       'meandistanceatom': meanatomicdistance}

            resultdata = resultdata._append(dataadd, ignore_index=True)
            data.reset_index(drop=True, inplace=True)

            print(residuenum1 + " and " + residuenum2 + " = " + str(minimumdistance))
            i += 1

        datalines = []

        datalines.insert(len(resultdata), resultdata.to_string(index=True, header=True))

        information = {'source': Path(grofile).stem,
                       'Mean': resultdata['meandistanceatom'].mean(),
                       'Median': resultdata['meandistanceatom'].median(),
                       'Min': resultdata['meandistanceatom'].min(),
                       'Max': resultdata['meandistanceatom'].max()}

        with open('./resultfiles/intermolecular_' + Path(grofile).stem + '.txt', 'w') as f:
            f.write(json.dumps(information))
            f.write('\n\n')
            datalines = ''.join(datalines)
            f.write(datalines)

        os.remove('./tempfiles/tempvectordistance_' + Path(grofile).stem + '.txt')
        print(Path(grofile).stem + " done")

    dicts = [extract_dict_from_file('./resultfiles/intermolecular_' + Path(grofile).stem + '.txt') for grofile in
             grofiles]

    table = pd.DataFrame(dicts)

    x = table["source"]
    x = x.apply(lambda text: text.replace('run0', 'Original'))
    x = x.apply(lambda text: text.replace('run', ''))

    print(table)

    name = './resultfiles/intermolecularsummary_' + Path(grofiles[0]).stem + '_to_' + Path(grofiles[-1]).stem + '.txt'

    with open(name, 'w') as f:
        f.writelines(table.to_string())

intermoleculardistances()

def plot_kdeplot(run=0):
    count = 0

    dfs = [pd.read_csv('./resultfiles/intermolecular_' + Path(grofile).stem + '.txt', skiprows=2, delim_whitespace=True)
           for grofile in grofiles]

    data = pd.DataFrame()

    for dataframe in dfs:
        if count == 0:
            dfs[count]['filenumber'] = 'Original'
            data = pd.concat([data, dfs[count]], ignore_index=True)

        else:
            dfs[count]['filenumber'] = str(count)
            data = pd.concat([data, dfs[count]], ignore_index=True)

        count += 1

    kdecolors = ['y', 'deeppink', 'green', 'blue', 'orange', 'grey', 'purple']

    if run == 0:
        filename = str('./plots/interkde_' + 'distance' + '_original.png')
        runquery = 'Original'
    else:
        filename = str('./plots/interkde_' + 'distance' + '_' + str(run) + '.png')
        runquery = str(run)

    plt.figure(figsize=(6, 4), dpi=80)
    sns.kdeplot(data.loc[data['filenumber'] == runquery, 'distance'], color=kdecolors[run],
                label='Run ' + str(run), alpha=.4)

    plt.tick_params(labelbottom=True, bottom=True)
    plt.xlabel("Intermolecular distance (A)", fontsize='large', weight="bold")
    plt.ylabel("Density", fontsize='large', weight="bold")
    plt.xlim([0, data['distance'].max()])
    plt.ylim([0, 0.1])

    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print('Saved ' + filename)


def plot_kdeplotstacked():
    count = 0
    dfs = [pd.read_csv('./resultfiles/intermolecular_' + Path(grofile).stem + '.txt', skiprows=2, delim_whitespace=True)
           for grofile in grofiles]

    data = pd.DataFrame()

    for dataframe in dfs:
        if count == 0:
            dfs[count]['filenumber'] = 'Original'
            data = pd.concat([data, dfs[count]], ignore_index=True)

        else:
            dfs[count]['filenumber'] = str(count)
            data = pd.concat([data, dfs[count]], ignore_index=True)

        count += 1

    kdecolors = ['y', 'deeppink', 'green', 'blue', 'orange', 'grey', 'purple']

    filename = str('./plots/interkdeallzoomed_distance.png')

    plt.figure(figsize=(6, 4), dpi=80)

    sns.kdeplot(data.loc[data['filenumber'] == "Original", 'meandistanceatom'], color=kdecolors[0],
                label='Original', alpha=.4)

    for i in range(count):
        sns.kdeplot(data.loc[data['filenumber'] == str(i), 'meandistanceatom'], color=kdecolors[i],
                    label='Run ' + str(i), alpha=(i + 3) / 10)

    plt.xlabel('Intermolecular distance (A)', weight='bold', fontsize='large')
    plt.ylabel("Density", weight='bold', fontsize='large')
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    print(data['meandistanceatom'].max())

    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

