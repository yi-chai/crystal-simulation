import pandas as pd
import numpy as np
import os

#filefrom = 'TIPS0.05989356881873897energy.log'
#fileto = 'TIPS.itp'

while True:
    filefrom = input("Enter LOG file: ")
    filefrom = filefrom.strip()

    if filefrom.endswith('.log'):
        break

    else:
        print("Try again! File must end with .log")

while True:
    fileto = input("Enter ITP file: ")
    fileto = fileto.strip()

    if fileto.endswith('.itp'):
        break

    else:
        print("Try again! File must end with .itp")

filefromtemp = 'temp'+str(filefrom)
filetotemp = 'temp'+str(fileto)
filetodupe = 'old'+str(fileto)

word = 'ESP restraint charges:'
word2 = '[ atoms ]'
headerList = ['Atom', 'X', 'Y', 'Z', 'charge', 'Exposure']
headerList2 = ['nr', ' type', 'resnr', ' resid', ' atom', 'cgnr', 'Charge', 'Mass']


def adjust(column, spaces):
    df2[column] = df2[column].astype(str)
    df2[column] = df2[column].str.rjust(spaces)
    return df2[column]


try:
    print("Reading " + filefrom + "...\n")

    with open(filefrom, 'r') as file:
        lines = file.readlines()

        for i, line in enumerate(lines):
            if word in line:
                linenumber = i + 3
            elif 'Total atoms:' in line:
                atoms = line.partition('Total atoms:')[2].strip()
                atoms = int(atoms)

    with open(filefromtemp, 'w') as file:
        file.writelines(lines)

    with open(filefromtemp, 'r') as file:
        dlist = file.readlines()[linenumber:linenumber + atoms]

    with open(filefromtemp, 'w') as file:
        file.writelines(dlist)

    df = pd.read_csv(filefromtemp, delim_whitespace=True, header=None)

    df.columns = headerList

    print("Sorting values...\n")

    df = df.sort_values(by='charge', ascending=False)

    df = df.pop('charge')
    df = df.round(3)

    print("Calculating total charge...\n")

    totalcharge = round(df.sum(), 3)

    print("Total charge: " + str(totalcharge) + '\n')

    changes = totalcharge // 0.001

    i = 0

    if changes > 0:
        print('Resolving charges... [1]\n')
        while i < changes:
            if (i % 2) == 0:
                df1 = df.iloc[-1 - i]
                df1 = df1 - 0.001
                df.iloc[-1 - i] = df1
                totalcharge = round(df.sum(), 3)
                print("Resolved " + str(df.iloc[-1 - i]))

            else:
                df1 = df.iloc[-1 + i]
                df1 = df1 - 0.001
                df.iloc[-1 + i] = df1
                totalcharge = round(df.sum(), 3)
                print("Resolved " + str(df.iloc[-1 + i]))
            i += 1

    elif changes < 0:
        print('Resolving charges... [2]\n')
        changes = abs(int(changes))
        while i < changes:
            if (i % 2) == 0:
                df1 = df.iloc[-1 - i]
                df1 = df1 + 0.001
                df.iloc[-1 - i] = df1
                print("Resolved " + str(df.iloc[-1 - i]))

            else:
                df1 = df.iloc[-1 + i]
                df1 = df1 + 0.001
                df.iloc[-1 + i] = df1
                print("Resolved " + str(df.iloc[-1 + i]))
            i += 1

    print("Calculating total charge...\n")

    total = '%.3f' % round(df.sum(), 3)

    print("Total charge: " + str(total) + '\n')

    df = df.sort_index(ascending=True)

    with open(fileto, 'r') as file:
        filedata = file.read()

    print("Copying " + fileto + " to " + filetodupe + "...\n")

    with open(filetodupe, 'w') as file:
        file.writelines(filedata)

    with open(fileto, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if word2 in line:
                linenumber = i + 2

    with open(filetotemp, 'w') as file:
        file.writelines(filedata)

    with open(filetotemp, 'r') as file:
        dlist = file.readlines()[linenumber:linenumber + atoms]

    with open(filetotemp, 'w') as file:
        file.writelines(dlist)

    df2 = pd.read_csv(filetotemp, delim_whitespace=True, header=None)

    df2.columns = headerList2
    df2 = df2.join(df)
    col_list = list(df2.columns)
    x, y = col_list.index('charge'), col_list.index('Charge')
    col_list[y], col_list[x] = col_list[x], col_list[y]
    dfs = df2[col_list]

    del df2['Charge']
    df2['mass'] = df2['Mass']
    del df2['Mass']
    df2['charge'] = df2.charge.map('{:.3f}'.format)
    df2['mass'] = df2.mass.map('{:.4f}'.format)

    adjust('nr', 5)
    adjust(' type', 5)
    adjust('resnr', 4)
    adjust(' resid', 7)
    adjust(' atom', 6)
    adjust('cgnr', 4)
    adjust('charge', 8)
    adjust('mass', 8)

    i = 0

    df2 = df2.replace(np.nan, ' ', regex=True)

    lines.insert(linenumber, df2.to_string(index=False, header=False) + '\n' + '; total charge of the molecule:  +'
                 + str(total) + '\n')

    print("Writing resolved charges to " + fileto + "...\n")

    with open(fileto, 'w') as file:
        lines = "".join(lines)
        file.write(lines)

    with open(fileto, 'r') as file:
        l1 = file.readlines()

    with open(fileto, 'w') as file:
        for number, line in enumerate(l1):
            if number not in range(linenumber + atoms + 1, linenumber + 2 * (atoms + 1)):
                file.write(line)

    print("Successfully updated charges in " + fileto + ".")

    os.remove(filetotemp)
    os.remove(filefromtemp)

except ValueError:
    print("Error. Check your files.")

except TypeError:
    print("Error. Check your files.")

except FileNotFoundError:
    print("File not found.")

except Exception as e:
    print("Error. Check your files.")
