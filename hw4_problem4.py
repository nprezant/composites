import numpy as np

from abd import calculate_ABD, get_layers

A,B,D = calculate_ABD(
    lam_file='problem4.csv', 
    lam_dir='designlib/hw4/', 
    mat_dir='designlib/hw4/'
)

layers = get_layers(
    lam_file='problem4.csv', 
    lam_dir='designlib/hw4/', 
    mat_dir='designlib/hw4/'
)

# print('A = \n{}\n'.format(A))
# print('B = \n{}\n'.format(B))
# print('D = \n{}'.format(D))

AB = np.append(A,B,axis=1)
BD = np.append(B,D,axis=1)
ABD = np.append(AB,BD,axis=0)

# applied load
applied_loads = np.array([
    0,
    0,
    0,
    -900,
    0,
    0
]).T

# allowable loads, matrix multiplication
strains = np.linalg.inv(ABD) @ applied_loads
K = strains[3:]

# compute stress in bottom layer
bottom_layer = layers[0]
stress = bottom_layer.Q @ K * bottom_layer.z_lower

print(K)
print(stress)
