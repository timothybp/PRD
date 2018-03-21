import time
from controllers.InstanceController import InstanceController
from controllers.FileController import FileController

# C'est l'entrée du programme
if __name__ == '__main__':
    programStartTime = time.time()
    print('Programme Start...')

    antQuantity = 20
    iterationTimes = 50
    careEffectRadius = 3000

    buildingFileName = 'files/Rq22_51760B_TriCrOID_TriNSACr4.txt'
    careFileName = 'files/Rq33_187CareMoveID188.txt'
    distanceFileName = 'files/LOD9679120_IdNet_NSACr3.txt'


    instanceCtrl = InstanceController()
    instanceCtrl.constructInstance(antQuantity, buildingFileName,careFileName, distanceFileName)

    print('Start to solve the problem...')
    solutionFileName = 'files/bestSolution.txt'
    solveProblemeStartTime = time.time()
    instanceCtrl.solveProblem(iterationTimes, careEffectRadius, solutionFileName)
    solveProblemeEndTime = time.time()
    print('Finish solving the problem, it takes %d s!\n\n' % (solveProblemeEndTime - solveProblemeStartTime))

    programEndTime = time.time()
    print('Finish executing program, it takes %d s!' % (programEndTime - programStartTime))