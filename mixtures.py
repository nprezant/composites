
# Problem 1, Effective lamina properties through mixture equations

class EffectiveLamina:
    def __init__(self, Ef, Em, Vf, Vm, nuf, num):
        '''Holds and computes Effective lamina properties.
        Based on matrix and fiber properties.'''
        self.E1 = E1(Ef, Em, Vf, Vm)
        self.E2 = E2(Ef, Em, Vf, Vm)
        self.v12 = v12(Vf, Vm, nuf, num)
        self.Gf = G(Ef, nuf)
        self.Gm = G(Em, num)
        self.G12 = G12(self.Gf, self.Gm, Vf, Vm)


def E1(Ef, Em, Vf, Vm):
    return Ef * Vf + Em * Vm


def E2(Ef, Em, Vf, Vm):
    return (Ef * Em) / (Vf*Em + Vm*Ef)


def v12(Vf, Vm, nuf, num):
    return Vf * nuf + Vm * num


def G12(Gf, Gm, Vf, Vm):
    return (Gf * Gm) / (Vf * Gm + Vm * Gf)


def G(E, nu):
    return E / (2 * (1 + nu))


if __name__ == '__main__':

    problem1_props = {
        'Ef': 160,
        'Em': 4.5,

        'nuf': 0.2,
        'num': 0.33,

        'Vf': 0.62,
        'Vm': 0.38
    }

    problem3_props = {
        'Ef': 37,
        'Em': 1.1,

        'nuf': 0.25,
        'num': 0.25,

        'Vf': 0.605,
        'Vm': 0.395
    }

    lamina = EffectiveLamina(**problem3_props)

    print('E1 =   {:.2f}'.format(lamina.E1))
    print('E2 =   {:.2f}'.format(lamina.E2))
    print('v12 =  {:.2f}'.format(lamina.v12))
    print('Gf =   {:.2f}'.format(lamina.Gf))
    print('Gm =   {:.2f}'.format(lamina.Gm))
    print('G12 =  {:.2f}'.format(lamina.G12))
