import numpy as np

class Node:
    def __init__(self, label):
        self.label = label
        self.p = None
        self.q = None
    def pointers(self, p, q):
        self.p = p
        self.q = q
    def __repr__(self) -> str:
        return self.label + '\np: ' + self.p.label + '\nq: ' + self.q.label

def simulacao(players, node0, p, q):
    currentNode = node0
    print(currentNode.label)
    while currentNode.label != 'A Wins' and currentNode.label != 'B Wins':
        result = np.random.choice(players, 1, p=[p,q])[0]
        if(result == 'P'):
            currentNode = currentNode.p            
        else: currentNode = currentNode.q
        print(currentNode.label)

def main(p, q):
    players = ['P','Q']
    labels = ['0-0',
               '15-Love','Love-15',
               '30-Love','15-15','Love-30',
               '40-Love','30-15','15-30','Love-40',
               '40-15','Deuce','15-40',
               'A Wins','Adv. A','Adv. B', 'B Wins']
    grafo = []
    for i in range(0,17):
        grafo.append(Node(labels[i]))
    
    grafo[0].pointers(grafo[1],grafo[2])
    grafo[1].pointers(grafo[3],grafo[4])
    grafo[2].pointers(grafo[4],grafo[5])
    grafo[3].pointers(grafo[6],grafo[7])
    grafo[4].pointers(grafo[7],grafo[8])
    grafo[5].pointers(grafo[8],grafo[9])
    grafo[6].pointers(grafo[13],grafo[10])
    grafo[7].pointers(grafo[10],grafo[11])
    grafo[8].pointers(grafo[11],grafo[12])
    grafo[9].pointers(grafo[12],grafo[16])
    grafo[10].pointers(grafo[13],grafo[14])
    grafo[11].pointers(grafo[14],grafo[15])
    grafo[12].pointers(grafo[15],grafo[16])
    grafo[14].pointers(grafo[13],grafo[11])
    grafo[15].pointers(grafo[11],grafo[16])

    simulacao(players, grafo[0], p, q)

main(0.9, 0.1)