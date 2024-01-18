import pandas as pd

filename = input("Enter .gro file: ")
filenamedupe = "old_" + str(filename)

while True:
    boxsize = input("Box size (nm): ")

    try:
        float_value = float(boxsize)
        break

    except ValueError:
        print("Please enter a valid number. Try again.")


def adjustcolumn(column, spaces):
    data[column] = data[column].astype(str)
    data[column] = data[column].apply(lambda x: f'{float(x):.5f}')
    data[column] = data[column].str.rjust(spaces)


try:
    print("Reading file...")

    with open(filename, 'r') as file:
        filedata = file.read()

    with open(filename, 'r') as file:
        resdata = file.readlines()

    with open(filenamedupe, 'w') as file:
        file.writelines(filedata)

    residuename = resdata[2][5:9]

    print("Residue: " + residuename)

    print("Replacing 0" + residuename + " with 1" + residuename + "...")

    filedata = filedata.replace('0' + residuename, '1' + residuename)

    print("Successfully replaced.")

    filedata = filedata[:-31]

    print("Setting box size to " + boxsize + " x " + boxsize + " x " + boxsize + "...")

    data = pd.DataFrame({1: [boxsize], 2: [boxsize], 3: [boxsize]})

    adjustcolumn(1, 10)
    adjustcolumn(2, 9)
    adjustcolumn(3, 9)

    data = data.to_string(header=False, index=False)

    print("Successfully set box size.")

    contents = "".join([filedata, str(data), '\n'])

    print("Writing data...")

    with open(filename, 'w') as file:
        file.writelines(contents)

    print("Process complete.")

except ValueError:
    print("Error. Check your files/input.")

except TypeError:
    print("Error. Check your files/input.")

except FileNotFoundError:
    print("File not found.")

except Exception as e:
    print("Error. Check your files/input")
