
def reaction_matrix(output_path,species):
    import os

    #
    # Select the extension of the output
    #
    for filename in sorted(os.listdir(output_path)):
        species.append(filename.strip('.out'))

    #
    # Open the list of reactions
    #

    file = open("Reactions.dat", "r")
    output = open("scratch/ReactionMatrix.dat", "w")
    for line in file:
        tmp = line.strip('\n').split()

        zero = 0
        reaction = []
        for i in range(0, len(species)):
            reaction.append(zero)

        sign = -1
        for i in range(0, len(tmp)):
            for j in range(0, len(species)):
                if str(tmp[i]) == str(species[j]):
                    reaction[j] = sign * int(tmp[i - 1])
                if str(tmp[i]) == '>>>':
                    sign = 1
        tmp2 = ''
        for i in range(0, len(reaction)):
            tmp2 = tmp2 + str(reaction[i])
            tmp2 = tmp2 + str(' ')
        output.write(str(tmp2) + '\n')

    file.close()
    output.close()


output_path = 'outputs'
species=[]
reaction_matrix(output_path,species)
