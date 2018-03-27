#-*-coding:utf-8-*-

import unittest
from controllers.InstanceController import InstanceController
from models.instance.InstanceModel import InstanceModel
from models.data.BuildingModel import BuildingModel
from models.data.CareModel import CareModel
from models.ant.AntModel import AntModel
from models.pheromone.PheromoneEdge import PheromoneEdge
from models.pheromone.PheromoneNode import PheromoneNode


class TestInstanceController(unittest.TestCase):

    def test_constructInstance(self):
        antQuantity = 10
        buildingFileName = '../../files/Rq22_51760B_TriCrOID_TriNSACr4.txt'
        careFileName = '../../files/Rq33_187CareMoveID188.txt'
        distanceFileName = '../../files/LOD9679120_IdNet_NSACr3.txt'

        ic = InstanceController()
        ic.constructInstance(antQuantity, buildingFileName, careFileName, distanceFileName)
        self.assertTrue(len(ic.instance.buildingList) == 50 and len(ic.instance.careList) == 10 and
                        len(ic.instance.distanceMatrix) == 50 and len(ic.instance.distanceMatrix[0]) == 10 and
                        len(ic.instance.antList) == 10)

    def test_solveProblem(self):
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
            pheromoneNode.eta = 1 / population[i]
            pheromoneNode.rho = 0.1
            pheromoneNode.eta = 0.9
            instance.pheromoneNodeList.append(pheromoneNode)
            i += 1

        i = 0
        while i < len(instance.buildingList):
            j = 0
            while j < len(instance.careList):
                pheromoneEdge = PheromoneEdge()
                pheromoneEdge.eta = 1 / instance.distanceMatrix[i][j]
                pheromoneEdge.rho = 0.1
                pheromoneEdge.eta = 0.9
                instance.pheromoneEdgeMatrix[i].append(pheromoneEdge)
                j += 1
            if i != len(instance.buildingList) - 1:
                instance.pheromoneEdgeMatrix.append([])
            i += 1

        instance.antList = [AntModel(), AntModel(), AntModel(), AntModel(), AntModel()]

        ic = InstanceController()
        ic.instance = instance

        ic.solveProblem(200, 300, "../../files/bestSolution_test.txt", "../../files/quality_test.txt")

if __name__ == '__main__':
    unittest.main()