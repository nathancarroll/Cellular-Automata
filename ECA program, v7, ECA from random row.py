#Version 7:
#-Includes implementation for more than 2 cell values and cell colorings.

#Possible next steps:
#-Adapt code for filters via Shalizi.
#-Add code to have either continuous display or a display that can be continued
#over with the click of a button.

'''
Code that will generate an image of 1-D cellular automaton.
'''
import sys
import random
import time
import pygame
import itertools

def generate_rule(rule_number, number_of_neighbors=3, values=[1, 0]): #Trying this outside of a class.
    '''Generates a rule from the number classification input and other parameters.
    `number_of_neighbors` takes an int and is how many above neighbors are inputs for each cell
        -e.g., nearest neighbor is 3, next nearest neighbor is 5, etc...
    `values` takes a list of all possible values cells can take, which must be translated into ints 0 - n.
        -fyi, the order of the items makes a difference in how the rule is implemented. Reverse order if troubleshooting.
        -Maybe there's a way to do this without using ints as values, but it seems practical for now.'''
    rules_dict = {}

    #Tells you if you entered an invalid rule number given the other parameters.
    if rule_number >= (len(values) ** (len(values) ** number_of_neighbors)):
        print ('rule_number too large to index to given rule values and number_of_neighbors.')
        sys.exit()

    #Generates a list of all possible codons.
    codons = list(itertools.product(values, repeat=number_of_neighbors)) #Gives a list of tuples.
    for index, elem in enumerate(codons): #Turns into a list of lists.
        codons[index] = list(elem)

    #Creates a string of the rule_number in the base equal to the number of values and number of digits equal to the number of codons.
    n = rule_number
    base = len(values)
    xary = ''
    while n > 1:
        xary = str(n%base) + xary
        n = n//base
    xary = str(n%base) + xary

    while len(xary) < len(codons): #Adds extra zeros to the front of the number so all codons are matched to a value.
        xary = '0' + xary

    #Turns the list of lists of codons into a list of strings, which can each be hashed in the dict.
    codons_as_strings = codons 
    for index, triplet in enumerate(codons):
        codon_string = ''
        for elem in triplet:
           codon_string = codon_string + str(elem)
        codons_as_strings[index] = codon_string

    #Pairs all codons with an output value in a dictionary
    for index, triplet in enumerate(codons_as_strings):
        rules_dict[triplet] = xary[index]

    #Print for convenience.
    print ('Cellular Automata Rule #' + str(rule_number))
    for codon in rules_dict:
        print (codon, ':', rules_dict.get(codon))
        
    return rules_dict


class Generator(object):
    '''An object which generates a single wedge based on an initial seed
    and a rule. If the seed is `None`, a random one will be generated.'''
    def __init__(self, seed=None, rule=generate_rule(112)):
        self.seed = seed
        self.rule = rule

    def _generate_seed(self, seed=None):
        '''Takes a seed and converts it into an integer.
        If the seed is `None`, a random seed based on system time
        will be generated.'''
        to_int = lambda item : int(''.join([str(ord(x)) for x in str(item)]))
        if seed is None:
            return to_int(time.time())
        elif type(seed) in (int, long):
            return seed
        else:
            return to_int(seed)

    def random_first_row(self, grid_width, values=[1, 0]):
        '''Creates a first row of random cell values.'''
        first_row = ''
        for i in range(grid_width):
            first_row += str(random.choice(values))
        return first_row

    def _calculate_row(self, previous_row):
        '''Generates the next row based on the previous row. Includes code
        for wrap-around effect.'''
        def _above(row):
            previous_row = row[-1] + row + row[0]   #wrap-around
            for i in range(len(previous_row) - 2):
                yield previous_row[i: i+3]

        return ''.join(self.rule[i] for i in _above(previous_row))

    def _calculate_row_randomness(self, previous_row, randomness=0, values=[1,0]):
        '''Generates the next row based on the previous row. Includes code
        for wrap-around effect.'''
        def _above(row, randomness):
            previous_row = row[-1] + row + row[0]   #wrap-around
            for i in range(len(previous_row) - 2):
                if randomness > 0 and random.random() < randomness:
                    yield (str(random.choice(values)) + str(random.choice(values))
                        + str(random.choice(values)))
                else:
                    yield previous_row[i: i+3]

        return ''.join(self.rule[i] for i in _above(previous_row, randomness)) #This returns a str.

    def generate(self, n=None, grid_width=None, randomness=0, values=[1,0]):
        '''Yields n rows.'''
        row = self.random_first_row(grid_width, values)
        yield row
        if n == None: #My guess this is for if you just want to somehow run the program without specifying an end point.
            while True:
                row = self._calculate_row(row)
                yield row
        elif randomness > 0:
            for i in range(n - 1): #`-1` to account for randonly generated first row.
                row = self._calculate_row_randomness(row, randomness, values)
                yield row
        else:
            for i in range(n - 1): #`-1` to account for randonly generated first row.
                row = self._calculate_row(row)
                yield row

    def create_grid(self, n, grid_width, randomness=0, values=[1,0]):
        '''Returns a `Grid` object `n` rows long, yielding
        a rectangle of size `grid_width` by `n`.'''
        height = n  
        width = grid_width
        grid = []

        for row in self.generate(n, grid_width, randomness, values):
            grid.append(row)

##        print ('grid =', grid) #A common test to use.

        return grid

    def __call__(self, *args, **kwargs):
        '''A convenience function to create a grid.'''
        return self.create_grid(*args, **kwargs)

class PygameRenderer(object):
    '''Renders a grid object using Pygame, and also contains code to
    save the current grid.'''
    def __init__(self, n, grid_width, pixel_size, colors):
        self.pixel_size = pixel_size
        width = grid_width
        height = n 
        self.size = (width * self.pixel_size, 
                     height * self.pixel_size)
        self.colors = colors
        self.background = colors['0']

        self._configure_pygame()
        self._configure_graphics()

        self.grid = None

    def _configure_pygame(self):
        pygame.init()
        pygame.display.set_mode(self.size)
        self.surface = pygame.display.get_surface()

    def _configure_graphics(self):
        self.tile = pygame.Surface((self.pixel_size, self.pixel_size))

    def render(self, grid):
        '''Renders the grid, and prints the current seed to stdout.'''
        self.surface.fill(self.background) 
        if self.pixel_size == 1: #Colors in pixels of pixel_size == 1.
            for i, row in enumerate(grid):
                for j, elem in enumerate(row): 
                    self.surface.set_at((j * self.pixel_size, i * self.pixel_size), self.colors[elem])
        else: #For larger pixel size settings, colors in pixels. Is slower than pixel_size = 1 implementation.
            for i, row in enumerate(grid):
                for j, elem in enumerate(row):
                    self.tile.fill(self.colors[elem])
                    self.surface.blit(self.tile, (j * self.pixel_size, i * self.pixel_size))

        pygame.display.flip()

    def wait(self):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def refresh(self):
        '''Waits until Pygame is closed. Clicking any keyboard
        button will save the current image to the current directory,
        and clicking the mouse will break from the mainloop so that
        the containing function can create a new grid.'''
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return # Returns so that a new grid can be generated.
            elif event.type == pygame.KEYDOWN:
                filename = str(time.time()) + '.png'
                pygame.image.save(self.surface, filename)


def test_grid(n = 5, grid_width = 200, pixel_size = 16, rule=generate_rule(110),
              randomness=0, values=[1,0], number_of_neighbors=3,
              colors={'1': (0, 0, 0), '0': (255, 255, 255)}):
    '''Creates a normal grid.'''
    rule_dict = generate_rule(rule, number_of_neighbors, values)
    grid = Generator(rule=rule_dict)(n, grid_width, randomness, values)
    r = PygameRenderer(n, grid_width, pixel_size, colors)
    r.render(grid)
    while True:
        r.refresh()


if __name__ == '__main__':
    #For ECA.
##    test_grid(200, 200, 1, 106, 0)

    #For more complex CA.
##    test_grid(100, 100, 4, 106, 0, [2, 1, 0], 3,
##              {'2': (0, 0, 255), '1': (0, 0, 0), '0': (255, 255, 255)})
    test_grid(1000, 500, 1, 110, 0, [1, 0], 3,
              {'1': (0, 0, 0), '0': (255, 255, 255)})

#Good rules to use to do are 22, 30, 54, 90, 105, 106, 110, 150, 184. All of them
    #except 184 seem to have long-term effects and not settle into uniformity.
#110 is particularly juicy because the particle effects are so visually pronounced.
