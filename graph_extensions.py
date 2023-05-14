from itertools import chain, combinations


class Graph:
    def __init__(self):
        self.__nodes = []
        self.__edges = []
        self.__extensions = []
        self.__admissibles = []
        self.__completes = []
        self.__groundeds = []
        self.__preferreds = []
        self.__stables = []

    def addNode(self, node):
        self.__nodes.append(node)

    def addEdge(self, node1, node2):
        self.__edges.append((node1, node2))

    def powerset(self):
        return list(chain.from_iterable(
            combinations(self.__nodes, r) for r in range(len(self.__nodes)+1)
        ))

    def attacks(self, attacker, victim):
        for edge in self.__edges:
            if edge == (attacker, victim):
                return True
        return False

    def defends(self, defenders, victim):
        for arg in self.__nodes:
            if self.attacks(arg, victim):
                defended = False
                for defender in defenders:
                    if self.attacks(defender, arg):
                        defended = True
                        break
                if not defended:
                    return False
        return True

    def defended(self, argset):
        defended = []
        for arg in self.__nodes:
            if self.defends(argset, arg):
                defended.append(arg)
        return defended

    def conflictFree(self, argset):
        for arg1 in argset:
            for arg2 in argset:
                if self.attacks(arg1, arg2):
                    return False
        return True

    def admissible(self, argset):
        if not self.conflictFree(argset):
            return False
        defended = self.defended(argset)
        for arg in argset:
            if arg not in defended:
                return False
        return True

    def complete(self, extension):
        defended = self.defended(extension)
        for arg in defended:
            if arg not in extension:
                return False
        return True

    def subset(self, argset1, argset2):
        if len(argset1) >= len(argset2):
            return False
        for elem in argset1:
            if elem not in argset2:
                return False
        return True

    def grounded(self, extension):
        for complete in self.__completes:
            if self.subset(complete, extension):
                return False
        return True

    def preferred(self, extension):
        for complete in self.__completes:
            if self.subset(extension, complete):
                return False
        return True

    def stable(self, extension):
        for node in self.__nodes:
            if node not in extension:
                attacked = False
                for attacker in extension:
                    if self.attacks(attacker, node):
                        attacked = True
                        break
                if not attacked:
                    return False
        return True

    def generateExtensions(self):
        self.__extensions = self.powerset()

        self.__admissibles = []
        for extension in self.__extensions:
            if self.admissible(extension):
                self.__admissibles.append(extension)

        self.__completes = []
        for extension in self.__admissibles:
            if self.complete(extension):
                self.__completes.append(extension)

        self.__groundeds = []
        for extension in self.__completes:
            if self.grounded(extension):
                self.__groundeds.append(extension)

        self.__preferreds = []
        for extension in self.__completes:
            if self.preferred(extension):
                self.__preferreds.append(extension)

        self.__stables = []
        for extension in self.__preferreds:
            if self.stable(extension):
                self.__stables.append(extension)

    def __repr__(self):
        s = ''
        s += 'Admissibles: '
        s += str(self.__admissibles)
        s += '\n'
        s += 'Completes: '
        s += str(self.__completes)
        s += '\n'
        s += 'Groundeds: '
        s += str(self.__groundeds)
        s += '\n'
        s += 'Preferreds: '
        s += str(self.__preferreds)
        s += '\n'
        s += 'Stables: '
        s += str(self.__stables)
        return s


if __name__ == '__main__':
    graph = Graph()
    graph.addNode('1')
    graph.addNode('2')
    graph.addNode('3')
    graph.addNode('4')
    graph.addNode('5')
    graph.addEdge('1', '2')
    graph.addEdge('3', '2')
    graph.addEdge('3', '4')
    graph.addEdge('4', '3')
    graph.addEdge('4', '5')
    graph.addEdge('5', '5')
    graph.generateExtensions()
    print(graph)
