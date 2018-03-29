#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du test unitaire de la classe "AlgorithmController"

Version: 1.0

Auteur: Peng BI
'''

import copy
import unittest

from controllers.AlgorithmController import AlgorithmController
from models.antAlgorithm.AntModel import AntModel
from models.antAlgorithm.PheromoneEdge import PheromoneEdge
from models.antAlgorithm.PheromoneNode import PheromoneNode
from models.antAlgorithm.SolutionModel import SolutionModel
from models.data.BuildingModel import BuildingModel
from models.data.CareModel import CareModel
from models.instance.InstanceModel import InstanceModel


class TestAlgorithmController(unittest.TestCase):
    '''
    Description:
        Cette classe est pour faire le test unitaire sur la classe "AlgorithmController"

    Attribut; rien
    '''

    def test_mergeSort(self):
        '''
        Desciption:
            Cette méthode est pour tester la méthode "mergeSort()", pour
            vérifier si le tri par fusion fonctionne bien

        :return:rien
        '''

        distanceColumn = [2,56,3,22]    # la liste de distance entre un care et chaque bâtiment
        distanceIndexRow = [0,1,2,3]    # la liste d'indice de bâtiment à trier

        instance = InstanceModel()
        # la matrice de distance
        instance.distanceMatrix = [[2, 4, 5, 3, 1], [56, 29, 3, 43, 11], [3, 54, 67, 13, 4], [22, 51, 78, 32, 45]]
        ac = AlgorithmController(instance,3000)
        distanceColumn, distanceIndexRow = ac.mergeSort(distanceColumn, distanceIndexRow)

        # vérifier si la liste d'indice de bâtiment trier est [0,2,3,1]
        self.assertListEqual(distanceIndexRow, [0,2,3,1])


    def test_sortBuildingIndexForEachCareInDistanceMatrix(self):
        '''
        Desciption:
            Cette méthode est pour tester la méthode "sortBuildingIndexForEachCareInDistanceMatrix()"，
            pour vérifier si on peut obtenir une matrice d'indices de bâtiments bien tirée

        :return:rien
        '''

        instance = InstanceModel()
        # la matrice de distance
        instance.distanceMatrix = [[2,4,5,3,1],[56,29,3,43,11], [3,54,67,13,4], [22,51,78,32,45]]
        # la matrice d'indice de bâtiment attendue
        targetList = [[0,2,3,1],[0,1,3,2],[1,0,2,3],[0,2,3,1],[0,2,1,3]]
        ac = AlgorithmController(instance,3000)

        # vérifier si la matrice triée retournée est égale à la matrice d'indice de bâtiment attendue
        self.assertListEqual(ac.sortBuildingIndexForEachCareInDistanceMatrix(),targetList)


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


    def test_objectiveFunctionF(self):
        '''
        Desciption:
            Cette méthode est pour tester la méthode "objectiveFunctionF()"

        :return: rien
        '''

        # construire une solution
        solution = SolutionModel()
        solution.solutionArray = [4,6,4,2,3]

        instance = self.build_instance()
        ac = AlgorithmController(instance, 3000)

        # vérifier si la valeur retournée de f(x) est 435
        self.assertTrue(ac.objectiveFunctionF(solution) == 435)


    def test_objectiveFunctionG(self):
        '''
        Desciption:
            Cette méthode est pour tester la méthode "objectiveFunctionG()"

        :return: rien
        '''

        solution = SolutionModel()
        solution.solutionArray = (4, 6, 4, 2, 3)

        instance = self.build_instance()
        ac = AlgorithmController(instance, 3000)

        # vérifier si la valeur retournée de f(x) est 87
        self.assertTrue(ac.objectiveFunctionG(solution) == 87)


    def test_objectiveFunctionH(self):
        '''
        Desciption:
            Cette méthode est pour tester la méthode "objectiveFunctionH()"

        :return: rien
        '''

        solution = SolutionModel()
        solution.solutionArray = (4, 6, 4, 2, 3)

        instance = self.build_instance()
        ac = AlgorithmController(instance, 3000)

        # vérifier si la valeur retournée de f(x) est 5
        self.assertTrue(ac.objectiveFunctionH(solution) == 5)


    def test_calculateAverageSolutionQualityForEachIteration(self):
        '''
        Desciption:
            Cette méthode est pour tester la méthode "calculateAverageSolutionQualityForEachIteration()"

        :return: rien
        '''

        # construire une liste de qualité pour les solutions dans une itérations
        qualityOfSolutionForOneIterationList = [0.5, 0.4, 0.6,0.3, 0.2]

        instance = InstanceModel()
        instance.antList = [AntModel(),AntModel(),AntModel(),AntModel(),AntModel()]
        ac = AlgorithmController(instance, 3000)

        # # vérifier si la qualité moyenne retournée est 0.4
        self.assertTrue(ac.calculateAverageSolutionQualityForEachIteration(qualityOfSolutionForOneIterationList) == 0.4)


    def test_chooseCare(self):
        '''
        Desciption:
            Cette méthode est pour tester la méthode "chooseCare()"

        :return: rien
        '''

        instance = self.build_instance()
        solution = SolutionModel()

        # sélectionner le bâtiments dont l'indice est 4
        buidlingToAllocateIndex = 4

        ac = AlgorithmController(instance,3000)
        iteration = 0
        while iteration < 100:
            solution.solutionArray = [-1, -1, -1, -1, -1]
            isCareFullList = [False, False, False, False, False, False, False]
            buildingToAllocateList = copy.deepcopy(instance.buildingList)
            careToFillList = copy.deepcopy(instance.careList)
            isAllCareFull, careToFillIndex = ac.chooseCare(buidlingToAllocateIndex, buildingToAllocateList,
                                                           careToFillList, isCareFullList, solution)
            iteration += 1

        # vérifier si le care sélectionner pour le bâtiment 4 est le care 3 après 100 itérations
        self.assertTrue(careToFillIndex == 3)


    def test_allocateBuilding(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "allocateBuilding()"

        :return: rien
        '''

        instance = self.build_instance()
        solution = SolutionModel()
        ac = AlgorithmController(instance, 3000)
        distanceSortedBuildingIndexMatrix = ac.sortBuildingIndexForEachCareInDistanceMatrix()
        ant = AntModel()

        # initialiser la liste de solution
        solution.solutionArray = [-1, -1, -1, -1, -1]
        solutionForOneIterationList = []
        qualityOfSolutionForOneIterationList = []
        copyDistanceSortedBuildingIndexMatrix = copy.deepcopy(distanceSortedBuildingIndexMatrix)
        ac.allocateBuilding(ant, copyDistanceSortedBuildingIndexMatrix, solutionForOneIterationList,
                            qualityOfSolutionForOneIterationList)

        # vérifier si la liste de qualité a un élément et la valeur d'élément n'est pas 0
        # et la liste de solution retournée n'est plus [-1,-1,-1,-1,-1]
        self.assertTrue(len(qualityOfSolutionForOneIterationList) == 1 and qualityOfSolutionForOneIterationList[0] != 0
                        and ant.solution.solutionArray != solution.solutionArray)


    def test_run(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "run()"

        :return: rien
        '''

        instance = self.build_instance()
        ac = AlgorithmController(instance,3000)

        # le nombre d'itérations est 300
        ac.run(300)

        polulationTotal = 0
        distanceTotal = 0
        i = 0
        while i < len(ac.bestSolution.solutionArray):
            j = ac.bestSolution.solutionArray[i]
            if j != -1:
                polulationTotal += instance.buildingList[i].population
                distanceTotal += instance.distanceMatrix[i][j]
            i += 1

        # regarder la meilleure solution, le nombre de sans-abris hébergés,
        # la distance totale parcourue, et la qualité de cette solution
        print(ac.bestSolution.solutionArray, polulationTotal,distanceTotal, polulationTotal/(1+distanceTotal))


    def test_calculateDistanceTotalOfOneSolution(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "calculateDistanceTotalOfOneSolution()"

        :return: rien
        '''

        instance = self.build_instance()
        ac = AlgorithmController(instance, 3000)

        # construire une solution
        solution = SolutionModel()
        solution.solutionArray = [4,6,-1,-1,3]

        # vérifier si la distance totale parcourue est égale à 15
        self.assertEqual(ac.calculateDistanceTotalOfOneSolution(solution), 15)


    def test_calculatePopulationAllocatedOfOneSolution(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "calculatePopulationAllocatedOfOneSolution"

        :return: rien
        '''

        instance = self.build_instance()
        ac = AlgorithmController(instance, 3000)

        # construire une solution
        solution = SolutionModel()
        solution.solutionArray = [4, 6, -1, -1, 3]

        # vérifier si le nombre de sans-abris hébergés est égale à 44
        self.assertEqual(ac.calculatePopulationAllocatedOfOneSolution(solution),44)


    def test_calculateBuildingAllocatedOfOneSolution(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "calculateBuildingAllocatedOfOneSolution()"

        :return: rien
        '''

        instance = self.build_instance()
        ac = AlgorithmController(instance, 3000)

        # construire une solution
        solution = SolutionModel()
        solution.solutionArray = [4, 6, -1, -1, 3]

        # vérifier si le nombre de bâtiments affectés est égale à 3
        self.assertEqual(ac.calculateBuildingAllocatedOfOneSolution(solution),3)


if __name__ == '__main__':
    unittest.main()