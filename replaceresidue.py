while True:
    newresidue = input("Enter your residue name: ")

    if len(newresidue) == 4 and newresidue.isalpha():
        break

    else:
        print("Invalid input. Residue name must be 4-letters long")

file_itp = newresidue + ".itp"
file_pdb = newresidue + ".pdb"

try:
    print("-----------------\nReading " + file_itp + "...")

    with open(file_itp, 'r') as file:
        filedata = file.read()

    with open(file_itp, 'r') as file:
        lines = file.readlines()
        originalresidue = lines[60][0:4]

    print("Replacing " + originalresidue + " with " + newresidue + "...")

    filedata = filedata.replace(originalresidue, newresidue)

    print("Writing to ITP file...")

    with open(file_itp, 'w') as file:
        file.writelines(filedata)

    print("Successfully modified " + file_itp + ".")

    print("-----------------\nReading " + file_pdb + "...")

    with open(file_pdb, 'r') as file:
        filedata = file.read()

    print("Replacing " + originalresidue + " with " + newresidue + "...")

    filedata = filedata.replace(originalresidue, newresidue)

    print("Writing to PDB file...")

    with open(file_pdb, 'w') as file:
        file.writelines(filedata)

    print("Successfully modified " + file_pdb + ".")

except ValueError:
    print("Error. Check your files.")

except TypeError:
    print("Error. Check your files.")

except FileNotFoundError:
    print("File not found. Please ensure your file has been renamed to match your residue name.")

except Exception as e:
    print("Error. Check your files")
