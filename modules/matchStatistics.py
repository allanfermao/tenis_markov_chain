import csv
import random
import modules.log as statisticsLog
import statistics

#Le o dataset e retorna como uma lista de objetos(dicionarios)
def readDataset(path):
    lines = []
    matches = 0
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for obj in reader:
            if int(obj['Partida']) > matches:
                matches = int(obj['Partida'])
            lines.append(obj)

    return lines, matches

#Gera as estatisticas a partir do dataset informado
def generateStatistics(datasetPath, randomStatistics = False, randomChoices=10):
    datasetLines, matchesCount = readDataset(datasetPath)
    logName = "results/match_random_" + str(randomChoices) + "_statistics.csv" if randomStatistics else "results/match_statistics.csv"
    statisticsLog.initLog(logName, ['Partida', 'Vitorias A', 'Vitorias B', 'Sets de A', 'Sets de B', 'Games de A', 'Games de B', 'Vitorias A (%)', 'Vitorias B (%)', 'Sets de A (%)', 'Sets de B (%)', 'Games de A (%)', 'Games de B (%)', 'Media de Sets', 'Desv padrao de Sets', 'Media de Games/Set', 'Desvio padrao de Games', 'Media de Pontos/Game', 'Desvio padrao de pontos'])

    #Para cada partida (1 ou 2), faz as analises
    for i in range(1, matchesCount + 1):
        #Salva apenas as linhas da partida i
        matchLines = [ datasetLines[x] for x in range(len(datasetLines)) if int(datasetLines[x]['Partida']) == i ]

        if(randomStatistics):
            #Seleciona aleatoriamente as 10 simulacoes que serão utilizadas
            chosenSimulations = [x for x in range(1, 31)]
            random.shuffle(chosenSimulations)
            chosenSimulations = chosenSimulations[:randomChoices]
            chosenSimulations.sort()
            newMatchLines = []
            
            for i in range(len(chosenSimulations)):
                for line in matchLines:
                    if int(line['Simulacao']) == chosenSimulations[i]:
                        line['Simulacao'] = i + 1
                        newMatchLines.append(line)

            matchLines = newMatchLines

        #Valores que serao inseridos na linha da partida correspondente
        winA = 0
        winB = 0
        setsA = 0
        setsB = 0
        gamesA = 0
        gamesB = 0
        meanSets = 0
        stdDevSets = 0
        meanGames = 0
        stdDevGames = 0
        meanPoints = 0
        stdDevPoints = 0

        #Valores auxiliares que mudam de acordo com as linhas lidas
        currentSimulation = 1
        currentSet = 1
        currentSetsA = 0
        currentSetsB = 0
        currentGamesA = 0
        currentGamesB = 0
        gamesList = []
        setsList = []
        pointsList = []

        #A logica para fazer o calculo estatistico é:
        # O programa le linha por linha de uma partida X,
        # se o valor do set na linha mudou, significa que o set foi "fechado", entao calcula o vencedor
        # se o valor da simulação mudou, singifica que a simulação acabou, então calcula o vencedor
        # alem disso, em cada linha calcula as informações como a quantidade de pontos marcados e os games
        for line in matchLines:
            #Se acabou as linhas referentes ao set, fecha o vencedor do set
            if int(line['Set']) != currentSet:
                if currentGamesA > currentGamesB:
                    currentSetsA += 1
                else:
                    currentSetsB += 1
                
                gamesA += currentGamesA
                gamesB += currentGamesB
                gamesList.append(currentGamesA + currentGamesB)

                currentGamesA = 0
                currentGamesB = 0

                currentSet = int(line['Set'])

            #Se cabou as linhas referentes à simulação, fecha o vencedor da simulação
            if int(line['Simulacao']) != currentSimulation:
                if currentSetsA > currentSetsB:
                    winA += 1
                else:
                    winB += 1

                setsA += currentSetsA
                setsB += currentSetsB
                setsList.append(currentSetsA + currentSetsB)

                currentSetsA = 0
                currentSetsB = 0

                currentSimulation = int(line['Simulacao'])
                
            if line['Vencedor'] == 'A':
                currentGamesA += 1
            else:
                currentGamesB += 1

            pointsList.append(len(line['Pontos'].split(' ')))

            if line == matchLines[len(matchLines) - 1]:
                if currentGamesA > currentGamesB:
                    currentSetsA += 1
                else:
                    currentSetsB += 1
                
                gamesA += currentGamesA
                gamesB += currentGamesB
                gamesList.append(currentGamesA + currentGamesB)

                if currentSetsA > currentSetsB:
                    winA += 1
                else:
                    winB += 1

                setsA += currentSetsA
                setsB += currentSetsB
                setsList.append(currentSetsA + currentSetsB)

        #Calcula as medias e desvios padrão
        meanSets = statistics.mean(setsList)
        stdDevSets = statistics.stdev(setsList)

        meanGames = statistics.mean(gamesList)
        stdDevGames = statistics.stdev(gamesList)

        meanPoints = statistics.mean(pointsList)
        stdDevPoints = statistics.stdev(pointsList)

        #Escreve no arquivo de log as informações da linha da partida
        statisticsLog.setLogData('Partida', i)
        statisticsLog.setLogData('Vitorias A', winA)
        statisticsLog.setLogData('Vitorias B', winB)
        statisticsLog.setLogData('Sets de A', setsA)
        statisticsLog.setLogData('Sets de B', setsB)
        statisticsLog.setLogData('Games de A', gamesA)
        statisticsLog.setLogData('Games de B', gamesB)
        statisticsLog.setLogData('Vitorias A (%)', (winA/(winA + winB))*100)
        statisticsLog.setLogData('Vitorias B (%)', (winB/(winA + winB))*100)
        statisticsLog.setLogData('Sets de A (%)', (setsA/(setsA + setsB))*100)
        statisticsLog.setLogData('Sets de B (%)', (setsB/(setsA + setsB))*100)
        statisticsLog.setLogData('Games de A (%)', (gamesA/(gamesA + gamesB))*100)
        statisticsLog.setLogData('Games de B (%)', (gamesB/(gamesA + gamesB))*100)
        statisticsLog.setLogData('Media de Sets', meanSets)
        statisticsLog.setLogData('Desv padrao de Sets', stdDevSets)
        statisticsLog.setLogData('Media de Games/Set', meanGames)
        statisticsLog.setLogData('Desvio padrao de Games', stdDevGames)
        statisticsLog.setLogData('Media de Pontos/Game', meanPoints)
        statisticsLog.setLogData('Desvio padrao de pontos', stdDevPoints)
        statisticsLog.commitData()