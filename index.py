from lib2to3.pgen2.pgen import generate_grammar
import numpy as np
import modules.log as log
import modules.matchStatistics as matchStatistics 

FIRST_MATCH = {
    'p': 0.7,
    'q': 0.3,
    'n': 30
}

SECOND_MATCH = {
    'p': 0.5,
    'q': 0.5,
    'n': 30
}

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
    lastNode = node0
    log.setLogData("Pontos", log.getLogData("Pontos") + currentNode.label + " ")
    while currentNode.label != 'A Wins' and currentNode.label != 'B Wins':
        result = np.random.choice(players, 1, p=[p,q])[0]
        if(result == 'P'):
            lastNode = currentNode.label
            currentNode = currentNode.p            
        else: 
            lastNode = currentNode.label
            currentNode = currentNode.q
        log.setLogData("Pontos", log.getLogData("Pontos") + currentNode.label + " ")

    log.setLogData("Pontos", log.getLogData("Pontos")[:-1])
    log.setLogData("Vencedor", currentNode.label.split(' ')[0])
    log.commitData()
    log.resetLogData("Vencedor")
    log.resetLogData("Pontos")
    return result

def setVerify(games):    
    if 7 in games.values():
        player = 'A' if games['A'] == 7 else 'B'
        games['A'] = 0
        games['B'] = 0
        return player
    if 6 in games.values() and abs(games['A'] - games['B']) >= 2:
        player = 'A' if games['A'] == 6 else 'B'
        games['A'] = 0
        games['B'] = 0
        
        return player
    return 0   

def matchVerify(sets):
    if 2 in sets.values():
        player = 'A' if sets['A'] == 2 else 'B'
        sets['A'] = 0
        sets['B'] = 0
        return player
    else: return 0

def main(p, q, n_simm):
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

    games = {'A': 0, 'B': 0}
    sets = {'A': 0, 'B': 0}
    matches = {'A': 0, 'B': 0}

    for i in range(0, n_simm):
        resultMatch = 0
        log.setLogData("Simulacao", i + 1)
        setsCount = 1
        while resultMatch == 0: # enquanto a partida não termina
            resultSet = 0
            log.setLogData("Set", setsCount)
            gamesCount = 1
            while resultSet == 0: # enquanto o set não termina, continua executando games
                log.setLogData("Game", gamesCount)
                if simulacao(players, grafo[0], p, q) == 'P':
                    games['A'] += 1
                else: games['B'] += 1
                resultSet = setVerify(games)
                gamesCount += 1
            setsCount += 1
            sets[resultSet] += 1
            resultMatch = matchVerify(sets)
        
        matches[resultMatch] += 1
        

log.initLog("results/match_dataset.csv", ['Partida', 'Simulacao', 'Set', 'Game', 'Vencedor', 'Pontos'])

log.setLogData("Partida", '1')
main(FIRST_MATCH['p'], FIRST_MATCH['q'], FIRST_MATCH['n'])

log.setLogData("Partida", '2')
main(SECOND_MATCH['p'], SECOND_MATCH['q'], SECOND_MATCH['n'])

log.closeLog()

matchStatistics.generateStatistics("results/match_dataset.csv")