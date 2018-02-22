from controllers.FileController import FileController
from controllers.AlgorithmController import AlgorithmController
from models.ant.AntModel import AntModel
import time
# C'est l'entrée du programme
if __name__ == '__main__':
    startTime = time.time()
    nbAnts = 10  # Le nombre de fourmis est 1
    i=0
    antList = []
    while i < nbAnts:
        ant = AntModel()
        antList.append(ant)
        i += 1

    nbIteration = 10 # Le nombre de l'itération est 5
    fc = FileController()
    fc.readFile()

    rayon = 3000    # Le rayon initial est 3000m
    ac = AlgorithmController(fc)
    bestSolution = ac.allocateBuilding(nbIteration, antList, rayon)

    fc.writeFile(bestSolution)
    endTime = time.time()
    print(endTime - startTime)

