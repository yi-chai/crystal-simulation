import time
from shutil import copyfile
import os

file = 'mTIP'
residue = 'TIPS'
jobname = 'TIPS'


def no_molecule(file, res):
    filepath = os.getcwd()+'/'+str(file)+'.gro'
    a_file = open(filepath, 'r')
    lines = a_file.readlines()
    first = lines[2].split()[0].split(res)[0]
    last = lines[-2:-1][0].split()[0].split(res)[0]
    number = int(last) - int(first) + 1
    return number


def top(file, no_mol, res):
    filepath = './'+str(file)+'.top'
    copyfile('standard.top', './' + filepath)
    hs = open('./'+filepath, 'a')
    txt = res + '   '+str(no_mol)
    hs.write(txt)
    hs.close()


def make_sh_file(code):
    sh = open('compile.sh', 'w')
    sh.write('module load gromacs/gromacs-2021.2' + '\n')
    sh.write(code)
    sh.close()
    # filename = './gromacs.err'
    # output = subprocess.check_output('source compile.sh' + '; env -0', shell=True, executable='/bin/bash')


def howmanyadded():
    addedm = 0
    hs = open(jobname+'.err', 'r')
    for i, line in enumerate(hs):
        if 'Added' in line:
            addedm = int(line.split()[1])
    return addedm


try:
    no_mol = no_molecule(file, residue)
    top(file, no_mol, residue)

    make_sh_file('gmx_mpi grompp -f minim.mdp -c ' + file + '.gro -r ' + file +
                 '.gro -p ' + file + '.top -o em.tpr -maxwarn 4')
    time.sleep(5)
    make_sh_file('mpirun gmx_mpi mdrun -v -deffnm em -ntomp 1')
    time.sleep(5)
    make_sh_file('gmx_mpi grompp -f nvtanneal.mdp -c ' + file + '.gro -r ' + file +
                 '.gro -p ' + file + '.top -o em.tpr -maxwarn 4')
    time.sleep(5)
    make_sh_file('mpirun gmx_mpi mdrun -v -deffnm em -ntomp 1')
    time.sleep(5)

except ValueError:
    print("Error. Check your files.")

except TypeError:
    print("Error. Check your files.")

except FileNotFoundError:
    print("File not found.")

except Exception as e:
    print("Error. Check your flies")
    
