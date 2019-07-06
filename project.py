import numpy as np

from abd import calculate_ABD, get_layers

A,B,D, layers = calculate_ABD(
    lam_file='BladeLaminateCored.csv', 
    lam_dir='designlib/project/', 
    mat_dir='designlib/project/'
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
    1695,
    0,
    0
]).T

# compute strains from loads, matrix multiplication
strains = np.linalg.inv(ABD) @ applied_loads
e = strains[:3]
K = strains[3:]
print()
print('strains:')
print(strains)

# define allowables
tensile_strength = 610e3 # psi
compressive_strength = -8.7e3 # psi

# compute stress in each layer and MS
print('\nstresses:')
for layer in layers:
    layer.stress = layer.Q @ e +  layer.Q @ K * layer.z_lower
    if layer.stress[0] < 0:
        layer.MS = compressive_strength / layer.stress[0] - 1
    elif layer.stress[0] > 0:
        layer.MS = tensile_strength / layer.stress[0] - 1
    else:
        layer.MS = 'Very high'
    print(f'layer: {layer.orientation}, stress: {layer.stress}, MS: {layer.MS}')