#-*-coding:utf-8-*-

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
    '''
    Description: cette classe est la controleur de instance de projet
    Attribut:
        instance: (l'objet de la classe InstanceModel) l'instance pour ce projet
    '''

    def __init__(self):
        '''
        Description: cette méthode est le constructeur de la classe InstanceController
        '''

        self.instance = InstanceModel() # (l'objet de la classe InstanceModel) l'instance pour ce projet


    def constructInstance(self,antQuantity, buildingFileName,careFileName, distanceFileName):
        '''
        Description: cette classe est pour construire l'instance de projet
        :param antQuantity: (int) le nombre de fourmis
        :param buildingFileName: (String) le nom du fichier de bâtiment
        :param careFileName: (String) le nom du fichier de care
        :param distanceFileName: (String) le nom du fichier de distance
        :return: rien
        '''

        fileCtrl = FileController()
        print('Start to read files...')
        readingFilesStartTime = time.time()

        # obtenir les listes de contenue de trois fichiers
        buildingFileContent = fileCtrl.readBuildingFile(buildingFileName)
        careFileContent = fileCtrl.readCareFile(careFileName)
        distanceFileContent = fileCtrl.readDistanceFile(distanceFileName)
        readingFilesEndTime = time.time()
        print('Finish reading all files, it takes %d s!\n\n' % (readingFilesEndTime - readingFilesStartTime))

        print('Start to construct the instance...')
        constructInstanceStartTime = time.time()

        # construire la liste de bâtiments et la liste de phéromone déposée sur les nœuds de bâtiment
        for buildingLine in buildingFileContent:
            building = BuildingModel()
            # retirer la première et la quatrième colonne dans chaque ligne de fichier bâtiment
            building.idBuilding = int(buildingLine.split('\t')[0])
            building.population = float(buildingLine.split('\t')[3])
            self.instance.buildingList.append(building)

            pheromoneNode = PheromoneNode()
            # pour la combinaison de F(x) et G(x), la valeur d'eta de phéromone sur les nœuds est égale à la population de bâtiments
            # pour la combinaison de F(x) et H(x), la valeur d'eta de phéromone sur les nœuds est égale à (1 / la population de bâtiments)
            pheromoneNode.eta = float(buildingLine.split('\t')[3])
            pheromoneNode.rho = 0.000001
            pheromoneNode.tau = 0.8
            self.instance.pheromoneNodeList.append(pheromoneNode)

        # construire la liste de care
        for careLine in careFileContent:
            care = CareModel()
            # retirer la première et la quatrième colonne dans chaque ligne de fichier care
            care.idCare = int(careLine.split('\t')[0])
            care.capacity = int(careLine.split('\t')[3])
            self.instance.careList.append(care)

        # construire la matrice de distance et la matrice de phéromone déposée sur les arcs entre le bâtiment et le care
        i = 0
        j = 0
        for distanceLine in distanceFileContent:
            pheromoneEdge = PheromoneEdge()
            # retirer la troisième colonne dans chaque ligne de fichier distance qui est la valeur de distance
            self.instance.distanceMatrix[i].append(float(distanceLine.split('\t')[2]))

            # si la distance n'est pas 0, la valeur d'eta de phéromone sur les arcs est égale à (1 / la distance)
            if float(distanceLine.split('\t')[2]) != 0:
                pheromoneEdge.eta = 1 / float(distanceLine.split('\t')[2])
            # sinon, la valeur d'eta de phéromone sur les arcs est égale à 0
            else:
                pheromoneEdge.eta = 0
            pheromoneEdge.rho = 0.1
            pheromoneEdge.tau = 0.9
            self.instance.pheromoneEdgeMatrix[i].append(pheromoneEdge)
            j += 1

            if j == len(self.instance.careList) and i != len(self.instance.buildingList) - 1:
                self.instance.distanceMatrix.append([])
                self.instance.pheromoneEdgeMatrix.append([])
                i += 1
                j = 0

        # construire la liste de fourmis
        k = 0
        while(k < antQuantity):
            ant = AntModel()
            self.instance.antList.append(ant)
            k += 1

        constructInstanceEndTime = time.time()
        print('Finish constructing the instance, it takes %d s!\n\n' % (constructInstanceEndTime - constructInstanceStartTime))


    def solveProblem(self,iterationTimes, careEffectRadius, solutionFileName, qualityFileName):
        '''
        Description: cette méthode fournit la service de résoudre le problème
        :param iterationTimes: (int) la fois d'itération
        :param careEffectRadius: (int) le rayon d'attraction initial pour les cares
        :param solutionFileName: le nom du fichier de solution qui enregistre la meilleure solution à la fin
        :return: rien
        '''

        algorithmCtrl = AlgorithmController(self.instance,careEffectRadius)

        # appeler la méthode "run()" de la classe AlgorithmController pour commencer à résoudre le problème
        algorithmCtrl.run(iterationTimes)

        # obtenir la meilleure solution
        bestSolution = algorithmCtrl.bestSolution
        # obtenir la liste de qualités de meilleure solution de chaque itération
        bestQualityOfSolutionForEachIterationList = algorithmCtrl.bestQualityOfSolutionForEachIterationList
        # obtenir la liste de qualités moyenne des soltuons de chaque itération
        averageQualityOfSolutionForEachIterationList = algorithmCtrl.averageQualityOfSolutionForEachIterationList
        # obtenir la liste de distance totale de la meilleure solution de chaque itération
        distanceTotalOfBestSolutionForEachIterationList = algorithmCtrl.distanceTotalOfBestSolutionForEachIterationList
        # obtenir la liste de sans-abris totaux hébergés de la meilleure solution de chaque itération
        populationAllocatedOfBestSolutionForEachIterationList = algorithmCtrl.populationAllocatedOfBestSolutionForEachIterationList
        # obtenir la liste de nombre de bâtiments affectés de la meilleure solution de chaque itération
        buildingAllocatedOfBestSolutionForEachIterationList = algorithmCtrl.buildingAllocatedOfBestSolutionForEachIterationList

        fileCtrl = FileController()
        # écrire la meilleure solution dans le fichier de solution
        fileCtrl.writeSolutionFile(solutionFileName, bestSolution, self.instance)
        # écrire les quantités des meiileures solutions et les quantités moyennes des solutions de chaque itération
        # dans le fichier de qualité
        fileCtrl.writeQualityFile(qualityFileName, bestQualityOfSolutionForEachIterationList, averageQualityOfSolutionForEachIterationList,
                                  distanceTotalOfBestSolutionForEachIterationList, populationAllocatedOfBestSolutionForEachIterationList,
                                  buildingAllocatedOfBestSolutionForEachIterationList)