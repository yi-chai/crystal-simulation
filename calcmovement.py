import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

grodir = r'./grofiles/'
grofiles = []

for file in os.listdir(grodir):
    if os.path.isfile(os.path.join(grodir, file)):
        grofiles.append(file)

grofiles = sorted(grofiles)


def check_value(val):
    if abs(val) > 8:
        if val < 0:
            return -(val + 10)
        if val > 0:
            return val - 10
    else:
        return val


def calculate_movement():
    df = pd.DataFrame()
    maglist = []
    i = 0

    for file in grofiles:
        file = grodir + file
        with open(file, 'r') as f:
            lines = f.readlines()

        lines = lines[2:-2]
        modified_lines = [line[:15] + line[20:] if line else '' for line in lines]

        with open('./tempfiles/temp_' + Path(file).stem + '.txt', 'w') as f:
            f.writelines(modified_lines)

        df1 = pd.read_csv('./tempfiles/temp_' + Path(file).stem + '.txt', header=None, delim_whitespace=True)
        df1 = df1[df1[1].isin(['C17'])]

        colnumber = 'x' + str(i)
        df[colnumber] = df1[2]

        i += 1

    i = 0

    for file in grofiles:
        file = grodir + file
        with open(file, 'r') as f:
            lines = f.readlines()

        lines = lines[2:-2]
        modified_lines = [line[:15] + line[20:] if line else '' for line in lines]

        with open('./tempfiles/temp_' + Path(file).stem + '.txt', 'w') as f:
            f.writelines(modified_lines)

        df1 = pd.read_csv('./tempfiles/temp_' + Path(file).stem + '.txt', header=None, delim_whitespace=True)
        df1 = df1[df1[1].isin(['C17'])]

        colnumber = 'y' + str(i)
        df[colnumber] = df1[3]

        i += 1

    i = 0

    for file in grofiles:
        file = grodir + file
        with open(file, 'r') as f:
            lines = f.readlines()

        lines = lines[2:-2]
        modified_lines = [line[:15] + line[20:] if line else '' for line in lines]

        with open('./tempfiles/temp_' + Path(file).stem + '.txt', 'w') as f:
            f.writelines(modified_lines)

        df1 = pd.read_csv('./tempfiles/temp_' + Path(file).stem + '.txt', header=None, delim_whitespace=True)
        df1 = df1[df1[1].isin(['C17'])]

        colnumber = 'z' + str(i)
        df[colnumber] = df1[4]

        i += 1

    a = 1

    print(df)

    df = df[df.index.isin([661])]

    ax = plt.figure().add_subplot(projection='3d')

    colors = ['r', 'g', 'b', 'y', 'pink', 'orange', 'purple']

    while a < i:
        dxnumber = 'dx' + str(a)
        dynumber = 'dy' + str(a)
        dznumber = 'dz' + str(a)

        xnumber1 = 'x' + str(a-1)
        ynumber1 = 'y' + str(a-1)
        znumber1 = 'z' + str(a-1)

        xnumber2 = 'x' + str(a)
        ynumber2 = 'y' + str(a)
        znumber2 = 'z' + str(a)

        mag = 'magnitude' + str(a)

        df[dxnumber] = df[xnumber2] - df[xnumber1]
        df[dynumber] = df[ynumber2] - df[ynumber1]
        df[dznumber] = df[znumber2] - df[znumber1]

        df.loc[df[dxnumber] > 7, xnumber2] -= 10
        df.loc[df[dxnumber] < -7, xnumber2] += 10

        df.loc[df[dynumber] > 7, ynumber2] -= 10
        df.loc[df[dynumber] < -7, ynumber2] += 10

        df.loc[df[dznumber] > 7, znumber2] -= 10
        df.loc[df[dznumber] < -7, znumber2] += 10

        df[dxnumber] = df[xnumber2] - df[xnumber1]
        df[dynumber] = df[ynumber2] - df[ynumber1]
        df[dznumber] = df[znumber2] - df[znumber1]

        df[mag] = np.linalg.norm(df[[dxnumber, dynumber, dznumber]] * 10, axis=1)
        averagemag = df[mag].mean()
        maglist.append(averagemag)

        ax.quiver(df[xnumber1], df[ynumber1], df[znumber1], df[dxnumber], df[dynumber],
                  df[dznumber], arrow_length_ratio=0.06, linewidth=0.8, color=colors[a-1])
        ax.plot([], [], [], color=colors[a-1], label="Run " + str(a))

        a += 1

    ax.set_xlim([2.5, 0.5])
    ax.set_ylim([1.5, 2.5])
    ax.set_zlim([7, 8])

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    ax.legend()

    filename = str('./plots/movements7TIPS.png')
    plt.tick_params(labelbottom=False, bottom=False, labelleft=False, left=False)
    plt.show()
    plt.savefig(filename, dpi=300, bbox_inches='tight')


    print(df.to_string(index=False))

    allavg = sum(maglist) / len(maglist)

    for file in grofiles:
        os.remove('./tempfiles/temp_' + Path(file).stem + '.txt')

    with open(filename, 'w') as f:
        f.writelines(df.to_string(index=False))

    return df, maglist, allavg

df, maglist, allavg = calculate_movement()




#movements, averagelist, average = calculate_movement()
