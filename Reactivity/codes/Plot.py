import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
import os
import sys

reaction_number=1
output_path = 'scratch/'

for filename in os.listdir(output_path):
    if "plot" in filename:
        plot=open("scratch/"+str(filename),"r")
        x = []
        y = []
        z = []

        if(str(sys.argv[1])=='1'):
            for line in plot:
                tmp=line.split()
                x.append(float(tmp[0]))
                y.append(float(tmp[1]))
                z.append(float(tmp[3]))

        if(str(sys.argv[1])=='2'):
            for line in plot:
                tmp=line.split()
                x.append(float(tmp[2]))
                y.append(float(tmp[1]))
                z.append(float(tmp[3]))

        #
        # Check if it is a punctual calculation
        #
        if (min(x) == max(x)):
            exit()
        if (min(y) == max(y)):
            exit()

        x=np.asarray(x)
        y=np.asarray(y)
        z=np.asarray(z)

        xi, yi = np.linspace(x.min(), x.max(), 10), np.linspace(y.min(), y.max(), 10)
        xi, yi = np.meshgrid(xi, yi)
        rbf = scipy.interpolate.Rbf(x, y, z, function='cubic')
        zi = rbf(xi, yi)

        plt.imshow(zi, vmin=z.min(), vmax=z.max(),origin='lower',extent=[x.min(), x.max(), y.min(), y.max()],aspect='auto',cmap='coolwarm')

        plt.colorbar()
        if(str(sys.argv[1])=='1'):
            plt.xlabel('Pressure (atm)')
            plt.ylabel('Temperature (K)')
        if(str(sys.argv[1])=='2'):
            plt.xlabel('pH')
            plt.ylabel('Temperature (K)')

        plt.savefig("plots/reaction"+str(reaction_number)+".png")
        plt.clf()
        plt.cla()
        reaction_number=reaction_number+1
