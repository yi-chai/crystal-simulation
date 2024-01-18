import pandas as pd
from pathlib import Path
import numpy as np
import json
import os

#filelist = ['em0901.gro']

dir_path = r'./grofiles'
filelist = []

for file in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, file)):
        filelist.append(file)

filelist = sorted(filelist)


def adjust(column, spaces):
    data[column] = data[column].astype(str)
    data[column] = data[column].str.rjust(spaces)


def threedecimalpoint(column):
    data[column] = data[column].astype(str)
    data[column] = data[column].apply(lambda x: f'{float(x):.3f}')

try:
    os.mkdir('./editedfiles/')

except:
    pass
try:
    os.mkdir('./tempfiles/')
except:
    pass

try:
    os.mkdir('./resultfiles/')
except:
    pass


for filename in filelist:
    newfile = './editedfiles/edited_' + Path(filename).stem + '.gro'
    tempfile = './tempfiles/tempfile_' + Path(filename).stem + '.txt'
    resultfile = './resultfiles/results_' + Path(newfile).stem + '.txt'
    filename = './grofiles/' + filename

    open(tempfile, 'w')
    open(resultfile, 'w')
    open(newfile, 'w')

    try:
        print('Reading ' + filename + '...\n')

        with open(filename, 'r') as file:
            lines = file.readlines()

        head = str(lines[0] + '\n' + lines[1] + '\n')
        dimensions = str('\n' + lines.pop(-1))

        lines = lines[2:]

        residue = lines[0][5:9]

        print('Residue: ' + residue + '\n')

        modified_lines = [line[:15] + ' ' + line[15:] if line else '' for line in lines]

        with open(tempfile, 'w') as file:
            file.writelines(modified_lines)

        data = pd.read_csv(tempfile, header=None, delim_whitespace=True)
        df2 = pd.DataFrame()
        df = pd.DataFrame()

        count = 1

        print('Expanding box...\n')

        while True:
            res = str(count) + residue
            df = data[data[0].isin([res])]

            sd3 = df[3].std()
            sd4 = df[4].std()
            sd5 = df[5].std()

            if sd3 > 1:
                df.loc[df[3] < 2, 3] += 10
            if sd4 > 1:
                df.loc[df[4] < 2, 4] += 10
            if sd5 > 1:
                df.loc[df[5] < 2, 5] += 10

            df2 = pd.concat([df2, df])

            count += 1

            if df.empty:
                break

        data = df2

        threedecimalpoint(3)
        threedecimalpoint(4)
        threedecimalpoint(5)

        adjust(0, 9)
        adjust(1, 5)
        adjust(2, 4)
        adjust(3, 7)
        adjust(4, 7)
        adjust(5, 7)

        datalines = []

        datalines.insert(len(data), data.to_string(index=False, header=False))

        print('Creating expanded GROMACS file...\n')

        with open(newfile, 'w') as f:
            f.write('mol in water\n')
            f.write(str(len(data)) + '\n')
            datalines = ''.join(datalines)
            f.write(datalines)

        with open(newfile, 'r') as file:
            allines = file.readlines()

        with open(newfile, 'w') as file:
            for fline in allines:
                fline = fline[:15] + fline[16:]
                file.write(fline)
            file.write(dimensions + '\n')

        print('File created (' + newfile + ')\n')

        ##

        headerList = ['residue', 'atom', 'n', 'x', 'y', 'z', 'length', 'xangle', 'yangle', 'zangle']

        with open(newfile, 'r') as file:
            lines = file.readlines()

        lines = lines[2:]

        modified_lines = [line[:15] + ' ' + line[15:] if line else '' for line in lines]

        with open(resultfile, 'w') as file:
            file.writelines(modified_lines)

        data = pd.read_csv(resultfile, header=None, skiprows=0, delim_whitespace=True)

        data = data[data[1].isin(['C17', 'C21'])]
        print(data)

        print('Calculating backbone vector with respect to all-axes...\n')

        data[6] = data[3].diff()
        data[7] = data[4].diff()
        data[8] = data[5].diff()

        del data[3]
        del data[4]
        del data[5]

        data = data[data[1].isin(['C17'])]

        data[9] = ''
        data[10] = ''
        data[11] = ''
        data[12] = ''

        data.columns = headerList

        print('Calculating backbone lengths...\n')

        data['length'] = np.linalg.norm(data[['x', 'y', 'z']] * 10, axis=1)

        data['xangle'] = np.rad2deg(np.arccos(data['x'] / (data['length'] / 10)))
        data['yangle'] = np.rad2deg(np.arccos(data['y'] / (data['length'] / 10)))
        data['zangle'] = np.rad2deg(np.arccos(data['z'] / (data['length'] / 10)))

        data['xangle'] = data['xangle'].apply(lambda x: x - 180 if x >= 180 else x)
        data['yangle'] = data['yangle'].apply(lambda x: x - 180 if x >= 180 else x)
        data['zangle'] = data['zangle'].apply(lambda x: x - 180 if x >= 180 else x)

        sd_of_xangle = data['xangle'].std()
        sd_of_yangle = data['yangle'].std()
        sd_of_zangle = data['zangle'].std()

        print(data['yangle'].median())

        meanmagnitude = data['length'].mean()

        del data['atom']
        del data['n']

        threedecimalpoint('x')
        threedecimalpoint('y')
        threedecimalpoint('z')

        datalines = []

        datalines.insert(0, data.to_string(index=False, header=True) + '\n')

        information = {'source': Path(filename).stem,
                       'Standard Deviation of X-Angle': sd_of_xangle,
                       'Standard Deviation of Y-Angle': sd_of_yangle,
                       'Standard Deviation of Z-Angle': sd_of_zangle,
                       'Average Length of Backbone (A)': meanmagnitude}

        print('Generating results...\n')

        with open(resultfile, 'w') as f:
            f.write(json.dumps(information))
            f.write('\n\n')
            datalines = ''.join(datalines)
            f.write(datalines)

        os.remove(tempfile)

        print('Result file created (' + resultfile + ')\n')
        print('-----------------------------------------------------------\n')

    except ValueError:
        print('Error. Check your files.')

    except TypeError:
        print('Error. Check your files.')

    except FileNotFoundError:
        print('File not found.')

    except Exception as e:
        print('Error. Check your files')
