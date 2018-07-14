#Max Notes:
#-Code taken from https://codereview.stackexchange.com/questions/15304/generating-a-1d-cellular-automata-in-python
#and adapted syntactically from python 2 to 3 by adapting the print syntax
#and changing all "xrange" functions to "range". I also included all of the
#suggested changes made in the comments of that article to make it more efficient.

#Next steps:
#-Try to follow the program through step-by-step to see why it's not producing
#the grid/image correctly. There's many different places this could be getting
#stuck.

#Version 5:
#-Create a wrap-around version that starts from a random row.

#Version 5.6:
#-Calibrate to be able to use the rule generator.
#START HERE: Find a way to not have to create a grid of '0' values which then
#gets written over. Just create rows as you go and then there's no need for
#a starting grid or mutable objects in the form of lists.

#Possible next steps:
#-Adapt code to take ints as values instead of bools. START HERE
#-Adapt code for filters via Shalizi.


#!/usr/bin/env python
'''
Code that will generate a fractal or a pseudo-random fractal
based on an initial seed and any acceptable 1-d cellular automata
algorithm.
'''
import sys
import random
import time
import pygame

class Rules(object):
    '''Contains a variety of rules that determines if a cell should turn black 
    based on the cells in the row above. Each function is namespaced inside 
    the 'Rules' class for convenience.
    '''

    def generate_rule(self, rule_number, number_of_neighbors, values):
        '''Generates a rule from the number classification input and other parameters.
        `number_of_neighbors` takes an int and is how many above neighbors are inputs for each cell
            -e.g., nearest neighbor is 3, next nearest neighbor is 5, etc...
        `values` takes a list of all possible values cells can take, which must be translated into ints 0 - n.
            -fyi, the order of the items makes a difference in how the rule is implemented. Reverse order if troubleshooting.
            -Maybe there's a way to do this without using ints as values, but it seems practical for now.'''
        rules_dict = {}

        #Generates a list of all possible codons.
        codons = list(itertools.product(values, repeat=number_of_neighbors)) #Gives a list of tuples.
        for index, elem in enumerate(codons): #Turns into a list of lists.
            codons[index] = list(elem)

        #Creates a string of a number with a base equal to the number of values and number of digits equal to the number of codons.
        n = rule_number
        base = len(values)
        xary = ''
        while n > 1:
            xary = str(n%base) + xary
            n = n//base
        xary = str(n%base) + xary

        while len(xary) < len(codons): #Adds extra zeros to the front of the number so all codons are matched to a value.
            xary = '0' + xary

        #Pairs all inputs with an output
        codons_as_strings = codons #This is meant to turn the list of lists of codons into a list of strings, which can be hashed in the dict.
        for index, triplet in enumerate(codons):
            codon_string = ''
            for elem in triplet:
               codon_string = codon_string + str(elem)
            codons_as_strings[index] = codon_string

        for index, triplet in enumerate(codons_as_strings):
            rules_dict[triplet] = xary[index]

        return rules_dict #There's probably a better way to do this.
        

    @staticmethod
    def rule30ints(above):
        '''Colors a cell black if the cells above it are in the "black set"
        for this rule.'''
        rule_set = { '100': '1', '011': '1', '010': '1', '001': '1', '111': '0', '110': '0', '101': '0', '000': '0' }
        return rule_set[above]
    
    @staticmethod
    def rule30(above):
        '''Colors a cell black if the cells above it are in the "black set"
        for this rule.'''
        black_set = ( [True, False, False], [False, True, True], [False, True, False], [False, False, True]  )
        return above in black_set

    @staticmethod
    def rule54(above):
        '''Colors a cell black if the cells above it are in the "black set"
        for this rule.'''
        black_set = ( [True, False, True], [True, False, False], [False, True, False], [False, False, True]  )
        return above in black_set

    @staticmethod
    def rule90(above):
        '''Colors a cell black if the cells above it are in the "black set"
        for this rule.'''
        black_set = ( [True, True, False], [True, False, False], [False, True, True], [False, False, True] )
        return above in black_set

    @staticmethod
    def rule110(above):
        '''Colors a cell black if the cells above it are in the "black set"
        for this rule.'''
        black_set = ( [True, True, False], [True, False, True], [False, True, True], [False, True, False], [False, False, True]  )
        return above in black_set
    
    @staticmethod
    def rule150(above):
        '''Colors a cell black if the cells above it are in the "black set"
        for this rule.'''
        black_set = ( [False, False, True], [False, True, False], [True, False, False], [True, True, True] )
        return above in black_set

    @staticmethod
    def rule150randomized(above):
        '''Colors a cell black if there's an odd number of black cells above it 
        (although this rule will be ignored 0.05% of the time.'''
        black_set = ( [False, False, True], [False, True, False], [True, False, False], [True, True, True] )
        if above in black_set:
            return random.randint(0, 2000) != 0
        else:
            return False

    @staticmethod
    def rule184(above):
        '''Colors a cell black if the cells above it are in the "black set"
        for this rule.'''
        black_set = ( [True, True, True], [True, False, True], [True, False, False], [False, True, True] )
        return above in black_set

class Generator(object):
    '''An object which generates a single wedge based on an initial seed
    and a rule. If the seed is `None`, a random one will be generated.'''
    def __init__(self, seed=None, rule=Rules.rule150):
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

    def random_first_row(self, grid_width): #Still need to adapt for more values than binary.
        '''Creates a first row of random cell values.'''
        values = [0, 1]
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

##        return [self.rule(i) for i in _above(previous_row)] #Original that returns list.

        return ''.join(self.rule(i) for i in _above(previous_row)) #This returns a str.

    def generate(self, n=None, grid_width=None):
        '''Yields n rows.'''
        row = self.random_first_row(grid_width)
        yield row
        if n == None: #My guess this is for if you just want to program run without specifying an end point.
            while True:
                row = self._calculate_row(row)
                yield row
        else:
            for i in range(n - 1): #`-1` to account for randonly generated first row.
                row = self._calculate_row(row) 
                yield row

    def create_grid(self, n, grid_width):
        '''Returns a `Grid` object `n` rows long, yielding
        a rectangle of size `grid_width` by `n`.'''
        height = n  
        width = grid_width
        grid = Grid(width, height)
        # Takes raw coordinates and returns new ones 
        # based on the center of the grid.

        grid.seed = self._generate_seed(self.seed)
        random.seed(grid.seed)

        for row in self.generate(n, grid_width): #test
            print ('row =', row)

        for index, row in enumerate(self.generate(n, grid_width)):
            raw_x = index
            for i, cell in enumerate(row):
                if cell:  
                    raw_y = i
                    grid.set( raw_y, raw_x ) 

        return grid

    def __call__(self, *args, **kwargs):
        '''A convenience function to create a grid.'''
        return self.create_grid(*args, **kwargs)

class Grid(object):
    '''An object which holds an arbitrary grid of pixels.'''
    def __init__(self, x, y, seed=None):
        self.width = x
        self.height = y
        self.array = []
##        self.array = '' #test
        # The seed used to generate the grid.
        self.seed = seed
        for i in range(self.height): #test #Makes a list of string rows.
            row = ['0' * self.width]
            self.array.extend(row)
##        for i in range(self.height): #Original
##            self.array.append([False for i in range(self.width)])

        print ('self.array = ', self.array, len(self.array)) #test
    
    def get(self, x, y):
        return self.array[y][x]

##    def set(self, x, y, value=True):
##        self.array[y][x] = value

##    def set(self, x, y, value='1'): #test
##        self.array[y][x] = value

    def set(self, x, y, value='1'): #test
        self.array[y[x]] = value

class PygameRenderer(object):
    '''Renders a grid object using Pygame, and also contains code to
    save the current grid.'''
    def __init__(self, n, grid_width, pixel_size, 
                    background=(255, 255, 255), foreground=(0, 0, 0)):
        self.pixel_size = pixel_size
        width = grid_width
        height = n 
        self.size = (width * self.pixel_size, 
                     height * self.pixel_size)
        self.background = background
        self.foreground = foreground

        self._configure_pygame()
        self._configure_graphics()

        self.grid = None

    def _configure_pygame(self):
        pygame.init()
        pygame.display.set_mode(self.size)
        self.surface = pygame.display.get_surface()

    def _configure_graphics(self):
        self.tile = pygame.Surface((self.pixel_size, self.pixel_size))
        self.tile.fill(self.foreground)

    def render(self, grid):
        '''Renders the grid, and prints the current seed to stdout.'''
        self.grid = grid
        self.surface.fill(self.background)
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.grid.get(x, y):
                    self.surface.blit(
                        self.tile,
                        (x * self.pixel_size, y * self.pixel_size)
                    )
        pygame.display.flip()
        print (self.grid.seed)

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
                filename = str(self.grid.seed) + '.png'
                pygame.image.save(self.surface, filename)
                

class AsciiRenderer(object):
    '''Creates an ASCII version of the grid.'''
    def to_string(self, grid):
        out = []
        for x in range(grid.width):
            row = ['[']
            for y in range(grid.height):
                if grid.get(x, y):
                    row.append('#')
                else:
                    row.append(' ')
            row.append(']')
            out.append(''.join(row))
        return '\n'.join(out)

    def render(self):
        print (self.to_string())


def test_rows(n=5):
    '''Tests generating a series of rows.'''
    g = Generator()
    for index, row in enumerate(g.generate(n)):
        padding = " " * (n - index - 1)
        out = "[{0}{1}{0}]"
        print (out.format(padding, "".join("#" if n else " " for n in row)))

def test_grid(n = 5, grid_width = 200, pixel_size = 16, rule=Rules.rule150):
    '''Creates a normal grid.'''
    grid = Generator(rule=rule)(n, grid_width)
    r = PygameRenderer(n, grid_width, pixel_size)
    r.render(grid)
    while True:
        r.refresh()

def test_grid_randomized(n=256, pixel_size=1, rule=Rules.rule150randomized):
    '''Creates a randomized grid, and will repeatedly create a new one.'''
    g = Generator(rule=rule)
    r = PygameRenderer(n, pixel_size)

    while True:
        grid = g(n)
        r.render(grid)
        r.refresh()

def generate_single_random_grid(n=256, pixel_size=1, 
            rule=Rules.rule150randomized, seed=None):
    '''Creates a randomized grid.'''
    grid = Generator(rule=rule, seed=seed)(n)
    r = PygameRenderer(n, pixel_size)
    r.render(grid)
    r.refresh()

def profiling_test(n):
    Generator(rule=rule)(n)


if __name__ == '__main__':
    #test_rows()
    #test_grid(16, 4, Rules.rule150)
    #test_grid(256, 1, Rules.rule150)
    #test_grid(800, 1, Rules.rule150)
    test_grid(20, 20, 1, Rules.rule30ints)
    #test_grid_randomized(256, 1, Rules.rule150randomized)
    #profiling_test(256, 1, Rules.rule150)
