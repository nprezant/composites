import numpy as np

from abd import calculate_ABD

A,B,D = calculate_ABD(
    lam_file='Shaft1.csv', 
    lam_dir='designlib/project/', 
    mat_dir='designlib/project/'
)

print('A = \n{}\n'.format(A))
print('B = \n{}\n'.format(B))
print('D = \n{}'.format(D))

AB = np.append(A,B,axis=1)
BD = np.append(B,D,axis=1)
ABD = np.append(AB,BD,axis=0)

applied = np.array([
    100,
    0,
    0,
    0,
    0,
    0
]).T

# strains
allowable = np.array([
    0.025,
    0.0375,
    0.02,
    0,
    0,
    0
]).T

allowable = np.array([
    0.025,
    0,
    0,
    0,
    0,
    0
]).T

# allowable loads, matrix multiplication
loads = ABD @ allowable

print(loads)
