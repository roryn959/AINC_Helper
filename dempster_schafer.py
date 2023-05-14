from itertools import chain, combinations


class BPA:
    def __init__(self, omega):
        self.omega = omega
        self.initialise_masses()

    def setMass(self, set, value):
        self.mass[set] = value

    def initialise_masses(self):
        self.mass = {}
        for set in self.powerset():
            self.mass[set] = 0

    def powerset(self):
        return list(chain.from_iterable(
            combinations(self.omega, r) for r in range(len(self.omega)+1)
        ))

    def subset(self, set1, set2):
        # is set1 a subset of set2?
        for item in set1:
            if item not in set2:
                return False
        return True

    def belief(self, A):
        total = 0
        for B in self.powerset():
            if self.subset(B, A):
                total += self.mass[B]
        return total

    def complement(self, A):
        # This is bad but i have to use tuples for dictionary
        for set in self.powerset():
            complement = True
            for item in self.omega:
                if not(item in A and item not in set) and not(item not in A and item in set):
                    complement = False
                    break
            if complement:
                return set
        raise Exception('Could not find complement of ' + str(A))

    def plausibility(self, A):
        Ac = self.complement(A)
        return 1 - self.belief(Ac)

    def __repr__(self):
        s = ''
        s += 'Omega: ' + str(self.omega) + '\n'
        for set in self.powerset():
            s += str(set)
            s += ', mass: '
            s += str(round(self.mass[set], 3))
            s += ', interval: '
            s += str([round(self.belief(set), 3), round(self.plausibility(set), 3)])
            s += '\n'
        return s


def combine(m1, m2):
    mc = BPA(
        m1.omega
    )

    for A in m1.powerset():
        for B in m2.powerset():
            C = []
            for item in A:
                if item in B:
                    C.append(item)
            C = tuple(C)
            mc.mass[C] += m1.mass[A] * m2.mass[B]

    return mc

def combine_normalised(m1, m2):
    mc = BPA(
        m1.omega
    )

    norm_factor = 0
    for A in m1.powerset():
        for B in m2.powerset():
            # check for empty intersection
            C = []
            for item in A:
                if item in B:
                    C.append(item)
            if len(C) == 0:
                norm_factor += m1.mass[A] * m2.mass[B]

    if norm_factor == 1:
        mc.setMass(mc.omega, 1)
        return mc

    print(norm_factor)

    for A in m1.powerset():
        for B in m2.powerset():
            C = []
            for item in A:
                if item in B:
                    C.append(item)
            C = tuple(C)
            mc.mass[C] += (m1.mass[A] * m2.mass[B]) / (1 - norm_factor)

    mc.setMass((), 0)

    return mc


if __name__ == '__main__':
    omega = (
        'a',
        'b'
    )

    m1 = BPA(
        omega
    )
    m1.setMass(('a',), 0.6)
    m1.setMass(omega, 0.4)

    m2 = BPA(
        omega
    )
    m2.setMass(('b',), 0.6)
    m2.setMass(omega, 0.4)

    mc = combine_normalised(m1, m2)
    print('M1')
    print(m1)
    print('M2')
    print(m2)
    print('MC')
    print(mc)
