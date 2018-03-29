#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du test de la performance d'affectation de bâtiment avec l'outil "profile"

Version: 1.0

Auteur: Peng BI
'''

import copy

from models.antAlgorithm.AntModel import AntModel
from models.antAlgorithm.PheromoneEdge import PheromoneEdge
from models.antAlgorithm.PheromoneNode import PheromoneNode
from models.antAlgorithm.SolutionModel import SolutionModel
from models.data.BuildingModel import BuildingModel
from models.data.CareModel import CareModel
from models.instance.InstanceModel import InstanceModel
from tests.PerformanceTest.ProfilerAlgorithmController import ProfilerAlgorithmController


class TestProfilerForAllocateBuilding:
    '''
    Description:
        Cette classe est pour tester l'affectation des bâtiments en utilisant l'outil "Profile"

    Attribut: rien
    '''

    def build_instance(self):
        '''
        Desciption:
            Cette méthode est pour construire une instance pour les méthodes de test

        :return: instance: (l'objet de la classe InstanceModel) une instance
        '''

        instance = InstanceModel()
        # la matrice de distance
        instance.distanceMatrix = [[10, 20, 30, 15, 5, 20, 30],
                                   [30, 20, 15, 20, 15, 10, 5],
                                   [20, 30, 10, 25, 5, 20, 10],
                                   [40, 10, 5, 30, 25, 15, 10],
                                   [30, 20, 30, 5, 10, 15, 20]]

        # le nombre de sans-abris dans chaque bâtiment
        population = [9, 5, 16, 27, 30]
        # construire les bâtiments
        i = 0
        while i < 5:
            building = BuildingModel()
            # les identifiants de bâtiment sont [0,1,2,3,4]
            building.idBuilding = i
            building.population = population[i]
            instance.buildingList.append(building)
            i += 1

        # la capacité de chaque care
        capacity = [8, 15, 6, 34, 13, 10, 18]
        # construire les cares
        j = 0
        while j < 7:
            care = CareModel()
            care.idCare = j
            # les identifiants de care sont [0,1,2,3,4,5,6]
            care.capacity = capacity[j]
            instance.careList.append(care)
            j += 1


        # construire les phéromones déposées sur les nœuds de bâtiment
        i = 0
        while i < len(instance.buildingList):
            pheromoneNode = PheromoneNode()
            pheromoneNode.eta = population[i]
            pheromoneNode.rho = 0.000001
            pheromoneNode.tau = 0.8
            instance.pheromoneNodeList.append(pheromoneNode)
            i += 1

        # construire les phéromones déposées sur les arcs entre les bâtiments et les cares
        i = 0
        while i < len(instance.buildingList):
            j = 0
            while j < len(instance.careList):
                pheromoneEdge = PheromoneEdge()
                pheromoneEdge.eta = 1 / instance.distanceMatrix[i][j]
                pheromoneEdge.rho = 0.1
                pheromoneEdge.tau = 0.9
                instance.pheromoneEdgeMatrix[i].append(pheromoneEdge)
                j += 1
            if i != len(instance.buildingList) - 1:
                instance.pheromoneEdgeMatrix.append([])
            i += 1

        # construire les fourmis
        instance.antList = [AntModel(), AntModel(), AntModel(), AntModel(), AntModel()]

        return instance

    def test_allocateBuilding(self):
        '''
        Description:
            Cette méthode est pour tester la fonction d'affectation de bâtiments

        :return: rien
        '''

        instance = self.build_instance()
        solution = SolutionModel()
        pac = ProfilerAlgorithmController(instance, 3000)
        distanceSortedBuildingIndexMatrix = pac.sortBuildingIndexForEachCareInDistanceMatrix()
        ant = AntModel()

        # initialiser la liste de solution
        solution.solutionArray = [-1, -1, -1, -1, -1, -1, -1]
        solutionForOneIterationList = []
        qualityOfSolutionForOneIterationList = []
        copyDistanceSortedBuildingIndexMatrix = copy.deepcopy(distanceSortedBuildingIndexMatrix)
        pac.allocateBuilding(ant, copyDistanceSortedBuildingIndexMatrix, solutionForOneIterationList,
                            qualityOfSolutionForOneIterationList)

if __name__ == '__main__':
    profilerAllocateBuilding = TestProfilerForAllocateBuilding()
    profilerAllocateBuilding.test_allocateBuilding()