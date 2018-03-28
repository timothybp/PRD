#-*-coding:utf-8-*-

import unittest
from controllers.AlgorithmController import AlgorithmController
from models.instance.InstanceModel import InstanceModel
from models.data.BuildingModel import BuildingModel
from models.data.CareModel import CareModel
from models.ant.SolutionModel import SolutionModel
from models.ant.AntModel import AntModel
from models.pheromone.PheromoneEdge import PheromoneEdge
from models.pheromone.PheromoneNode import PheromoneNode
import copy

class TestAlgorithmController(unittest.TestCase):
    def test_merge_sort(self):
        distanceColumn = [2,56,3,22]
        distanceIndexRow = [0,1,2,3]
        instance = InstanceModel()
        instance.distanceMatrix = [[2, 4, 5, 3, 1], [56, 29, 3, 43, 11], [3, 54, 67, 13, 4], [22, 51, 78, 32, 45]]
        ac = AlgorithmController(instance,3000)
        distanceColumn, distanceIndexRow = ac.merge_sort(distanceColumn, distanceIndexRow)
        self.assertListEqual(distanceIndexRow, [0,2,3,1])


    def test_sortBuildingIndexForEachCareInDistanceMatrix(self):
        instance = InstanceModel()
        instance.distanceMatrix = [[2,4,5,3,1],[56,29,3,43,11], [3,54,67,13,4], [22,51,78,32,45]]
        targetList = [[0,2,3,1],[0,1,3,2],[1,0,2,3],[0,2,3,1],[0,2,1,3]]
        ac = AlgorithmController(instance,3000)
        self.assertListEqual(ac.sortBuildingIndexForEachCareInDistanceMatrix(),targetList)


    def build_instance(self):
        instance = InstanceModel()
        instance.distanceMatrix = [[10, 20, 30, 15, 5, 20, 30],
                                   [30, 20, 15, 20, 15, 10, 5],
                                   [20, 30, 10, 25, 5, 20, 10],
                                   [40, 10, 5, 30, 25, 15, 10],
                                   [30, 20, 30, 5, 10, 15, 20]]

        population = [9, 5, 16, 27, 30]
        i = 0
        while i < 5:
            building = BuildingModel()
            building.idBuilding = i
            building.population = population[i]
            instance.buildingList.append(building)
            i += 1

        capacity = [8, 15, 6, 34, 13, 10, 18]
        j = 0
        while j < 7:
            care = CareModel()
            care.idCare = j
            care.capacity = capacity[j]
            instance.careList.append(care)
            j += 1

        i = 0
        while i < len(instance.buildingList):
            pheromoneNode = PheromoneNode()
            pheromoneNode.eta = population[i]
            pheromoneNode.rho = 0.000001
            pheromoneNode.tau = 0.8
            instance.pheromoneNodeList.append(pheromoneNode)
            i += 1

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

        instance.antList = [AntModel(), AntModel(), AntModel(), AntModel(), AntModel()]

        return instance

    def test_objectiveFunctionF(self):
        solution = SolutionModel()
        solution.solutionArray = [4,6,4,2,3]

        instance = self.build_instance()
        ac = AlgorithmController(instance, 3000)
        self.assertTrue(ac.objectiveFunctionF(solution) == 435)


    def test_objectiveFunctionG(self):
        solution = SolutionModel()
        solution.solutionArray = (4, 6, 4, 2, 3)

        instance = self.build_instance()
        ac = AlgorithmController(instance, 3000)
        self.assertTrue(ac.objectiveFunctionG(solution) == 87)


    def test_objectiveFunctionH(self):
        solution = SolutionModel()
        solution.solutionArray = (4, 6, 4, 2, 3)

        instance = self.build_instance()
        ac = AlgorithmController(instance, 3000)
        self.assertTrue(ac.objectiveFunctionH(solution) == 5)


    def test_calculateAverageSolutionQualityForEachIteration(self):
        qualityOfSolutionForOneIterationList = [0.5, 0.4, 0.6,0.3, 0.2]

        instance = InstanceModel()
        instance.antList = [AntModel(),AntModel(),AntModel(),AntModel(),AntModel()]
        ac = AlgorithmController(instance, 3000)
        self.assertTrue(ac.calculateAverageSolutionQualityForEachIteration(qualityOfSolutionForOneIterationList) == 0.4)


    def test_chooseCare(self):
        instance = self.build_instance()

        solution = SolutionModel()


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

        self.assertTrue(careToFillIndex == 3)

    def test_allocateBuilding(self):
        instance = self.build_instance()

        solution = SolutionModel()

        ac = AlgorithmController(instance, 3000)
        distanceSortedBuildingIndexMatrix = ac.sortBuildingIndexForEachCareInDistanceMatrix()
        ant = AntModel()
        solution.solutionArray = [-1, -1, -1, -1, -1, -1, -1]
        solutionForOneIterationList = []
        qualityOfSolutionForOneIterationList = []
        copyDistanceSortedBuildingIndexMatrix = copy.deepcopy(distanceSortedBuildingIndexMatrix)
        ac.allocateBuilding(ant, copyDistanceSortedBuildingIndexMatrix, solutionForOneIterationList,
                            qualityOfSolutionForOneIterationList)

        self.assertTrue(len(qualityOfSolutionForOneIterationList) == 1 and qualityOfSolutionForOneIterationList[0] != 0
                        and ant.solution.solutionArray != solution.solutionArray)

    def test_run(self):
        instance = self.build_instance()

        ac = AlgorithmController(instance,3000)
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
        print(ac.bestSolution.solutionArray, polulationTotal,distanceTotal, polulationTotal/(1+distanceTotal))


    def test_calculateDistanceTotalOfOneSolution(self):
        instance = self.build_instance()
        ac = AlgorithmController(instance, 3000)
        solution = SolutionModel()
        solution.solutionArray = [4,6,-1,-1,3]
        self.assertEqual(ac.calculateDistanceTotalOfOneSolution(solution), 15)


    def test_calculatePopulationAllocatedOfOneSolution(self):
        instance = self.build_instance()
        ac = AlgorithmController(instance, 3000)
        solution = SolutionModel()
        solution.solutionArray = [4, 6, -1, -1, 3]
        self.assertEqual(ac.calculatePopulationAllocatedOfOneSolution(solution),44)


    def test_calculateBuildingAllocatedOfOneSolution(self):
        instance = self.build_instance()
        ac = AlgorithmController(instance, 3000)
        solution = SolutionModel()
        solution.solutionArray = [4, 6, -1, -1, 3]
        self.assertEqual(ac.calculateBuildingAllocatedOfOneSolution(solution),3)


if __name__ == '__main__':
    unittest.main()