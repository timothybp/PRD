from controllers.FileController import FileController
from controllers.AlgorithmController import AlgorithmController
from models.ant.AntModel import AntModel

if __name__ == '__main__':
    nbAnts = 1
    i=0
    while i < nbAnts:
        ant = AntModel()
        antList = []
        antList.append(ant)
        i += 1

    nbIteration = 5
    fc = FileController()
    fc.readFile()

    rayon = 3000
    ac = AlgorithmController(fc)
    bestSolution = ac.allocateBuilding(nbIteration, antList, rayon)

    fc.writeFile(bestSolution)

