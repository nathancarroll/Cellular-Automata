x = int('1101101', 5)

print (x)


##n = 18
##base = 3
##xary = ''
##while n > 1:
##    xary = str(n%base) + xary
##    n = n//base
##xary = str(n%base) + xary
##
##print (xary)


##print (3 ** 2 ** 2)
##
##print (3 ** 3 ** 3)
##
##print (155555555555555 > 3**3**3)

##print(len('105330488576562345234538380193503486834235634352234234234534523452345345345634855675668'))

##colors={'1': (0, 0, 0), '0': (255, 255, 255)}
##
##for color in colors:
##    print (color)


##import itertools
##import sys
##def generate_rule(rule_number, number_of_neighbors=3, values=[1, 0]):
##    '''Generates a rule from the number classification input and other parameters.
##    `number_of_neighbors` takes an int and is how many above neighbors are inputs for each cell
##        -e.g., nearest neighbor is 3, next nearest neighbor is 5, etc...
##    `values` takes a list of all possible values cells can take, which must be translated into ints 0 - n.
##        -fyi, the order of the items makes a difference in how the rule is implemented. Reverse order if troubleshooting.
##        -Maybe there's a way to do this without using ints as values, but it seems practical for now.'''
##    rules_dict = {}
##
##    #Tells you if you entered an invalid rule number given the other parameters.
##    if rule_number >= (len(values) ** (len(values) ** number_of_neighbors)):
##        print ('rule_number too large to index to rule parameters.')
##        sys.exit()
##
##    #Generates a list of all possible codons.
##    codons = list(itertools.product(values, repeat=number_of_neighbors)) #Gives a list of tuples.
##    for index, elem in enumerate(codons): #Turns into a list of lists.
##        codons[index] = list(elem)
##
##    #Creates a string of a number with a base equal to the number of values and number of digits equal to the number of codons.
##    n = rule_number
##    base = len(values)
##    xary = ''
##    while n > 1:
##        xary = str(n%base) + xary
##        n = n//base
##    xary = str(n%base) + xary
##
##    while len(xary) < len(codons): #Adds extra zeros to the front of the number so all codons are matched to a value.
##        xary = '0' + xary
##
##    #Pairs all inputs with an output
##    codons_as_strings = codons #This is meant to turn the list of lists of codons into a list of strings, which can be hashed in the dict.
##    for index, triplet in enumerate(codons):
##        codon_string = ''
##        for elem in triplet:
##           codon_string = codon_string + str(elem)
##        codons_as_strings[index] = codon_string
##
##    for index, triplet in enumerate(codons_as_strings):
##        rules_dict[triplet] = xary[index]
##
##    return rules_dict #There's probably a better way to do this.
##
##x = generate_rule(5000000000, 5, [1, 0])
##for i in x:
##    print (i, x[i])


##x = 'abcd'
##y = ['1234', 2, 3, 4]
##
##print (y[1, 1])


##x = {'a': 1, 'b': 2}
##
##print (x['a'])

##import random
##
##x = [1, 2, 3]
##y = ''
##for i in x:
##    y += str(i)
##
##z = ['0' * 4]
##
##x.extend(z)
##
##print (x[3])


##values = [0,1]
##x = 'abc'
##dicty = {}
##for i in x:
##    dicty[i] = values[int(1)] 
##
##for i in dicty:
##    print (i, dicty[i])

##n = 184
##base = 2
##xary = ''
##while n > 1:
##    xary = str(n%base) + xary
##    n = n//base
##xary = str(n%base) + xary
##
##print (xary)

#This code works!!!:
##n = 16
##base = 3
##x = ''
##
##while n > 1:
##    x = str(n%base) + x
##    n = n//base
##
##x = str(n%base) + x
##
##print (x)  

##x = [1,2,3]
##y = ''
##
##for i in x:
##    y = y + str(i)
##
##print (y)


##import itertools
##x = ['a', 'b', 'c', 'd']
##values = [True, False]
##number_of_neighbors = 3
##codons = list(itertools.product(values, repeat=number_of_neighbors))
##
##print (codons)
##
##for index, elem in enumerate(codons):
##    codons[index] = list(elem)
##
##print(codons)

##rule_number = 54
##
##z = "{0:b}".format(rule_number)
##
##print (z)

# Function to print binary number for the 
# input decimal using recursion

#This one works, I just want to return the value instead of print it.
##def decimalToXary(n, base):
##    '''Takes a decimal int `n` and returns it in the base representation `base`.'''
##    print (n)
##    if n > 1:
##         #  divide with integral result 
##         # (discard remainder) 
##        decimalToXary(n//base, base)
##
##    print (n%base, end ='')
##
##    
##x = decimalToXary(6, 2)

  

##def decimalToXary(n, base):
##    '''Takes a decimal int `n` and returns it in the base representation `base`.'''
##    if n > 1:
##         #  divide with integral result 
##         # (discard remainder) 
##        decimalToXary(n//base, base) 
## 
##    return str(n%base)
##
##x = decimalToXary(8, 3)
##
##print (x)
 
 #Driver code
##if __name__ == '__main__':
##    decimalToXary(8, 3)
##    print
##    decimalToBinary(18)
####    print
##    decimalToBinary(7)
####    print
