
import json

import numpy as np

from stiffness import (
    rotate_Q, 
    make_Q
)

# compute the ABD matrix

class Layer:
    '''Layer of a laminate'''

    def __init__(self):
        '''Makes a laminate layer'''
        self.orientation = None
        self.thickness = None
        self.materialname = None
        self.E1 = None
        self.E2 = None
        self.G12 = None
        self.v12 = None
        self.z_upper = None
        self.z_lower = None
        self.Q_nominal = None
        self.Q = None


layers: Layer = []

laminatefile = 'test2.txt'
with open(laminatefile, 'r') as f:

    # skip first line
    for _ in range(1):
        next(f)

    # make layers
    for row, line in enumerate(f):

        # read line and trim whitespace
        vals = line.split(',')
        vals = [v.strip() for v in vals]

        # read in layer value
        layer = Layer()
        layer.orientation = float(vals[1])
        layer.thickness = float(vals[2])
        layer.materialname = vals[3]

        # add layer to the stack
        layers.append(layer)

# reverse layers we read in so that we go bottom up?
layers.reverse()

# find total height of the laminate
height = sum(layer.thickness for layer in layers)

# assign z for each layer
current_height = -1 * (height / 2)
for layer in layers:
    next_height = current_height + layer.thickness
    layer.z_lower = current_height
    layer.z_upper = next_height
    current_height = next_height

# read in the material values for each layer
for layer in layers:

    # read json file
    with open(layer.materialname + '.json', 'r') as f:
        mat = json.load(f)
    
    # assign properties
    layer.E1 = mat['modulus']['E1']
    layer.E2 = mat['modulus']['E2']
    layer.E2 = mat['modulus']['E2']
    layer.G12 = mat['modulus']['G12']
    layer.v12 = mat['modulus']['v12']

# find Q matrices of each layer
for layer in layers:
    layer.Q_nominal = make_Q(
        layer.E1,
        layer.E2,
        layer.G12,
        layer.v12
    )
    layer.Q = rotate_Q(
        layer.Q_nominal, 
        layer.orientation
    )

# find A, B, D
A = np.zeros((3,3))
B = np.zeros((3,3))
D = np.zeros((3,3))
for layer in layers:
    A = A + layer.Q * (layer.z_upper - layer.z_lower)
    B = B + (1/2) * layer.Q * (layer.z_upper**2 - layer.z_lower**2)
    D = D + (1/3) * layer.Q * (layer.z_upper**3 - layer.z_lower**3)

# print ABD
print('A = \n{}\n'.format(A))
print('B = \n{}\n'.format(B))
print('D = \n{}'.format(D))