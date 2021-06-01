from subprocess import Popen, STDOUT, PIPE
import subprocess
import sys
import math
import os

def ADF(path):
    global x
    global y
    global z
    global name
    global natoms
    global energy

    #
    # Initialize Function Variables
    #

    nline=0
    geo=0
    endgeo=0

    with open(path, 'r') as searchfile:
        for line in searchfile:
            if 'Atom         X           Y           Z   (Angstrom)' in line:
                geo = int(nline)
            if '>>>> CORORT' in line:
                endgeo = int(nline)
            if '   Bond Energy     ' in line:
                energy = float(line.split()[4])
            nline=nline+1
        natoms=int((int(endgeo) - int(geo) - 1))

        nline = 1
        with open(path, 'r') as searchfile:
            for line in searchfile:
                if int(geo) + 1 < int(nline) < int(endgeo)+1:
                    tmp = line.split()
                    name.append(((tmp[0].replace('.',' '))).split()[1])
                    x.append(tmp[1])
                    y.append(tmp[2])
                    z.append(tmp[3])
                nline = nline + 1


#
# Initialize the variables
#

x=[]
y=[]
z=[]
name=[]
energy=0.0
path = sys.argv[1]

#
# Get all the data from the output.
#

ADF(path)

#
# Write the values into file
#

output = open(sys.argv[2],"w")
output.write(str(natoms) + ' \n')
output.write("Energy= %10.3f kcal/mol \n" % energy)

for i in range(0, len(x)):
        output.write("%s %10.6f %10.6f %10.6f \n" % (name[i], float(x[i]), float(y[i]), float(z[i])))

output.write(' \n')
output.write(' \n')