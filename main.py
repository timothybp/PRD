from controllers.FileController import FileController
from controllers.AlgorithmController import AlgorithmController
from models.ant.AntModel import AntModel

# C'est l'entrée du programme
if __name__ == '__main__':

    nbAnts = 1  # Le nombre de fourmis est 1
    i=0
    while i < nbAnts:
        ant = AntModel()
        antList = []
        antList.append(ant)
        i += 1

    nbIteration = 5 # Le nombre de l'itération est 5
    fc = FileController()
    fc.readFile()

    rayon = 3000    # Le rayon initial est 3000m
    ac = AlgorithmController(fc)
    bestSolution = ac.allocateBuilding(nbIteration, antList, rayon)

    fc.writeFile(bestSolution)

