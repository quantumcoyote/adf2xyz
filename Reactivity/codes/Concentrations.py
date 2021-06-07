import os
import sys

species=[]
output_path = 'outputs'

#
# Reads filenames
#

for filename in sorted(os.listdir(output_path)):
    species.append(filename.strip('.out'))

#
# Specify the concentrations
#

output = open("scratch/Concentrations.dat","w")
for i in range(0,len(species)):

    #
    # Select 55.6 M if water is the solvent and 1.0 M if water is NOT the solvent. Hydroxide and hydronium ions are
    # pH dependent, and the concentrations of cations are equal to the hydroxide concentration.
    #
    if str(species[i])=='H2O':
      output.write(str(species[i]) + '  55.6 \n')

    if str(species[i])=='Li':
      output.write(str(species[i]) + '  '+str(10**(-1.0*(14.0-float(sys.argv[1]))))+' \n')

    if str(species[i])=='Na':
      output.write(str(species[i]) + '  '+str(10**(-1.0*(14.0-float(sys.argv[1]))))+' \n')

    if str(species[i])=='K':
      output.write(str(species[i]) + '  '+str(10**(-1.0*(14.0-float(sys.argv[1]))))+' \n')

    if str(species[i])=='Rb':
      output.write(str(species[i]) + '  '+str(10**(-1.0*(14.0-float(sys.argv[1]))))+' \n')

    if str(species[i])=='Cs':
      output.write(str(species[i]) + '  '+str(10**(-1.0*(14.0-float(sys.argv[1]))))+' \n')

    if str(species[i])=='OH':
      output.write(str(species[i]) + '  '+str(10**(-1.0*(14.0-float(sys.argv[1]))))+' \n')

    if str(species[i])=='H3O':
      output.write(str(species[i]) + '  '+str(10**(-1.0*(float(sys.argv[1]))))+' \n')

    if str(species[i])=='OOH':
      output.write(str(species[i])+'  1.0 \n')

    if str(species[i])=='H2O2':
      output.write(str(species[i])+'  1.0 \n')

    #
    # All other species are 1 M in solution
    #
    if str(species[i]) !='H2O2' and str(species[i]) !='Li' and str(species[i]) !='Na' and str(species[i]) !='K' and str(species[i]) !='Rb' and str(species[i]) !='Cs' and str(species[i]) !='OH' and str(species[i]) !='H2O' and str(species[i])!='H3O' and str(species[i])!='OOH':
      output.write(str(species[i])+'  1.0 \n')
output.close()
