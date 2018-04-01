#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du contrôleur d'instance, qui sert à construire l'instance pour le programme,
    et fournir un service pour démarrer l'algorithme et pour enregistrer les résultats dans les fichiers

Version: 1.0

Auteur: Peng BI
'''

import time

from controllers.AlgorithmController import AlgorithmController
from controllers.FileController import FileController
from models.antAlgorithm.AntModel import AntModel
from models.antAlgorithm.PheromoneEdge import PheromoneEdge
from models.antAlgorithm.PheromoneNode import PheromoneNode
from models.data.BuildingModel import BuildingModel
from models.data.CareModel import CareModel
from models.instance.InstanceModel import InstanceModel


class InstanceController:
    '''
    Description:
        Cette classe est le contrôleur d'instance de projet

    Attribut:
        instance: (l'objet de la classe InstanceModel) l'instance pour ce projet
        configJson: (l'objet de JSON) les valeurs des paramètres configurées par l'utilisateur
    '''

    def __init__(self, configJson):
        '''
        Description:
            Cette méthode est le constructeur de la classe InstanceController
        '''

        self.instance = InstanceModel() # (l'objet de la classe InstanceModel) l'instance pour ce projet
        self.configJson = configJson # (l'objet de JSON) les valeurs des paramètres configurées par l'utilisateur


    def constructInstance(self):
        '''
        Description:
            Cette méthode est pour construire l'instance de projet

        :return: rien
        '''

        buildingFileName = self.configJson["inputFiles"]["buildingFileName"]  # Le nom du fichier "bâtiment"
        careFileName = self.configJson["inputFiles"]["careFileName"]  # Le nom du fichier "care"
        distanceFileName = self.configJson["inputFiles"]["distanceFileName"]  # Le nom du fichier "distance"

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
            pheromoneNode.rho = self.configJson["pheromone"]["rhoNode"]
            pheromoneNode.tau = self.configJson["pheromone"]["tauNode"]
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
            pheromoneEdge.rho = self.configJson["pheromone"]["rhoEdge"]
            pheromoneEdge.tau = self.configJson["pheromone"]["tauEdge"]
            self.instance.pheromoneEdgeMatrix[i].append(pheromoneEdge)
            j += 1

            if j == len(self.instance.careList) and i != len(self.instance.buildingList) - 1:
                self.instance.distanceMatrix.append([])
                self.instance.pheromoneEdgeMatrix.append([])
                i += 1
                j = 0

        # construire la liste de fourmis
        k = 0
        while(k < self.configJson["antQuantity"]):
            ant = AntModel()
            self.instance.antList.append(ant)
            k += 1

        constructInstanceEndTime = time.time()
        print('Finish constructing the instance, it takes %d s!\n\n' % (constructInstanceEndTime - constructInstanceStartTime))


    def solveProblem(self):
        '''
        Description:
            Cette méthode fournit la service de résoudre le problème

        :return: rien
        '''

        algorithmCtrl = AlgorithmController(self.instance,self.configJson["careEffectRadius"])

        # appeler la méthode "run()" de la classe AlgorithmController pour commencer à résoudre le problème
        algorithmCtrl.run(self.configJson["iterationTimes"])

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
        fileCtrl.writeSolutionFile(self.configJson["outputFiles"]["solutionFileName"], bestSolution, self.instance)
        # écrire les quantités des meiileures solutions et les quantités moyennes des solutions de chaque itération
        # dans le fichier de qualité
        fileCtrl.writeQualityFile(self.configJson["outputFiles"]["qualityFileName"], bestQualityOfSolutionForEachIterationList,
                                  averageQualityOfSolutionForEachIterationList,distanceTotalOfBestSolutionForEachIterationList,
                                  populationAllocatedOfBestSolutionForEachIterationList,
                                  buildingAllocatedOfBestSolutionForEachIterationList)