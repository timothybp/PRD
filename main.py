#-*-coding:utf-8-*-

import time
from controllers.InstanceController import InstanceController


# Description: C'est l'entrée de programme
if __name__ == '__main__':
    programStartTime = time.time()
    print('Programme Start...')

    antQuantity = 30 # Le nombre de fourmis est de 50
    iterationTimes = 500  # La fois d'itération est de 300
    careEffectRadius = 3000 # Le rayon d'effect initial de chaque care est de 3000m

    buildingFileName = 'files/Rq22_51760B_TriCrOID_TriNSACr4.txt' # Le nom du fichier "bâtiment"
    careFileName = 'files/Rq33_187CareMoveID188.txt'    # Le nom du fichier "care"
    distanceFileName = 'files/LOD9679120_IdNet_NSACr3.txt'  # Le nom du fichier "distance"

    instanceCtrl = InstanceController()
    # Appeler la méthode "constructInstance()" pour construire l'instance de programme
    instanceCtrl.constructInstance(antQuantity, buildingFileName,careFileName, distanceFileName)

    print('Start to solve the problem...')
    solutionFileName = 'files/bestSolution.txt' # Le nom du fichier qui stocke la meilleur solution à la fin d'exécution
    qualityFileName = 'files/quality.txt'  # Le nom du fichier qui stocke les qualités de meilleures solutions et les
                                             #  qualités moyenne de solutions de chaque itération à la fin d'exécution
    solveProblemeStartTime = time.time()
    # Appeler la méthode "solveProblem()" de la classe InstanceController pour demander la service de résolution de problème
    instanceCtrl.solveProblem(iterationTimes, careEffectRadius, solutionFileName,qualityFileName)
    solveProblemeEndTime = time.time()
    print('Finish solving the problem, it takes %d s!\n\n' % (solveProblemeEndTime - solveProblemeStartTime))

    programEndTime = time.time()
    print('Finish executing program, it takes %d s!' % (programEndTime - programStartTime))