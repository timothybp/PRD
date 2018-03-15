from models.instance.InstanceModel import InstanceModel
from models.data.BuildingModel import BuildingModel
from models.data.CareModel import CareModel
from models.pheromone.PheromoneNode import PheromoneNode
from models.pheromone.PheromoneEdge import PheromoneEdge
from models.ant.AntModel import AntModel
from controllers.AlgorithmController import AlgorithmController
from controllers.FileController import FileController
import time

class InstanceController:

    def __init__(self):
        self.instance = InstanceModel()


    def constructInstance(self,antAmount, buildingFileName,careFileName, distanceFileName):

        fileCtrl = FileController()
        print('Start to read files...')
        readingFilesStartTime = time.time()
        buildingFileContent = fileCtrl.readFile(buildingFileName, 'building')
        careFileContent = fileCtrl.readFile(careFileName, 'care')
        distanceFileContent = fileCtrl.readFile(distanceFileName, 'distance')
        readingFilesEndTime = time.time()
        print('Finish reading all files, it takes %d s!\n\n' % (readingFilesEndTime - readingFilesStartTime))

        print('Start to construct the instance...')
        constructInstanceStartTime = time.time()
        for buildingLine in buildingFileContent:
            building = BuildingModel()
            building.idBuilding = int(buildingLine.split('\t')[0])
            building.population = float(buildingLine.split('\t')[3])
            self.instance.buildingList.append(building)

            pheromoneNode = PheromoneNode()
            pheromoneNode.eta = float(buildingLine.split('\t')[3])
            pheromoneNode.rho = 0.25
            pheromoneNode.tau = 0.5
            self.instance.pheromoneNodeList.append(pheromoneNode)

        for careLine in careFileContent:
            care = CareModel()
            care.idCare = int(careLine.split('\t')[0])
            care.capacity = int(careLine.split('\t')[3])
            self.instance.careList.append(care)

        i = 0
        j = 0
        for distanceLine in distanceFileContent:
            pheromoneEdge = PheromoneEdge()
            self.instance.distanceMatrix[i].append(float(distanceLine.split('\t')[2]))

            if float(distanceLine.split('\t')[2]) != 0:
                pheromoneEdge.eta = 1 / float(distanceLine.split('\t')[2])
            else:
                pheromoneEdge.eta = 0
            pheromoneEdge.rho = 0.5
            pheromoneEdge.tau = 0.5
            self.instance.pheromoneEdgeMatrix[i].append(pheromoneEdge)
            j += 1

            if j == len(self.instance.careList) and i != len(self.instance.buildingList) - 1:
                self.instance.distanceMatrix.append([])
                self.instance.pheromoneEdgeMatrix.append([])
                i += 1
                j = 0

        k = 0
        while(k < antAmount):
            ant = AntModel()
            self.instance.antList.append(ant)
            k += 1

        constructInstanceEndTime = time.time()
        print('Finish constructing the instance, it takes %d s!\n\n' % (constructInstanceEndTime - constructInstanceStartTime))

    def solveProblem(self,iterationTimes, radius, outFileName):
        algorithmCtrl = AlgorithmController(self.instance)
        algorithmCtrl.allocateBuilding(iterationTimes, radius)
        bestSolution = algorithmCtrl.bestSolution
        fileCtrl = FileController()
        fileCtrl.writeFile(outFileName, bestSolution, self.instance)