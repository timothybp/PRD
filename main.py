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

    instanceCtrl = InstanceController(configJson)
    # Appeler la méthode "constructInstance()" pour construire l'instance de programme
    instanceCtrl.constructInstance()

    print('Start to solve the problem...')
    solveProblemeStartTime = time.time()
    # Appeler la méthode "solveProblem()" de la classe InstanceController pour demander la service de résolution de problème
    instanceCtrl.solveProblem()
    solveProblemeEndTime = time.time()
    print('Finish solving the problem, it takes %d s!\n\n' % (solveProblemeEndTime - solveProblemeStartTime))

    programEndTime = time.time()
    print('Finish executing program, it takes %d s!' % (programEndTime - programStartTime))