from models.data.BuildingModel import BuildingModel
from models.data.CareModel import CareModel
from models.pheromone.PheromoneNode import PheromoneNode
from models.pheromone.PheromoneEdge import PheromoneEdge


class FileController:

    def __init__(self):
        self.buildingList = []
        self.careList = []
        self.distanceMatrix = [[]]
        self.pheromoneNodeList = []
        self.pheromoneEdgeMatrix = [[]]

    def readFile(self):
        buildingCounter = 0
        with open('files/Rq22_51760B_TriCrOID_TriNSACr4.txt','rt') as buildings:
            for buildingLine in buildings:
                if buildingCounter != 0:
                    building = BuildingModel()
                    building.idBuilding = int(buildingLine.split('\t')[0])
                    building.population = float(buildingLine.split('\t')[3])
                    self.buildingList.append(building)
                    pheromoneNode = PheromoneNode()
                    pheromoneNode.eta = float(buildingLine.split('\t')[3])
                    pheromoneNode.rho = 0.25
                    pheromoneNode.tau = 0.5
                    self.pheromoneNodeList.append(pheromoneNode)
                buildingCounter += 1

        careCounter = 0
        with open('files/Rq33_187CareMoveID188.txt','rt') as cares:
            for careLine in cares:
                if careCounter != 0:
                    care = CareModel()
                    care.idCare = int(careLine.split('\t')[0])
                    care.capacity = int(careLine.split('\t')[3])
                    self.careList.append(care)
                careCounter += 1

        distanceCounter = 0
        with open('files/LOD9679120_IdNet_NSACr3.txt','rt') as distances:
            i = 0
            j = 0
            for distanceLine in distances:
                if distanceCounter != 0:
                    pheromoneEdge = PheromoneEdge()
                    self.distanceMatrix[i].append(float(distanceLine.split('\t')[2]))
                    if float(distanceLine.split('\t')[2]) != 0:
                        pheromoneEdge.eta = 1/float(distanceLine.split('\t')[2])
                    else:
                        pheromoneEdge.eta = 0
                    pheromoneEdge.rho = 0.5
                    pheromoneEdge.tau = 0.5
                    self.pheromoneEdgeMatrix[i].append(pheromoneEdge)
                    j += 1
                if j == len(self.careList) and i != len(self.buildingList)-1:
                    self.distanceMatrix.append([])
                    self.pheromoneEdgeMatrix.append([])
                    i += 1
                    j = 0
                distanceCounter += 1
        print("finished reading files")

    def writeFile(self,solution):
        with open('files/result.txt','wt') as result:
            i = 0
            strToWrite = ''
            while i < len(solution):
                if str(solution[i]) != '-1':
                    indexCare = int(solution[i])
                    idCare = str(self.careList[indexCare].idCare)
                else:
                    idCare = str(-1)

                if i != len(solution) - 1:
                    strToWrite += idCare + '\t'
                else:
                    strToWrite += idCare + '\n'
                i += 1
            result.write(strToWrite)

