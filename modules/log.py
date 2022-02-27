# Modulo log.py
# Funcoes para a manipulacao do arquivo de log que devera ser gerado
# durante a execução de cada simulação de partida, game e set.
# 
# A utilização do módulo é da seguinte forma:
#  - Primeiro deve-se inicializar o arquivo de log passando o nome do arquivo e os cabeçalhos 
# utilizando a função initLog
#  - Para adicionar ou atualizar um valor a um campo do log é usado o setLogData
#  - Por fim, para escrever a linha no arquivo de log deve ser chamado a função commitData

import csv

logFile = None  #Referencia global para o arquivo de log
writer = None   #Referencia para o csvWriter
logData = {}    #Representa a linha atual do log

#Cria o arquivo de log, escreve os headers e inicializa o objeto de log
def initLog(fileName, headers):
    global logFile
    global writer
    global logData

    logFile = open(fileName, 'w+', encoding='UTF8', newline='')

    #Inicializa o csv writer e escreve os headers no arquivo
    writer = csv.DictWriter(logFile, fieldnames=headers)
    writer.writeheader()

    #Inicializa os campos do objeto de log
    logData = {}
    for header in headers:
        logData[header] = ""

#Escreve os dados presentes no objeto logData na proxima linha do arquivo
def commitData():
    global writer
    global logData
    writer.writerow(logData)

#Limpa o valor de um campo do objeto logData
def resetLogData(key):
    global logData
    logData[key] = ""

#Atribui um valor a um campo do objeto logData
def setLogData(key, value):
    global logData
    logData[key] = value

#Retorna o valor de um campo do objeto logData
def getLogData(key):
    return logData[key]