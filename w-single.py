import subprocess
import time
import numpy as np
import math
import os
import re
import sys
import io

myfilelist = ['TIPS']
mybasislist = ['sto-3g', '6-31g', 'def2-svp']

w = 0.1
eps = 3.6


def make_ts_file_op(mybasis, myfile, function, w=0, epsilon=0, dftd='no', run='minimize', charge=0, spinmult=1,
                    dispersion='no', resp=False, restricted='yes', excited='no', state=0, highmethod1='no',
                    highmethod2='no'):
    basis = 'basis    ' + mybasis
    myco = myfile + '.xyz'

    if epsilon != 0:
        epsilon = 'epsilon' + '  ' + str(epsilon)

        if run == 'minimize' and charge == -1:
            thepath = myfile + 'add_E.xyz'

            if os.path.isfile(thepath):
                myco = myfile + 'add_E.xyz'

    coordinates = 'coordinates    ' + myco
    filename = myfile + str(run)

    if restricted == 'yes' and excited == 'yes':
        filename = myfile + str(run) + 'singlet'

    if restricted == 'no' and excited == 'yes':
        filename = myfile + str(run) + 'triplet'

    openfile = filename + '.ts'
    charge1 = 'charge          ' + str(charge)
    spinmult = 'spinmult      ' + str(spinmult)
    ts_file = open(openfile, 'w')
    ts_file.write(basis)
    ts_file.write('\n')
    ts_file.write(coordinates)
    ts_file.write('\n')
    ts_file.write(charge1)
    ts_file.write('\n')
    ts_file.write(spinmult)
    ts_file.write('\n')

    if w != 0:
        ww = 'rc_w' + '  ' + str(w)
        ts_file.write(ww)
        ts_file.write('\n')

    if restricted == 'yes':
        my_function = 'method    ' + str(function)
        ts_file.write(my_function)

    if restricted == 'no':
        my_function = 'method    ' + 'u' + str(function)
        ts_file.write(my_function)

    ts_file.write('\n')

    if dftd != 'no':
        dftd = 'dftd ' + str(dftd)
        ts_file.write(dftd)
        ts_file.write('\n')

    if epsilon != 0:
        epsilon = str(epsilon)
        ts_file.write(epsilon)
        ts_file.write('\n')
        ts_file.write('pcm cosmo')
        ts_file.write('\n')

    if dispersion != 'no':
        ts_file.write('dispersion yes')
        ts_file.write('\n')

    if highmethod1 == 'yes':
        ts_file.write('min_method bfgs')
        ts_file.write('\n')
        ts_file.write('min_init_hess diagonal')
        ts_file.write('\n')

    if highmethod2 == 'yes':
        ts_file.write('dftgrid 3')
        ts_file.write('\n')
        ts_file.write('convthre 3e-6')
        ts_file.write('\n')     
        ts_file.write('min_tolerance 4.5E-5')
        ts_file.write('\n')
        ts_file.write('min_tolerance_e 1E-7')
        ts_file.write('\n')

    if run == 'minimize':
        ts_file.write('min_coordinates cartesian')
        ts_file.write('\n')

    ts_file.write('maxit 500')
    ts_file.write('\n')

    if excited == 'yes':
        ts_file.write('cis yes')
        ts_file.write('\n')
        ts_file.write('cisnumstates ' + str(state))
        ts_file.write('\n')
        ts_file.write('cismaxiter 200')
        ts_file.write('\n')

    if run == 'minimize':
        ts_file.write('new_minimizer yes')
        ts_file.write('\n')  
        ts_file.write('run minimize')
        ts_file.write('\n')

    if run == 'energy':
        ts_file.write('run energy')
        ts_file.write('\n')

    if resp is True:
        ts_file.write('resp	yes')
        ts_file.write('\n')

    ts_file.write('end')
    ts_file.close()

    return run, filename


def make_ts_file(mybasis, myfile, myw, run='minimize', charge=0, spinmult=1):
    basis = 'basis    ' + mybasis
    rc_w = 'rc_w ' + str(myw)
    myco = myfile + '.xyz'

    if run == 'minimize' and charge == -1:
        thepath = myfile + 'add_E.xyz'

        if os.path.isfile(thepath):
            myco = myfile + 'add_E.xyz'

    coordinates = 'coordinates    ' + myco
    openfile = myfile + '.ts'
    charge1 = 'charge          ' + str(charge)
    spinmult = 'spinmult      ' + str(spinmult)
    ts_file = open(openfile, 'w')
    ts_file.write(basis)
    ts_file.write('\n')
    ts_file.write(coordinates)
    ts_file.write('\n')
    ts_file.write(charge1)
    ts_file.write('\n')
    ts_file.write(spinmult)
    ts_file.write('\n')

    if charge == 0:
        ts_file.write('method          wpbeh')

    else:
        ts_file.write('method          uwpbeh')

    ts_file.write('\n')
    ts_file.write(rc_w)
    ts_file.write('\n')
    ts_file.write('pcm cosmo')
    ts_file.write('\n')
    ts_file.write('epsilon 2.38')
    ts_file.write('\n')
    ts_file.write('dispersion       yes')
    ts_file.write('\n')
    ts_file.write('pcm_scale 1')
    ts_file.write('\n')
    ts_file.write('min_coordinates cartesian')
    ts_file.write('\n')
    ts_file.write('maxit 500')
    ts_file.write('\n')
    ts_file.write('solvent_radius 3.48')
    ts_file.write('\n')

    if run == 'minimize':
        ts_file.write('run minimize')

    if run == 'energy':
        ts_file.write('run energy')

    ts_file.write('\n')
    ts_file.write('end')
    ts_file.write('\n')
    ts_file.close()


def make_sh_file(file):
    sh_file = str(file) + '.sh'
    f = open(sh_file, 'w')
    sh = open('./terachem2.sh')

    for i, line in enumerate(sh):
        if i == 9:
            openfile = myfile + '.ts'
            f.write('terachem ' + os.getcwd() + '/' + file + '.ts')
        elif i != 9:
            f.write(line)
    f.close()
    filename = './' + str(file) + '.log'

    with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
        process = subprocess.Popen('source ' + sh_file + '; env -0', shell=True, executable='/bin/bash', stdout=writer)

        while process.poll() is None:
            sys.stdout.write(str(reader.read()))
            time.sleep(5)

        sys.stdout.write(str(reader.read()))

def extract_HOMO_LUMO(myfile):
    mymolden = './scr/' + myfile + '.molden'
    read_file = open(mymolden)
    n = 0

    for i, line in enumerate(read_file):
        if line.__contains__('Occup= 2.0'):
            i2 = i

        if line.__contains__('Occup= 0.0') and n == 0:
            i0 = i
            n = 1

    read_file2 = open(mymolden)

    for i, line in enumerate(read_file2):
        if i == i2 - 2:
            HOMO = line.split()[1]

        if i == i0 - 2:
            LUMO = line.split()[1]

    return HOMO, LUMO


def extract_Energy(myfile):
    myfile1 = './scr' + '/' + 'results.dat'
    myfile1 = open(myfile1, 'r')
    for i, line in enumerate(myfile1):
        if i == 1:
            line1 = line.split()
            line1 = (line1[0])

    return float(line1)


def replace_xyz(myfile, new_file=False):
    myco = myfile + '.xyz'
    fline = open('./' + myco).readline().rstrip()
    fline = int(fline)
    b = 0

    while b == 0:
        b = os.path.getsize('./scr/optim.xyz')

    time.sleep(10)    
    read_file3 = open('./scr/optim.xyz')

    if new_file is True:
        mynewco = myfile + 'add_E.xyz'
        write_newxyz = open('./' + mynewco, 'w')

        for line in (read_file3.readlines()[-fline-2:]):
            line1 = line.rstrip('/n')
            write_newxyz.write(line1)

    elif new_file is False:
        write_newxyz = open('./' + myco, 'w')

        for line in (read_file3.readlines()[-fline-2:]):
            line1 = line.rstrip('/n')
            write_newxyz.write(line1)

    write_newxyz.close()


def w_tuning(mybasis, myw, myfile):
    make_ts_file(mybasis, myfile, myw)
    make_sh_file(myfile)
    time.sleep(5)
    replace_xyz(myfile)
    time.sleep(5)
    Energy0 = extract_Energy(myfile)
    HOMO, LUMO = extract_HOMO_LUMO(myfile)
    make_ts_file(mybasis, myfile, myw, run='energy', charge=1, spinmult=2)  # remove one electron
    make_sh_file(myfile)
    time.sleep(5)
    Energy_0p1 = extract_Energy(myfile)
    make_ts_file(mybasis, myfile, myw, run='minimize', charge=-1, spinmult=2)   # add one electron
    make_sh_file(myfile)
    time.sleep(5)
    replace_xyz(myfile, new_file=True)
    time.sleep(5)
    Energy_n1 = extract_Energy(myfile)
    myfile2 = myfile + 'add_E'    # new file
    make_ts_file(mybasis, myfile2, myw, run='energy', charge=0, spinmult=1)
    make_sh_file(myfile2)
    time.sleep(5)
    Energy_n1p0 = extract_Energy(myfile2)
    errorH = (float(Energy0) - float(Energy_0p1)) - float(HOMO)
    errorL = (float(Energy_n1) - float(Energy_n1p0)) - float(LUMO)
    error = np.sqrt(errorH**2 + errorL**2)

    return error


def gss(J, a, b, mybasis, myfile, tol=0.01):
    listofw = open('w_file.txt', 'a+')
    gr = (math.sqrt(5) + 1) / 2
    c = b - (b - a) / gr
    d = a + (b - a) / gr

    while abs(b - a) > tol:
        J1 = w_tuning(mybasis, c, myfile)
        time.sleep(10)
        J2 = w_tuning(mybasis, d, myfile)

        if J1 < J2:
            b = d

        else:
            a = c

        txt = 'w1= ' + str(c) + 'J1= ' + str(J1) + 'w2= ' + str(d) + ' J2= ' + str(J2)
        listofw.write(str(myfile) + ' ' + txt)
        listofw.write('\n')
        print(str(myfile) + ' ' + txt + '\n')
        c = b - (b - a) / gr
        d = a + (b - a) / gr

    return (b + a) / 2


for myfile in myfilelist:
    for basis in mybasislist:
        jobtype, filename = make_ts_file_op(basis, myfile, 'wpbeh', w=w, epsilon=eps, dispersion='no',
                                            highmethod1='no', highmethod2='no')
        make_sh_file(filename)
        time.sleep(2)
        replace_xyz(myfile, new_file=False)

time.sleep(30)
mybasis = 'def2-svp'

for myfile in myfilelist:
    w_final = gss(w_tuning, 0.03, 0.10, mybasis, myfile)
    make_ts_file(mybasis, myfile, w_final)
    make_sh_file(myfile)
    time.sleep(10)
    myco = myfile + '.xyz'
    mynewco = myfile + str(w_final) + '.xyz'
    os.rename(myco, mynewco)
    time.sleep(30)
    jobtype, filename = make_ts_file_op(mybasis, myfile + str(w_final), 'wpbeh', w=w_final, epsilon=eps,
                                        run='energy',
                                        resp=True, restricted='no', excited='no')
    make_sh_file(filename)
    time.sleep(10)

try:
    pass

except ValueError:
    print("Error. Check your files.")

except TypeError:
    print("Error. Check your files.")

except FileNotFoundError:
    print("File not found.")

except Exception as e:
    print("Error. Check your flies")
