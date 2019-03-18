
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


def read_file(fp):
    '''reads the file at `fp`
    returns a list of the layers'''
    layers: Layer = []

    with open(fp, 'r') as f:

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
    return layers


def calculate_z(layers):
    '''Calculates the z distance IN PLACE
    for each layer in `layers`'''

    # find total height of the laminate
    height = sum(layer.thickness for layer in layers)

    # assign z for each layer
    current_height = -1 * (height / 2)
    for layer in layers:
        next_height = current_height + layer.thickness
        layer.z_lower = current_height
        layer.z_upper = next_height
        current_height = next_height


def retreive_mat_data(layers, pre_fp=''):
    '''retreive the material data for each layer IN PLACE
    Gets from a file located in the directory `pre_fp`'''
    # read in the material values for each layer
    for layer in layers:

        # read json file
        with open(pre_fp + layer.materialname + '.json', 'r') as f:
            mat = json.load(f)
        
        # assign properties
        layer.E1 = float(mat['modulus']['E1'])
        layer.E2 = float(mat['modulus']['E2'])
        layer.G12 = float(mat['modulus']['G12'])
        layer.v12 = float(mat['modulus']['v12'])
        try:
            layer.Q_nominal = np.array(mat['modulus']['Q'], dtype=float)
        except:
            layer.Q_nominal = make_Q(
                layer.E1,
                layer.E2,
                layer.G12,
                layer.v12
            )


def rotate_layers(layers):
    '''rotate each layer by it's orientation
    sets a new Q matrix for the layer IN PLACE'''
    # rotate Q matrices of each layer
    for layer in layers:
        layer.Q = rotate_Q(
            layer.Q_nominal, 
            layer.orientation * np.pi / 180
        )

        # set values close to zero equal to zero
        with np.nditer(layer.Q, op_flags=['readwrite']) as it:
            for x in it:
                if abs(x) <= 1e-5:
                    x[...] = 0


def calculate_ABD_from_layers(layers):
    '''Calculates the A, B, D matrices for the layers
    returns: A, B, D'''
    # find A, B, D
    A = np.zeros((3,3))
    B = np.zeros((3,3))
    D = np.zeros((3,3))
    for layer in layers:
        A = A + layer.Q * (layer.z_upper - layer.z_lower)
        B = B + (1/2) * layer.Q * (layer.z_upper**2 - layer.z_lower**2)
        D = D + (1/3) * layer.Q * (layer.z_upper**3 - layer.z_lower**3)
    return A, B, D


def calculate_ABD(lam_file, lam_dir='', mat_dir=''):
    '''Calculates the ABD matrix from a `laminate file`
    The laminate file is located in directory `lam_dir`
    The material file is located in directory `mat_dir`'''
    lam_fp = lam_dir + lam_file
    layers = read_file(lam_fp)
    calculate_z(layers)
    retreive_mat_data(layers, mat_dir)
    rotate_layers(layers)
    A, B, D = calculate_ABD_from_layers(layers)
    return A, B, D



if __name__ == '__main__':
    A,B,D = calculate_ABD(
        lam_file='problem1.csv', 
        lam_dir='designlib/', 
        mat_dir='designlib/')
    
    print('A = \n{}\n'.format(A))
    print('B = \n{}\n'.format(B))
    print('D = \n{}'.format(D))