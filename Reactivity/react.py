import subprocess
import sys

#
# python3.6 react.py T(K) P(atm) pH(unitless)
#

#
# Create Reaction Matrix
#
subprocess.call("cp codes/ReactionMatrix.py .", shell=True)
subprocess.call("python ReactionMatrix.py ", shell=True)
subprocess.call("rm ReactionMatrix.py", shell=True)

#
# Read the pressure, temperature, and pH
#

T=float(sys.argv[1])
P=float(sys.argv[2])
pH=float(sys.argv[3])

#
# Update concentrations
# Comment to use your own concentration file.
#
subprocess.call("cp codes/Concentrations.py .", shell=True)
subprocess.call("python Concentrations.py "+str(pH), shell=True)
subprocess.call("rm Concentrations.py", shell=True)

#
# Calculate Thermochemistry
#
subprocess.call("cp codes/Thermochemistry.py .", shell=True)
subprocess.call("python Thermochemistry.py "+str(T)+" "+str(P)+" "+str(pH), shell=True)
subprocess.call("rm Thermochemistry.py", shell=True)

#
# Apply Non-Standard State Corrections
#
subprocess.call("cp codes/StandardState.py .", shell=True)
subprocess.call("python StandardState.py "+str(T)+" "+str(P)+" "+str(pH), shell=True)
subprocess.call("rm StandardState.py", shell=True)

#
# Clean Scratch Files
#
subprocess.call("rm scratch/*", shell=True)
