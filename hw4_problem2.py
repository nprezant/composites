import numpy as np

from abd import calculate_ABD

A,B,D = calculate_ABD(
    lam_file='problem2.csv', 
    lam_dir='designlib/hw4/', 
    mat_dir='designlib/hw4/'
)

print('A = \n{}\n'.format(A))
print('B = \n{}\n'.format(B))
print('D = \n{}'.format(D))

AB = np.append(A,B,axis=1)
BD = np.append(B,D,axis=1)
ABD = np.append(AB,BD,axis=0)

# strains
strains = np.array([
    0.0002,
    -0.00002,
    0,
    1/3000,
    1/50000,
    0
]).T

# allowable loads, matrix multiplication
loads = ABD @ strains

print(loads)
