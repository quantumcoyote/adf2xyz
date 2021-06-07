import os
import math
import sys

output_path = 'scratch/'
species=[]
concentrations=[]
H=[]
G=[]
T=float(sys.argv[1])
P=float(sys.argv[2])
pH=float(sys.argv[3])
Reactions_G=[]

#
# Obtain the concentrations
#

for filename in sorted(os.listdir(output_path)):
    if "Concentrations.dat" in filename:
        file=open("scratch/"+str(filename),"r")
        for line in file:
            tmp=line.split()
            concentrations.append(tmp[1])
#
# Obtain the Enthalpy and Gibbs Free Energy
#
for filename in sorted(os.listdir('outputs')):
        species.append(str(filename.strip('.out')))

for filename in sorted(os.listdir(output_path)):
    if "Energy" in filename:
        file=open("scratch/"+str(filename),"r")
        for line in file:
            tmp = line.strip('\n').split()
            H.append(tmp[0])
            G.append(tmp[1])
        file.close()

#
# Apply the reaction matrix
#
print('#############################')
print('###### THERMOCHEMISTRY ######')
print('#############################')
print('')
print('Pressure = %5.2f atm' %(P))
print('Temperature = %5.2f K' %(T))
print('pH = %5.2f' %(pH))
print('')
print('######### REACTIONS #########')
print('All energies in kcal/mol')
print('')

reaction_number=1
file_labels = open("Reactions.dat","r")
for filename in sorted(os.listdir(output_path)):
    if "ReactionMatrix.dat" in filename:
        file=open("scratch/"+str(filename),"r")
        for line in file:
            tmp = line.strip('\n').split()
            stdstate=1.0
            Tot_G=0.0
            Tot_H=0.0
            Tot_G_std=0.0
            Tot_H_std=0.0
            plot = open("scratch/plot" + str(reaction_number) + ".dat", "a")

            #
            # Get the standard state correction
            #
            for i in range(0,len(tmp)):
                if(float(tmp[i])) < 0.0:
                    stdstate = stdstate * (1/(float(concentrations[i])**(-1.0*float(tmp[i]))))
                if(float(tmp[i])) > 0.0:
                    stdstate = stdstate * ((float(concentrations[i])**(float(tmp[i]))))
                Tot_H=Tot_H+(float(tmp[i])*float(H[i]))
                Tot_G=Tot_G+(float(tmp[i])*float(G[i]))
            stdstate=0.008314462175*T*math.log(stdstate)

            #
            # Apply standard state and unit conversion from kJ/mol to kcal/mol
            #

            Tot_H_std=(Tot_H+stdstate)/4.184
            Tot_G_std=(Tot_G+stdstate)/4.184
            Tot_H=(Tot_H)/4.184
            Tot_G=(Tot_G)/4.184
            reac=str(file_labels.readline().strip('\n'))

            #
            # Print reaction + dG_std. Uncomment to print other combinations
            #
            #print("%i )   %s   dG=%5.1f kcal/mol" % (reaction_number, reac, Tot_G_std))
            #print("%i )   %s   %5.2f   %5.2f" % (reaction_number, reac, Tot_H_std, Tot_G_std))
            print("%i )   %s   %5.2f   %5.2f   %5.2f %5.2f"% (reaction_number, reac, Tot_H, Tot_G, Tot_H_std, Tot_G_std))

            plot.write(str(P)+' '+str(T)+' '+str(pH)+' '+str(Tot_G_std)+'\n')
            reaction_number=reaction_number+1
            plot.close()
        file.close()
file_labels.close()

print('')
print('###### CONCENTRATIONS #######')
print('')
for i in range (0,len(concentrations)):
    if(float(concentrations[i]) > 0.01):
        print("[%s] \t %7.2f M" % (species[i],float(concentrations[i])))
    else:
        print("[%s] \t %7.2e M" % (species[i],float(concentrations[i])))
print('')
print('############ END ############')
