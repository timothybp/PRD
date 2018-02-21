from models.data.BuildingModel import BuildingModel
from models.data.CareModel import CareModel
from models.pheromone.PheromoneNode import PheromoneNode
from models.pheromone.PheromoneEdge import PheromoneEdge

# Cette classe est pour contrôler les fichier(la lecture et l'écriture)
class FileController:

    def __init__(self):
        self.buildingList = []  # La liste de bâtiments
        self.careList = []  # La liste de cares
        self.distanceMatrix = [[]]  # La matrice de distances entre chaque bâtiment et chaque care
        self.pheromoneNodeList = [] # La liste de phéromone sur le nœud de bâtiment
        self.pheromoneEdgeMatrix = [[]] # La matrice de phéromone sur l'arc entre le batiments et le case

    # Cette méthode est pour lire les 3 fichiers : bâtiments, cares, distances
    def readFile(self):
        # Lire le fichier de bâtiments et construire la liste de bâtiment et la liste de phéromone sur le nœud de bâtiment
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
        # Lire le fichier de cares et construire la liste de care
        careCounter = 0
        with open('files/Rq33_187CareMoveID188.txt','rt') as cares:
            for careLine in cares:
                if careCounter != 0:
                    care = CareModel()
                    care.idCare = int(careLine.split('\t')[0])
                    care.capacity = int(careLine.split('\t')[3])
                    self.careList.append(care)
                careCounter += 1
        # Lire le fichier de distances et construire la matrice de distances et la matrice de phéromone sur l'arc entre le batiments et le case
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

    # Cette méthode est pour écrire la meilleure solution dans le fichier de sortie
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