import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path


grodir = r'./grofiles/'
grofiles = []

for file in os.listdir(grodir):
    if os.path.isfile(os.path.join(grodir, file)):
        grofiles.append(file)

grofiles = sorted(grofiles)

filedescription = ['Original']

for i in range(len(grofiles)):
    if i == 0:
        pass
    else:
        filedescription.append('Run ' + str(i))

print(filedescription)

count = 0

dfs = [pd.read_csv('./resultfiles/results_edited_' + Path(file).stem + '.txt', skiprows=2, delim_whitespace=True)
       for file in grofiles]

data = pd.DataFrame()

for dataframe in dfs:
    if count == 0:
        dfs[count]['filenumber'] = 'Original'
        data = pd.concat([data, dfs[count]], ignore_index=True)

    else:
        dfs[count]['filenumber'] = str(count)
        data = pd.concat([data, dfs[count]], ignore_index=True)

    count += 1


def plot_catplot(variable=None):
    if variable == 'length':
        chart = sns.catplot(data=data, x='filenumber', y=variable, hue='filenumber')
        for ax in chart.axes.flatten():
            #ax.set_title('Distribution of lengths of backbone in each run', weight='bold', size=15)
            ax.set_xlabel('Run')
            ax.set_ylabel('Length of Backbone (A)')
    elif variable == 'xangle' or 'yangle' or 'zangle':
        chart = sns.catplot(data=data, x='filenumber', y=variable, hue='filenumber')
        for ax in chart.axes.flatten():
            #ax.set_title('Angle of backbone w.r.t. ' + variable[0] + '-axis in each run', weight='bold', size=15)
            ax.set_xlabel('Run')
            ax.set_ylabel('Angle (deg)')

    else:
        print("error")
        exit()

    filename = str('./plots/catplot_' + variable + '.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

    print('Saved ' + filename)


def plot_displot(n=10, variable=None):
    if variable == 'length':
        chart = sns.displot(data=data, x='filenumber', y='length', hue='filenumber', bins=n)

        for ax in chart.axes.flatten():
            #ax.set_title('Distribution of lengths of backbone in each run', weight='bold', size=15)
            ax.set_xlabel('Run')
            ax.set_ylabel('Length of Backbone (A)')
        chart.legend.set_title('Run')

    elif variable == 'xangle' or 'yangle' or 'zangle':
        chart = sns.displot(data=data, x='filenumber', y=variable, hue='filenumber', bins=n)

        for ax in chart.axes.flatten():
            #ax.set_title('Angle of backbone w.r.t. ' + variable[0] + '-axis in each run', weight='bold', size=15)
            ax.set_xlabel('Run')
            ax.set_ylabel('Angle (deg)')
        chart.legend.set_title('Run')

    else:
        print("error")
        exit()

    filename = str('./plots/displot_' + str(n) + '_' + variable + '.png')

    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print('Saved ' + filename)


def plot_boxplot(variable=None):
    if variable == 'length':
        chart = sns.boxplot(data=data, x='filenumber', y='length', hue='filenumber', width=0.8)
        #chart.set_title('Distribution of lengths of backbone in each run', weight='bold', size=15)
        chart.set_xlabel('Run')
        chart.set_ylabel('Length of Backbone (A)')

    elif variable == 'xangle' or 'yangle' or 'zangle':
        chart = sns.boxplot(data=data, x='filenumber', y=variable, hue='filenumber', width=0.8)
        #chart.set_title('Angle of backbone w.r.t. ' + variable[0] + '-axis in each run', weight='bold', size=15)
        chart.set_xlabel('Run')
        chart.set_ylabel('Angle (deg)')
        chart.set_yticks(np.arange(0, 181, 60))

    else:
        print("error")
        exit()

    filename = str('./plots/box_' + variable + '.png')

    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print('Saved ' + filename)


def plot_displot2(size, run, variable=None):
    discolors = ['y', 'deeppink', 'green', 'blue', 'orange', 'grey', 'purple']

    if variable == 'length':
        graphtitle = 'Distribution of lengths of pentacene backbone'
        xlabel = 'Length (A)'
        bins = 'auto'

    elif variable == 'xangle' or 'yangle' or 'zangle':
        graphtitle = 'Distribution of angles of backbone w.r.t. ' + variable[0] + '-axis'
        xlabel = 'Angle (deg)'
        xlimit = int(181)
        ylimit = int(63)
        bins = np.arange(0, xlimit, size) - (size / 2)

    else:
        print('angle or length?')
        exit()

    if run == -1:
        chart = sns.displot(data=data, x=variable, hue='filenumber', multiple='layer', legend=True, bins=bins)
        for ax in chart.axes.flatten():
            #ax.set_title(graphtitle, weight='bold', size=15)
            ax.set_xlabel(xlabel, weight="bold")
            ax.set_ylabel("Count", weight="bold")
            ax.tick_params(axis='x', which='major', labelsize=5, labelrotation=45)
        chart.legend.set_title('Run')

        if variable == 'length':
            plt.tick_params(axis='x', which='major', labelsize=10)
            filename = str('./plots/dis_' + variable + '_all.png')

        elif variable == 'xangle' or 'yangle' or 'zangle':
            plt.xticks(range(size, xlimit, size))
            plt.xlim([-1, xlimit])
            filename = str('./plots/dis_' + variable + '_all_' + str(size) + '.png')

        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print('Saved ' + filename)

    else:
        if run == 0:
            runquery = str("Original")
        else:
            runquery = str(run)

        data2 = data[data['filenumber'].isin([runquery])]

        #plt.figure(figsize=(16, 4), dpi=100)

        chart = sns.displot(data=data2, x=variable, color=discolors[run], legend=True, bins=bins)

        for ax in chart.axes.flatten():
            #ax.set_title(graphtitle, weight='bold', size=15)
            ax.set_xlabel(xlabel, fontsize=9, weight="bold")
            ax.set_ylabel("Count", weight="bold")
            ax.tick_params(axis='x', which='major', labelsize='x-small', labelrotation=45)

        if variable == 'length':
            plt.tick_params(axis='x', which='major', labelsize='small')
            filename = str('./plots/dis_' + variable + '_' + str(runquery) + '.png')

        elif variable == 'xangle' or 'yangle' or 'zangle':
            plt.xticks(range(size, xlimit, size*2))
            plt.xlim([0, xlimit])
            plt.ylim([0, ylimit])
            filename = str('./plots/dis_' + variable + '_' + str(runquery) + '_' + str(size) + '.png')

        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print('Saved ' + filename)


def plot_kdeplot(run=0, variable=None):
    i = 1
    kdecolors = ['y', 'deeppink', 'green', 'blue', 'orange', 'grey', 'purple']

    if variable == 'length':
        graphtitle = 'Distribution of lengths of backbone'
        xlabel = 'Length (A)'

    elif variable == 'xangle' or 'yangle' or 'zangle':
        graphtitle = 'Distribution of angles of backbone w.r.t. ' + variable[0] + '-axis'
        xlabel = 'Angle (deg)'

    else:
        print('angle or length?')
        exit()

    if run == -1:
        plt.subplot(2, 2, 1)
        sns.kdeplot(data.loc[data['filenumber'] == str('Original'), variable], color='y', alpha=.4)
        plt.ylim([0, 0.01])

        plt.tick_params(labelbottom=False, bottom=False)
        plt.xlabel(None)
        plt.ylabel("Density", fontsize='large', weight="bold")

        while i < count:
            plt.subplot(2, 2, i+1)
            sns.kdeplot(data.loc[data['filenumber'] == str(i), variable], color=kdecolors[i], alpha=.4)
            plt.ylim([0, 0.01])

            if (i % 2) == 0:
                plt.ylabel("Density", fontsize='large', weight="bold")
                plt.tick_params(labelleft=True, left=True, labelbottom=False, bottom=False)
            else:
                plt.ylabel(None)
                plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

            if count - i == 1:
                plt.xlabel("Angle (deg)", fontsize='large', weight="bold")

            elif count - i == 2:
                plt.xlabel("Angle (deg)", fontsize='large', weight="bold")
            else:
                plt.xlabel(None)

            i += 1

        filename = str('./plots/kde_' + variable + '_all.png')

    else:
        if run == 0:
            filename = str('./plots/kde_' + variable + '_original.png')

            runnumber = 'original run'
            runquery = 'Original'
        else:
            filename = str('./plots/kde_' + variable + '_' + str(run) + '.png')

            runnumber = 'run #' + str(run)
            runquery = str(run)

        plt.figure(figsize=(6, 4), dpi=80)
        sns.kdeplot(data.loc[data['filenumber'] == runquery, variable], color=kdecolors[run],
                    label='Run ' + str(run), alpha=.4)
        plt.ylim([0, 0.01])
        #plt.title(graphtitle + ' in ' + str(runnumber), fontsize=23, weight='bold')

        plt.tick_params(labelbottom=False, bottom=False)
        plt.xlabel(xlabel, fontsize='large', weight="bold")
        plt.ylabel("Density", fontsize='large', weight="bold")


    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print('Saved ' + filename)


def plot_kdeplotstacked(variable=None):
    kdecolors = ['y', 'deeppink', 'green', 'blue', 'orange', 'grey', 'purple']

    if variable == 'length':
        filename = str('./plots/kdeall_' + variable + '.png')
        graphtitle = 'Distribution of lengths of backbone'
        xlabel = 'Length (A)'

    elif variable == 'allangle':
        filename = str('./plots/kdeall_' + variable + '.png')
        graphtitle = 'Distribution of angles of backbone'
        variable = ['xangle', 'yangle', 'zangle']
        xlabel = 'Angle (deg)'

    elif variable == 'xangle' or 'yangle' or 'zangle':
        filename = str('./plots/kdeall_' + variable + '.png')
        graphtitle = 'Distribution of angles of backbone w.r.t. ' + variable[0] + '-axis'
        xlabel = 'Angle (deg)'

    else:
        print('angle or length?')
        exit()

    plt.figure(figsize=(6, 4), dpi=80)

    if isinstance(variable, list):
        for var in variable:
            sns.kdeplot(data.loc[data['filenumber'] == "Original", var], color=kdecolors[0],
                        label='Original', alpha=.4)
    else:
        sns.kdeplot(data.loc[data['filenumber'] == "Original", variable], color=kdecolors[0],
                    label='Original', alpha=.4)

    if isinstance(variable, list):
        for var in variable:
            for i in range(count):
                sns.kdeplot(data.loc[data['filenumber'] == str(i), var], color=kdecolors[i],
                            label='Run ' + str(i), alpha=(i+3)/10)


    else:
        for i in range(count):
            sns.kdeplot(data.loc[data['filenumber'] == str(i), variable], color=kdecolors[i],
                        label='Run ' + str(i), alpha=.4)


    plt.xlabel(xlabel, weight='bold', fontsize='large')
    plt.ylabel("Density", weight='bold', fontsize='large')
    #plt.title(graphtitle, fontsize=23, weight='bold')
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()


def plot_pairplot():
    sns.pairplot(data, kind='scatter', hue='filenumber', plot_kws=dict(s=4))


def calcmovement():
    df = pd.DataFrame()
    maglist = []
    i = 0

    for grofile in grofiles:
        grofile = grodir + grofile
        with open(grofile, 'r') as f:
            lines = f.readlines()

        lines = lines[2:-2]
        modified_lines = [line[:15] + line[20:] if line else '' for line in lines]

        with open('./tempfiles/temp_' + Path(grofile).stem + '.txt', 'w') as f:
            f.writelines(modified_lines)

        df1 = pd.read_csv('./tempfiles/temp_' + Path(grofile).stem + '.txt', header=None, delim_whitespace=True)
        df1 = df1[df1[1].isin(['C17'])]

        colnumber = 'x' + str(i)
        df[colnumber] = df1[2]

        i += 1

    i = 0

    for grofile in grofiles:
        grofile = grodir + grofile
        with open(grofile, 'r') as f:
            lines = f.readlines()

        lines = lines[2:-2]
        modified_lines = [line[:15] + line[20:] if line else '' for line in lines]

        with open('./tempfiles/temp_' + Path(grofile).stem + '.txt', 'w') as f:
            f.writelines(modified_lines)

        df1 = pd.read_csv('./tempfiles/temp_' + Path(grofile).stem + '.txt', header=None, delim_whitespace=True)
        df1 = df1[df1[1].isin(['C17'])]

        colnumber = 'y' + str(i)
        df[colnumber] = df1[3]

        i += 1

    i = 0

    for grofile in grofiles:
        grofile = grodir + grofile
        with open(grofile, 'r') as f:
            lines = f.readlines()

        lines = lines[2:-2]
        modified_lines = [line[:15] + line[20:] if line else '' for line in lines]

        with open('./tempfiles/temp_' + Path(grofile).stem + '.txt', 'w') as f:
            f.writelines(modified_lines)

        df1 = pd.read_csv('./tempfiles/temp_' + Path(grofile).stem + '.txt', header=None, delim_whitespace=True)
        df1 = df1[df1[1].isin(['C17'])]

        colnumber = 'z' + str(i)
        df[colnumber] = df1[4]

        i += 1

    a = 1

    ax = plt.figure().add_subplot(projection='3d')

    colors = ['r', 'g', 'b', 'y', 'pink', 'orange', 'purple']

    while a < i:
        dxnumber = 'dx' + str(a)
        dynumber = 'dy' + str(a)
        dznumber = 'dz' + str(a)

        xnumber1 = 'x' + str(a - 1)
        ynumber1 = 'y' + str(a - 1)
        znumber1 = 'z' + str(a - 1)

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
                  df[dznumber], arrow_length_ratio=0.1, linewidth=0.2, color=colors[a - 1])
        ax.plot([], [], [], color=colors[a - 1], label="Run " + str(a))

        a += 1

    ax.set_xlim([10, 0])
    ax.set_ylim([0, 10])
    ax.set_zlim([0, 10])

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    ax.legend()

    filename = str('./plots/movements.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')

    # allavg = sum(maglist) / len(maglist)

    for grofile in grofiles:
        os.remove('./tempfiles/temp_' + Path(grofile).stem + '.txt')

    name = './resultfiles/movement_' + Path(grofiles[0]).stem + '_to_' + Path(grofiles[-1]).stem + '.txt'

    with open(name, 'w') as f:
        f.writelines(df.to_string(index=False))


varia = 'yangle'

sdxangle = [41.02344300824685, 39.863991384286294, 38.09083486157127, 39.81404003189252]
sdyangle = [38.38182681651835, 38.694803280148236, 38.34312747181512, 37.38038780329123]
sdzangle = [38.181867961279515, 38.5664955911714, 41.12406003253968, 40.635729583670596]
lengths = [12.015691827805846, 12.201897465670116, 12.202480184959704, 12.200735262631623]

x = ["Original", str(1), str(2), str(3)]

# plot lines
# plt.plot(x, sdxangle, label="x-angle")
# plt.plot(x, sdyangle, label="y-angle")
# plt.plot(x, sdzangle, label="z-angle")
# plt.plot(x, lengths, label="lengths")
# plt.legend()


def allangles(variables, binsizes, runs):
    for varia in variables:
        for binsize in binsizes:
            for run in runs:
                plot_displot2(binsize, run, varia)


def kdeall():
    for varia in varialist:
        plot_kdeplot(-1, varia)

        plot_kdeplot(0, varia)

        plot_kdeplot(1, varia)

        plot_kdeplot(2, varia)

        plot_kdeplot(3, varia)






varialist = ['yangle']
binlist = [5]
runlist = [3]

#plot_kdeplot(-1, 'length')



plot_kdeplotstacked('length')
allangles(varialist, binlist, runlist)

# plot_displot2(1, -1, 'length')
# plot_displot2(1, 0, 'length')
# plot_displot2(1, 1, 'length')
# plot_displot2(1, 2, 'length')
# plot_displot2(1, 3, 'length')
