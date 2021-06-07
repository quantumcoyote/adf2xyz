#
# Import sys library to use inline input.
#
import sys

#
# Dictionary with element symbols and element numbers.
#
element={'1':'H','2':'He','3':'Li','4':'Be','5':'B','6':'C','7':'N','8':'O','9':'F',
'10':'Ne','11':'Na','12':'Mg','13':'Al','14':'Si','15':'P','16':'S','17':'Cl','18':'Ar','19':'K',
'20':'Ca','21':'Sc','22':'Ti','23':'V','24':'Cr','25':'Mn','26':'Fe','27':'Co','28':'Ni','29':'Cu',
'30':'Zn','31':'Ga','32':'Ge','33':'As','34':'Se','35':'Br','36':'Kr','37':'Rb','38':'Sr','39':'Y',
'40':'Zr','41':'Nb','42':'Mo','43':'Tc','44':'Ru','45':'Rh','46':'Pd','47':'Ag','48':'Cd','49':'In',
'50':'Sn','51':'Sb','52':'Te','53':'I','54':'Xe','55':'Cs','56':'Ba','57':'La','58':'Ce','59':'Pr',
'60':'Nd','61':'Pm','62':'Sm','63':'Eu','64':'Gd','65':'Tb','66':'Dy','67':'Ho','68':'Er','69':'Tm',
'70':'Yb','71':'Lu','72':'Hf','73':'Ta','74':'W','75':'Re','76':'Os','77':'Ir','78':'Pt','79':'Au',
'80':'Hg','81':'Tl','82':'Pb','83':'Bi','84':'Po','85':'At','86':'Rn','87':'Fr','88':'Ra','89':'Ac',
'90':'Th','91':'Pa','92':'U','93':'Np','94':'Pu','95':'Am','96':'Cm','97':'Bk','98':'Cf','99':'Es',
'100':'Fm','101':'Md','102':'No','103':'Lr','104':'Rf','105':'Db','106':'Sg','107':'Bh','108':'Hs','109':'Mt',
'110':'Ds','111':'Rg','112':'Cn','113':'Nh','114':'Fl','115':'Mc','116':'Lv','117':'Ts','118':'Og'}

#
# Function that reads the ADF output to find :
#   - Optimized geometry.
#   - Frequencies.
#
def ADF():
    global negative
    global col_neg
    global position_neg
    global select
    global natoms

    #
    # Initialize Function Variables.
    #

    nline=0
    linefreq=0
    linefreqstart=0
    linefreqend=0

    with open(sys.argv[1], 'r') as searchfile:
        for line in searchfile:
            #
            # Find the line number before the final geometry is printed.
            #
            if '    Atom         X           Y           Z   (Angstrom)' in line:
                geo = int(nline)
            #
            # Find the line after the final geometry is printed.
            #
            if '  >>>> CORORT' in line:
                natoms = int(nline)

            #
            # Find the frequencies and identify in which column the
            # chosen negative frequency is located. (EDIT LATER)
            #
            if '                cm-1           1e-40 esu2 cm2          km/mole' in line:
                linefreq=nline

            if '(a negative value means an imaginary frequency, no output for (almost-)zero frequencies)' in line:
                linefreqstart=nline

            if 'List of All Frequencies:' in line:
                linefreqend=nline


            nline = nline + 1
    nline = 1
    natoms=natoms-geo-1

    with open(sys.argv[1], 'r') as searchfile:
        for line in searchfile:
            #
            # Read the frequencies.
            #
            if int(linefreq+2) < int(nline) < int(linefreq+2) +((3*natoms)-6) + 1:
               tmp=line.split()
               frequencies.append(tmp[0])
            nline = nline + 1

    nline=0
    with open(sys.argv[1], 'r') as searchfile:
        for line in searchfile:
          #
          # Read the displacements.
          #
          if int(linefreqstart) < int(nline) < int(linefreqend)-natoms :
            if((str(round(float(frequencies[select-1]),3)) in line) == True):
                searchfile.readline()
                for i in range(0,natoms):
                   tmp=(searchfile.readline().split())
                   number=select
                   for k in range(0,len(frequencies)):
                       if(number-3 == 0) or (number-3 < 0):
                          break
                       else:
                          number=number-3
                   if number==1:
                     dx.append(tmp[1])
                     dy.append(tmp[2])
                     dz.append(tmp[3])
                   if number==2:
                     dx.append(tmp[4])
                     dy.append(tmp[5])
                     dz.append(tmp[6])
                   if number==3:
                     dx.append(tmp[7])
                     dy.append(tmp[8])
                     dz.append(tmp[9])

          nline = nline + 1

    nline=0
    with open(sys.argv[1], 'r') as searchfile:
        for line in searchfile:
            #
            # Read optimized geometry.
            #
            if int(geo) < int(nline) < int(geo+1) + int(natoms):
                tmp = line.split()
                name.append(tmp[0].replace("."," ").split()[1])
                x.append(tmp[1])
                y.append(tmp[2])
                z.append(tmp[3])
            nline = nline + 1


#
# Initialization of Variables.
#
frequencies=[]
negative=0
nline=1
name=[]
x=[]
y=[]
z=[]
dx=[]
dy=[]
dz=[]
position_neg=[]
col_neg=[]

#
# Input of the displacement to apply and the negative frequency to correct.
#
disp=float(sys.argv[2])
select=int(sys.argv[3])

#
# Execute the function to obtain the optimized geometry and frequencies from
# the gaussian output.
#


ADF()
#
# Print the displaced geometry in the screen.
#
for i in range(0, len(name), 1):
        print(str(name[i]) + ' ' + str(float(x[i]) + (disp * float(dx[i]))) + ' ' + str(
            float(y[i]) + (disp * float(dy[i]))) + ' ' + str(float(z[i]) + (disp * float(dz[i]))))
