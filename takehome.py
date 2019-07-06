import numpy as np

from abd import calculate_ABD, get_layers

A,B,D, layers = calculate_ABD(
    lam_file='takehome.csv', 
    lam_dir='designlib/takehomeproblem/', 
    mat_dir='designlib/takehomeproblem/'
)

# print('A = \n{}\n'.format(A))
# print('B = \n{}\n'.format(B))
# print('D = \n{}'.format(D))

AB = np.append(A,B,axis=1)
BD = np.append(B,D,axis=1)
ABD = np.append(AB,BD,axis=0)

# applied strain
strains = np.array([
    0,
    0,
    0,
    1/254,
    0,
    0
]).T

# compute strains from loads, matrix multiplication
loads = ABD @ strains
print()
print('Loads:')
print(loads)