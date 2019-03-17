
# Problem 4, Rotate Q Matrices

from collections import namedtuple

import numpy as np


def T(t):
    '''Returns a tranformation matrix at angle `t`
    Usage:
    [sigma] = [T][sigma]'''
    return np.array(
        [[np.cos(t)**2,         np.sin(t)**2,           2*np.sin(t)*np.cos(t)],
        [np.sin(t)**2,          np.cos(t)**2,           -2*np.sin(t)*np.cos(t)],
        [-np.sin(t)*np.cos(t),  np.sin(t)*np.cos(t),    np.cos(t)**2 * np.sin(t)**2]]
    )


def make_Q(E1, E2, G12, v12):
    '''makes a Q matrix from lamina level properties'''
    v21 = E2 / E1 * v12
    Q11 = E1 / (1 - v12 * v21)
    Q22 = E2 / (1 - v12 * v21)
    Q12 = v12 * Q22
    Q66 = G12
    return np.array(
        [[Q11, Q12, 0],
        [Q12, Q22, 0],
        [0, 0, Q66]]
    )



def rotate_Q(Q, t):
    '''Returns matrix Q, rotated by angle `t`'''
    m = np.cos(t)
    n = np.sin(t)

    Q11 = Q[0,0]
    Q12 = Q[0,1]
    Q22 = Q[1,1]
    Q66 = Q[2,2]

    Q11_rot = Q11 * m**4 + Q22 * n**4 + 2 * (Q12 + 2 * Q66) * m**2 * n**2
    Q12_rot = (Q11 + Q22 - 4*Q66) * m**2 * n**2 + Q12 * (m**4 + n**4)
    Q22_rot = Q11 * n**4 + Q22 * m**4 + 2 * (Q12 + 2*Q66) * m**2 * n**2
    Q16_rot = (Q11 - Q12 - 2*Q66) * m**3 * n + (Q12 - Q22 + 2*Q66) * m * n**3
    Q26_rot = (Q11 - Q12 - 2*Q66) * m * n**3 + (Q12 - Q22 + 2*Q66) * m**3 * n
    Q66_rot = (Q11 + Q22 - 2*Q12 - 2*Q66) * m**2 * n**2 + Q66 * (m**4 + n**4)

    return np.array(
        [[Q11_rot, Q12_rot, Q16_rot],
        [Q12_rot, Q22_rot, Q26_rot],
        [Q16_rot, Q26_rot, Q66_rot]]
    )


def Q2props(Q):
    '''Convert a Q matrix into it's effective properties'''

    Q11 = Q[0,0]
    Q12 = Q[0,1]
    Q22 = Q[1,1]
    Q66 = Q[2,2]

    E1 = Q11 * (1 - Q12**2 / (Q11*Q66))
    E2 = Q22 * (1 - Q12**2 / (Q11*Q66))
    v21 = Q12 / Q11
    v12 = E1 / E2 * v21
    G12 = Q66

    return E1, E2, v12, v21, G12


if __name__ == '__main__':
    Q = np.array(
        [[150, 5, 0],
        [5, 20, 0],
        [0, 0, 5]]
    )

    Q30 = rotate_Q(Q, 30*np.pi/180)
    Q45 = rotate_Q(Q, 45*np.pi/180) 
    Q60 = rotate_Q(Q, 60*np.pi/180) 

    LaminaProperties = namedtuple('LaminaProperties', 'E1, E2, v12, v21, G12')
    props0 = LaminaProperties._make ( Q2props( Q    ) )
    props30 = LaminaProperties._make( Q2props( Q30  ) )
    props45 = LaminaProperties._make( Q2props( Q45  ) )
    props60 = LaminaProperties._make( Q2props( Q60  ) )

    def print_lamina(lam:LaminaProperties):
        s = ''
        for fld in lam._fields:
            s += '{:5} = {:8.4g},   '.format(fld, getattr(lam, fld))
        print(s)

    print('Q = '   + str(Q)   + '\n')
    print('Q30 = ' + str(Q30) + '\n')
    print('Q45 = ' + str(Q45) + '\n')
    print('Q60 = ' + str(Q60) + '\n')

    print_lamina(props0)
    print_lamina(props30)
    print_lamina(props45)
    print_lamina(props60)