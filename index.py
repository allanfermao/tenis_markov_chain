from collections import namedtuple
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

class Match:
    def __init__(self):
        self.winner = None
        self.games = {'A': 0, 'B': 0}
        self.sets = {'A': 0, 'B': 0}
        self.scores = [] # vetor de namedtuple (A=x, B=y); o ganhador sempre tem +10 pontos em cada score
    def includeScore(self, score):
        self.scores.append(score)
    def setGames(self, games):
        self.games['A'] += games['A']
        self.games['B'] += games['B']
    def setSets(self, sets):
        self.sets['A'] += sets['A']
        self.sets['B'] += sets['B']
    def __repr__(self) -> str:
        return '\n\t' + self.winner +  '\n\tSets:' + str(self.sets) + '\n\tGames: ' + str(self.games) + '\n\tScores: ' + str(self.scores) + '\n'

def simulacao(players, node0, p, q, match):
    currentNode = node0
    lastNode = node0
    # print(currentNode.label)
    log.setLogData("Pontos", log.getLogData("Pontos") + currentNode.label + " ")
    while currentNode.label != 'A Wins' and currentNode.label != 'B Wins':
        result = np.random.choice(players, 1, p=[p,q])[0]
        if(result == 'P'):
            lastNode = currentNode.label
            currentNode = currentNode.p            
        else: 
            lastNode = currentNode.label
            currentNode = currentNode.q
        # print(currentNode.label)
        log.setLogData("Pontos", log.getLogData("Pontos") + currentNode.label + " ")
    # Score = namedtuple('Score', ['A','B'])
    # aux = currentNode.label.split('-')
    # score = Score(aux[0],aux[1])
    log.setLogData("Pontos", log.getLogData("Pontos")[:-1])
    log.setLogData("Vencedor", currentNode.label.split(' ')[0])
    log.commitData()
    log.resetLogData("Vencedor")
    log.resetLogData("Pontos")
    match.includeScore(lastNode)
    # print()
    return result

def setVerify(games, match):    
    if 7 in games.values():
        player = 'A' if games['A'] == 7 else 'B'
        match.setGames(games)
        games['A'] = 0
        games['B'] = 0
        # print(player + ' Wins Set\n')
        return player
    if 6 in games.values() and abs(games['A'] - games['B']) >= 2:
        player = 'A' if games['A'] == 6 else 'B'
        match.setGames(games)
        games['A'] = 0
        games['B'] = 0
        # print(player + ' Wins Set\n')
        
        return player
    return 0   

def matchVerify(sets, match):
    if 2 in sets.values():
        player = 'A' if sets['A'] == 2 else 'B'
        match.setSets(sets)
        sets['A'] = 0
        sets['B'] = 0
        # print(player + ' Wins Match\n')
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

    matchesStatistics = []

    for i in range(0, n_simm):
        match = Match()
        resultMatch = 0
        log.setLogData("Simulacao", i + 1)
        setsCount = 1
        while resultMatch == 0: # enquanto a partida não termina
            resultSet = 0
            log.setLogData("Set", setsCount)
            gamesCount = 1
            while resultSet == 0: # enquanto o set não termina, continua executando games
                log.setLogData("Game", gamesCount)
                if simulacao(players, grafo[0], p, q, match) == 'P':
                    games['A'] += 1
                else: games['B'] += 1
                resultSet = setVerify(games, match)
                gamesCount += 1
            setsCount += 1
            sets[resultSet] += 1
            resultMatch = matchVerify(sets, match)
        
        matches[resultMatch] += 1
        setattr(match, 'winner', resultMatch)

        matchesStatistics.append(match)

    # print(matchesStatistics)
        

log.initLog("results/match_dataset.csv", ['Partida', 'Simulacao', 'Set', 'Game', 'Vencedor', 'Pontos'])

log.setLogData("Partida", '1')
main(FIRST_MATCH['p'], FIRST_MATCH['q'], FIRST_MATCH['n'])

log.setLogData("Partida", '2')
main(SECOND_MATCH['p'], SECOND_MATCH['q'], SECOND_MATCH['n'])

log.closeLog()

matchStatistics.generateStatistics("results/match_dataset.csv")