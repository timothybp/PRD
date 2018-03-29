#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script qui est l'entrée du programme, l'utilisateur
    peut définir les values de paramètres dans ce script

Version: 1.0

Auteur: Peng BI
'''

import time
from controllers.InstanceController import InstanceController
from controllers.FileController import FileController

# Description: C'est l'entrée de programme
if __name__ == '__main__':
    programStartTime = time.time()
    print('Programme Start...')

    configFileName = 'configuration/configParameters.json'

    # lire les configuration des paramètres pour le problème du fichier "configParameters.json"
    fileCtrl = FileController()
    configJson = fileCtrl.readConfigurationFile(configFileName)
    antQuantity = int(configJson["antQuantity"]) # Le nombre de fourmis est de 50
    iterationTimes = int(configJson["iterationTimes"])  # La fois d'itération est de 1000
    careEffectRadius = int(configJson["careEffectRadius"]) # Le rayon d'effect initial de chaque care est de 3000m

    buildingFileName = configJson["buildingFileName"] # Le nom du fichier "bâtiment"
    careFileName = configJson["careFileName"]   # Le nom du fichier "care"
    distanceFileName = configJson["distanceFileName"]  # Le nom du fichier "distance"

    instanceCtrl = InstanceController()
    # Appeler la méthode "constructInstance()" pour construire l'instance de programme
    instanceCtrl.constructInstance(antQuantity, buildingFileName,careFileName, distanceFileName)

    print('Start to solve the problem...')
    solutionFileName = configJson["solutionFileName"] # Le nom du fichier qui stocke la meilleur solution à la fin d'exécution
    qualityFileName = configJson["qualityFileName"]  # Le nom du fichier qui stocke les qualités de meilleures solutions et les
                                                       #  qualités moyenne de solutions de chaque itération à la fin d'exécution
    solveProblemeStartTime = time.time()
    # Appeler la méthode "solveProblem()" de la classe InstanceController pour demander la service de résolution de problème
    instanceCtrl.solveProblem(iterationTimes, careEffectRadius, solutionFileName,qualityFileName)
    solveProblemeEndTime = time.time()
    print('Finish solving the problem, it takes %d s!\n\n' % (solveProblemeEndTime - solveProblemeStartTime))

    programEndTime = time.time()
    print('Finish executing program, it takes %d s!' % (programEndTime - programStartTime))