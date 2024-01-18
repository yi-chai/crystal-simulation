import pandas as pd
import os
import json
import matplotlib.pyplot as plt
from pathlib import Path

grodir = r'./resultfiles/'
grofiles = []

for file in os.listdir(grodir):
    if os.path.isfile(os.path.join(grodir, file)):
        if 'results_edited_' in file:
            if 'summary' not in file:
                grofiles.append(file)


grofiles = sorted(grofiles)


def extract_dict_from_file(filename):
    with open(filename, 'r') as file:
        first_line = file.readline().strip()
        return json.loads(first_line)


dicts = [extract_dict_from_file(grodir + grofile) for grofile in grofiles]

table = pd.DataFrame(dicts)

sdxangle = table["Standard Deviation of X-Angle"]
sdyangle = table["Standard Deviation of Y-Angle"]
sdzangle = table["Standard Deviation of Z-Angle"]
avglength = table["Average Length of Backbone (A)"]

x = table["source"]
x = x.apply(lambda text: text.replace('run0', 'Original'))
x = x.apply(lambda text: text.replace('run', ''))

plt.plot(x, sdxangle)
plt.title("Standard Deviation of X-Angle After Each Run", weight='bold', size=15)
plt.xlabel('Run', weight='bold')
plt.ylabel('Angle (deg)', weight='bold')
plotfilename = str('./plots/change_xangle.png')
plt.savefig(plotfilename, dpi=300, bbox_inches='tight')
plt.close()
print('Saved ' + plotfilename)

plt.plot(x, sdyangle)
plt.title("Standard Deviation of Y-Angle After Each Run", weight='bold', size=15)
plt.xlabel('Run', weight='bold')
plt.ylabel('Angle (deg)', weight='bold')
plotfilename = str('./plots/change_yangle.png')
plt.savefig(plotfilename, dpi=300, bbox_inches='tight')
plt.close()
print('Saved ' + plotfilename)

plt.plot(x, sdzangle)
plt.title("Standard Deviation of Z-Angle After Each Run", weight='bold', size=15)
plt.xlabel('Run', weight='bold')
plt.ylabel('Angle (deg)', weight='bold')
plotfilename = str('./plots/change_zangle.png')
plt.savefig(plotfilename, dpi=300, bbox_inches='tight')
plt.close()
print('Saved ' + plotfilename)

plt.plot(x, avglength)
plt.title("Average Length of Backbone After Each Run", weight='bold', size=15)
plt.xlabel('Run', weight='bold')
plt.ylabel('Length (A)', weight='bold')
plotfilename = str('./plots/change_lengths.png')
plt.savefig(plotfilename, dpi=300, bbox_inches='tight')
plt.close()
print('Saved ' + plotfilename)

plt.plot(x, sdxangle, label="x-angle")
plt.plot(x, sdyangle, label="y-angle")
plt.plot(x, sdzangle, label="z-angle")
plt.title("Standard Deviation of Angles After Each Run", weight='bold', size=15)
plt.xlabel('Run', weight='bold')
plt.ylabel('Angle (deg)', weight='bold')
plt.legend()
plotfilename = str('./plots/change_allangle.png')
plt.savefig(plotfilename, dpi=300, bbox_inches='tight')
plt.close()
print('Saved ' + plotfilename)

name = './resultfiles/summary_' + Path(grofiles[0]).stem + '_to_' + Path(grofiles[-1]).stem + '.txt'

with open(name, 'w') as f:
    f.writelines(table.to_string())
