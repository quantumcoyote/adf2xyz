from subprocess import Popen, STDOUT, PIPE
import subprocess
import sys
import math
import os

def ADF(path):
    global P
    global T
    global multiplicity
    global x
    global y
    global z
    global mass
    global natoms
    global frequencies
    global E
    global Rot_Number
    global count
    global type

    #
    # Initialize Function Variables
    #

    nline=0
    geo=0
    masspos=0
    endgeo=0
    nfreq=0

    with open(path, 'r') as searchfile:
        for line in searchfile:
            if 'Total Bonding Energy:' in line:
                tmp = line.split()
                E = tmp[3]
            if 'Pressure:' in line:
                tmp = line.split()
                P = float(tmp[1])
            if 'Temperature:' in line:
                tmp = line.split()
                T = float(tmp[1])
            if 'reported below were computed using sigma =' in line:
                line = line.replace(',', ' ')
                line = line.replace('=', '= ')
                tmp = line.split()
                Rot_Number=float(tmp[7])
            if 'Atom         X           Y           Z   (Angstrom)' in line:
                geo = int(nline)
            if '>>>> CORORT' in line:
                endgeo = int(nline)
            if '                                (Angstrom)             Nucl     +Core       At.Mass (Angstrom)' in line:
                masspos = int(nline)
            if 'Molecule:                         ' in line:
                multiplicity=1
            if ' List of All Frequencies:' in line:
                nfreq = int(nline)

            nline=nline+1
        natoms=int((int(endgeo) - int(geo) - 1))

        nline = 1
        with open(path, 'r') as searchfile:
            for line in searchfile:
                if int(geo) + 1 < int(nline) < int(endgeo)+1:
                    tmp = line.split()
                    x.append(tmp[1])
                    y.append(tmp[2])
                    z.append(tmp[3])
                if int(masspos+2) < int(nline) < int(masspos)+int(natoms)+3 :
                    tmp = line.split()
                    atomic_mass.append(tmp[7])

                if type == 'molecule':
                    if int(nfreq+9) < int(nline) < int(nfreq+9)+(3*int(natoms))-5 :
                        tmp = line.split()
                        frequencies.append(tmp[0])

                if type == 'atom':
                    frequencies=[]

                if type == 'linear':
                    if int(nfreq+9) < int(nline) < int(nfreq+11) :
                        tmp = line.split()
                        frequencies.append(tmp[0])

                nline = nline + 1

        mass=0.0

        for i in range(0,len(atomic_mass)):
            mass=mass+float(atomic_mass[i])

def Moment_of_Intertia():

    #
    # Function to compute the moment of intertia
    #

    global natoms
    global mass
    global atomic_mass
    global x
    global y
    global z
    global inx
    global iny
    global inz
    global PBED3BJ
    global M06L

    # Initialize the variables that will contain the center of mass
    centerofmassx = 0
    centerofmassy = 0
    centerofmassz = 0

    # Loop to read the geometry and store the x, y and z components
    for i in range(0, int(natoms)):
        # Calculate the center of mass
        centerofmassx = centerofmassx + (float(atomic_mass[i]) * float(x[i]))
        centerofmassy = centerofmassy + (float(atomic_mass[i]) * float(y[i]))
        centerofmassz = centerofmassz + (float(atomic_mass[i]) * float(z[i]))

    centerofmassx = centerofmassx / mass
    centerofmassy = centerofmassy / mass
    centerofmassz = centerofmassz / mass

    # Translate the center of mass to (0,0,0)
    for i in range(0, int(natoms)):
        x[i] = float(x[i]) - centerofmassx
        y[i] = float(y[i]) - centerofmassy
        z[i] = float(z[i]) - centerofmassz

    # Initialize the moment of inertia
    Ixx = 0
    Ixy = 0
    Ixz = 0
    Iyx = 0
    Iyy = 0
    Iyz = 0
    Izx = 0
    Izy = 0
    Izz = 0

    # Compute the values of each component in the moment of inertia matrix
    # The 1.8897 is the Angstroms to Bohr conversion
    for i in range(0, int(natoms)):
        Ixx = Ixx + (float(atomic_mass[i]) * ((float(y[i]) * float(y[i]) * 1.8897 * 1.8897) + (float(z[i]) * float(z[i]) * 1.8897 * 1.8897)))
        Ixy = Ixy + (float(atomic_mass[i]) *  (float(x[i]) * float(y[i]) * 1.8897 * 1.8897))
        Ixz = Ixz + (float(atomic_mass[i]) *  (float(x[i]) * float(z[i]) * 1.8897 * 1.8897))
        Iyx = Iyx + (float(atomic_mass[i]) *  (float(y[i]) * float(x[i]) * 1.889725989 * 1.889725989))
        Iyy = Iyy + (float(atomic_mass[i]) * ((float(x[i]) * float(x[i]) * 1.889725989 * 1.889725989) + (float(z[i]) * float(z[i]) * 1.8897 * 1.8897)))
        Iyz = Iyz + (float(atomic_mass[i]) *  (float(y[i]) * float(z[i]) * 1.889725989 * 1.889725989))
        Izx = Izx + (float(atomic_mass[i]) *  (float(z[i]) * float(x[i]) * 1.889725989 * 1.889725989))
        Izy = Izy + (float(atomic_mass[i]) *  (float(z[i]) * float(y[i]) * 1.889725989 * 1.889725989))
        Izz = Izz + (float(atomic_mass[i]) * ((float(x[i]) * float(x[i]) * 1.889725989 * 1.889725989) + (float(y[i]) * float(y[i]) * 1.8897 * 1.8897)))

    # Put the correct signs into the moment of inertia matrix
    Ixx = Ixx
    Ixy = -Ixy
    Ixz = -Ixz
    Iyx = -Iyx
    Iyy = Iyy
    Iyz = -Iyz
    Izx = -Izx
    Izy = -Izy
    Izz = Izz

    # Open the file with the moment of the inertia matrix
    file = open("momentinertia.dat", "w")

    # Write the inertia matrix into the file
    file.write(str(Ixx) + '\n')
    file.write(str(Ixy) + '\n')
    file.write(str(Ixz) + '\n')
    file.write(str(Iyx) + '\n')
    file.write(str(Iyy) + '\n')
    file.write(str(Iyz) + '\n')
    file.write(str(Izx) + '\n')
    file.write(str(Izy) + '\n')
    file.write(str(Izz) + '\n')

    # Close the file with the moment of the inertia matrix
    file.close()

    # Call the fortran subroutine that diagonalize the moment of inertia matrix
    cmd = 'codes/Diagonalization.exe'
    ret = Popen([cmd], shell=True, stdout=PIPE, stderr=STDOUT)
    (stdout, stderr) = ret.communicate()

    # Call the fortran subroutine that diagonalize the moment of inertia matrix
    cmd = 'mv eigenvalues.dat scratch/.'
    ret = Popen([cmd], shell=True, stdout=PIPE, stderr=STDOUT)
    (stdout, stderr) = ret.communicate()

    # Open the file with the eigenvalues
    file = open('scratch/eigenvalues.dat', 'r+')

    # Read the eigenvalues
    inx = float(file.readline())
    iny = float(file.readline())
    inz = float(file.readline())

    # Close the file with the eigenvalues
    file.close()


    return

def Frequency_Replacement(val):
    global frequencies

    for i in range (0,len(frequencies)):
        if float(frequencies[i]) <= float(val):
            frequencies[i]=float(val)

def Thermochemistry(T,P):

    #
    # Function that calculate the thermochemistry
    #

    global inx
    global iny
    global inz
    global multiplicity
    global frequencies
    global mass
    global H
    global G
    global Rot_Number
    global count
    global type

    # Initialize

    TotUvib = 0.0
    TotSvib = 0.0
    TotZPE = 0.0
    Srot = 0.0
    Urot = 0.0
    Strans = 0.0
    Utrans = 0.0
    Selec = 0.0
    Uelec = 0.0

    # pi constant
    pi = 3.14159265359

    # Boltzman constant kJ/K
    boltzman = 1.380648813 * (10 ** (-23))

    # h in kJ.s
    planck = 6.6260695729 * (10 ** (-34))

    # Combination of constants
    #  - Avogadro's number in molecules/mol
    #  - h in kJ.s
    #  - speed of light in cm/2
    variable1 = 0.011962656594658400

    # Combination of constants (theta)
    #  - h in kJ.s
    #  - speed of light in cm/s
    #  - Boltzman constant kJ/K
    variable2 = 1.438776947066190

    if type != 'atom':

        for a in range(0, int(len(frequencies))):

            # Calculation of the vibrational contribution to the internal energy
            if (frequencies[a] != 0.0):
                Uvib = 0.008314462175 * ((variable2 * (float(frequencies[a]))) * (
                        0.5 + (1 / (math.exp((variable2 * (float(frequencies[a])) / T)) - 1))))
            if (frequencies[a] == 0.0):
                Uvib = 0.0

            # Calculation of the vibrational contribution to the enthropy
            if (frequencies[a] != 0.0):
                Svib = 0.008314462175 * (((variable2 * (float(frequencies[a])) / T) / (
                        math.exp((variable2 * (float(frequencies[a])) / T)) - 1)) - (
                                         math.log(1 - math.exp(-(variable2 * (float(frequencies[a])) / T)))))
            if (frequencies[a] == 0.0):
                Svib = 0.0

            # Calculation of the zero point energy contribution of the given frequency
            ZPE = 0.5 * ((float(frequencies[a])) * variable1)

            # Sums of the total vibrational contribution to the internal energy and the entropy
            TotUvib = TotUvib + Uvib
            TotSvib = TotSvib + Svib

            # Sums of the total zero point energy
            TotZPE = TotZPE + ZPE

    # Mass from a.m.u. to Kg
    mass_kg = mass * 1.66053892 * (10 ** (-27))

    # Initialize the eigenvalues of the moment of inertia matrix
    inx_s=0.0
    iny_s=0.0
    inz_s=0.0

    # Calculation of the rotational partition function and the rotational contribution to the entropy
    # The eigenvalues of the moment of inertia matrix are transformed from a.m.u. and Bohrs to Kg and meters
    inx_s = inx * 1.66053892 * (10 ** (-27)) * 5.29177249 * (10 ** (-11)) * 5.29177249 * (10 ** (-11))
    iny_s = iny * 1.66053892 * (10 ** (-27)) * 5.29177249 * (10 ** (-11)) * 5.29177249 * (10 ** (-11))
    inz_s = inz * 1.66053892 * (10 ** (-27)) * 5.29177249 * (10 ** (-11)) * 5.29177249 * (10 ** (-11))

    if type == 'molecule':
        intertia = math.sqrt(pi * inx_s * iny_s * inz_s)/float(Rot_Number)
        qr = intertia * (((8 * pi * pi * boltzman * T) / (planck * planck)) ** (1.5))
        # Calculation of the rotational contribution to entropy
        Srot = 0.008314462175 * (math.log(qr) + 1.5)

        # Calculation of the rotational contribution to the internal energy
        Urot = 0.0124716932625 * T

    if type == 'linear':
        qr = ((8 * inz_s * pi * pi * boltzman * T) / (planck * planck*float(Rot_Number)))
        # Calculation of the rotational contribution to entropy
        Srot = 0.008314462175 * (math.log(qr) + 1.0)

        # Calculation of the rotational contribution to the internal energy
        Urot = 0.008314462175 * T

    if type == 'atom':
        # Calculation of the rotational contribution to entropy
        Srot = 0.00

        # Calculation of the rotational contribution to the internal energy
        Urot = 0.00

    #
    # Pressure corrections into the translational partition function
    #

    if species == 'OOH':
        P = 1.0 * T * 0.082057338

    if species == 'H2O2':
        P = 1.0 * T * 0.082057338

    if species == 'H2O':
        P=1360.27598

    if species == 'H3O':
        P=(10**(-1.0*(float(sys.argv[3]))))*T*0.082057338

    if species == 'OH':
        P=(10**(-1.0*(14.0-float(sys.argv[3]))))*T*0.082057338

    if species == 'Li':
        P=(10**(-1.0*(14.0-float(sys.argv[3]))))*T*0.082057338

    if species == 'Na':
        P=(10**(-1.0*(14.0-float(sys.argv[3]))))*T*0.082057338

    if species == 'K':
        P=(10**(-1.0*(14.0-float(sys.argv[3]))))*T*0.082057338

    if species == 'Rb':
        P=(10**(-1.0*(14.0-float(sys.argv[3]))))*T*0.082057338

    if species == 'Cs':
        P=(10**(-1.0*(14.0-float(sys.argv[3]))))*T*0.082057338

    if species != 'H2O2' and species != 'OOH' and species != 'H3O' and species != 'OH' and species != 'H2O' and species != 'Li' and species != 'Na' and species != 'K' and species != 'Rb' and species != 'Cs':
        P=24.46539532

    #
    # This deactivate the above corrections
    #
    P=1.0

    # Calculation of the translational partition function and the translational contribution to the entropy
    qt = (((2 * pi * mass_kg * boltzman * T) / (planck * planck)) ** (1.5)) * ((boltzman * T) / (P*101325))
    Strans = 0.008314462175 * ((math.log(qt)) + 1 + 1.5)

    # Calculation of the translational contribution to the internal energy
    Utrans = 0.0124716932625 * T

    # Calculation of the electronic contribution to the entropy
    Selec = 0.008314462175 * (math.log(float(multiplicity)))

    H = (float(E) * 2625.50) + (0.008314462175 * T) + ((float(Uelec) + float(Urot) + float(Utrans) + float(TotUvib)))
    G = (float(E) * 2625.50) + (0.008314462175 * T) + ((float(Uelec) + float(Urot) + float(Utrans) + float(TotUvib))) - T*(
                    (float(Selec) + float(Srot) + float(Strans) + float(TotSvib)))

#
# Uncomment to verify Thermochemistry
#
#    print(species)
#    print(E,H/2625.50,G/2625.50)
#    print(Uelec/4.184,Utrans/4.184,Urot/4.184,TotUvib/4.184)
#    print(Selec/0.004184,Strans/0.004184,Srot/0.004184,TotSvib/0.004184)
#

    return


#
# Initialiazation of Variables
#

type=''
type_name=[]
type_value=[]

#
# Read the types (atom, linear or molecule)
#

file = open("Types.dat", "r")
for line in file:
    tmp=line.split()
    type_name.append(tmp[0])
    type_value.append(tmp[1])
file.close()

#
# Start of the loops
#

count=0
output_path = 'outputs/'

for filename in sorted(os.listdir(output_path)):

#
# Initialization of Variables
#

    multiplicity=1
    Rot_Number=1
    frequencies=[]
    x=[]
    y=[]
    z=[]
    atomic_mass=[]
    T=0.0
    P=0.0
    natoms=0
    mass=0.0
    E=0.0
    H=0.0
    G=0.0

#
# Creation of the path
#
    species=''

    #
    # Select .out for ADF and .log for Gaussian
    #
    species=str(filename.strip('.out'))

    path=str(output_path)+str(filename)
    output = open("scratch/Energy_"+str(species)+".dat","w")

    #
    # Assign the type to describe the atom, linear molecule and 3D molecules
    #
    type = 'molecule'
    for i in range(0, len(type_name)):
        if str(type_name[i]) == str(species):
            type = str(type_value[i])

    #
    # Get all the data from the output.
    #
    ADF(path)

    #
    # Compute the moment of inertia
    #
    if type != 'atom':
        Moment_of_Intertia()
    if type == 'atom':
        inx = 0.0
        iny = 0.0
        inz = 0.0

    #
    # Replaces frequencies below 100 cm-1 to 100 cm-1
    #
    Frequency_Replacement(0)

    T=float(sys.argv[1])
    P=float(sys.argv[2])

    #
    # Calculates the Thermochemistry
    #
    Thermochemistry(T,P)

    #
    # Write the values into files
    #
    output.write(str(H)+' '+str(G))
    output.close()
    count=count+1

subprocess.call("rm momentinertia.dat ", shell=True)
