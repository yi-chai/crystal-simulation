import pandas as pd
import numpy as np
import os

#filefrom = '3.xyz'
#fileto = '3.pdb'

while True:
    filefrom = input("Enter XYZ file: ")
    filefrom = filefrom.strip()

    if filefrom.endswith('.xyz'):
        break

    else:
        print("Try again! File must end with .xyz")

while True:
    fileto = input("Enter PDB file: ")
    fileto = fileto.strip()

    if fileto.endswith('.pdb'):
        break

    else:
        print("Try again! File must end with .pdb")

filefromtemp = "temp" + str(filefrom)
filetotemp = "temp" + str(fileto)
filetodupe = "old" + str(fileto)

word = 'TeraChem'
word2 = 'UNCLASSIFIED'
headerList = ['Atom', 'x', 'y', 'z']
headerList2 = ["AUTHOR", "num", "atom", "TIPS", "num2", "X", "Y", "Z", "num3", "num4", "atom2"]


def swap_columns(dfs, col1, col2):
    col_list = list(dfs.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    dfs = dfs[col_list]
    return dfs


def adjust(colname, spaces):
    df2[colname] = df2[colname].astype(str)
    df2[colname] = df2[colname].str.rjust(spaces)
    return df2[colname]


try:
    with open(filefrom, 'r') as file:
        lines = file.readlines()
        atoms = len(lines) - 2
        for line in lines:
            if line.find(word) != -1:
                n = lines.index(line) + 1

    with open(filefrom, 'r') as file:
        dlist = file.readlines()[n:n + atoms]

    with open(filefromtemp, 'w') as file:
        file.writelines(dlist)

    df = pd.read_csv(filefromtemp, header=None, delim_whitespace=True)
    df.columns = headerList

    df = df.round(3)

    with open(fileto, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.find(word2) != -1:
                n = lines.index(line) + 4

    with open(filetodupe, 'w') as file:
        file.writelines(lines)

    with open(fileto, 'r') as file:
        dlist = file.readlines()[n:n + atoms]

    with open(filetotemp, 'w') as file:
        file.writelines(dlist)


    df2 = pd.read_csv(filetotemp, header=None, delim_whitespace=True)
    df2.columns = headerList2

    df2 = df2.join(df)
    df2 = swap_columns(df2, 'X', 'x')
    df2 = swap_columns(df2, 'Y', 'y')
    df2 = swap_columns(df2, 'Z', 'z')

    del df2["X"]
    del df2["Y"]
    del df2["Z"]
    del df2["Atom"]

    df2["x"] = df2.x.map('{:.3f}'.format)
    df2["y"] = df2.y.map('{:.3f}'.format)
    df2["z"] = df2.z.map('{:.3f}'.format)
    df2["num3"] = df2.num3.map('{:.2f}'.format)
    df2["num4"] = df2.num4.map('{:.2f}'.format)

    adjust("num", 4)
    adjust("atom", 4)
    adjust("num2", 4)
    adjust("x", 11)
    adjust("y", 7)
    adjust("z", 7)
    adjust("num3", 5)
    adjust("num4", 5)
    adjust("atom2", 11)

    i = 0

    with open(filetodupe) as f:
        lines = f.readlines()
        while i < atoms+1:
            del lines[4]
            i += 1

    with open(fileto, "r") as f:
        lines = f.readlines()

    df2 = df2.replace(np.nan, ' ', regex=True)

    lines.insert(n, df2.to_string(index=False, header=False) + "\n")

    with open(fileto, 'w') as file:
        del lines[5:105]
        lines = "".join(lines)
        file.write(lines)

    os.remove(filefromtemp)
    os.remove(filetotemp)

except ValueError:
    print("Error. Check your files.")

except TypeError:
    print("Error. Check your files.")

except FileNotFoundError:
    print("File not found.")

except Exception as e:
    print("Error. Check your flies")
