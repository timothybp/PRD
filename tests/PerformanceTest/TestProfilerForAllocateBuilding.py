#-*-coding:utf-8-*-

from tests.PerformanceTest.ProfilerAlgorithmController import ProfilerAlgorithmController
from models.instance.InstanceModel import InstanceModel
from models.data.BuildingModel import BuildingModel
from models.data.CareModel import CareModel
from models.ant.SolutionModel import SolutionModel
from models.ant.AntModel import AntModel
from models.pheromone.PheromoneEdge import PheromoneEdge
from models.pheromone.PheromoneNode import PheromoneNode
import copy


class TestProfilerForAllocateBuilding:

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

    def test_allocateBuilding(self):
        instance = self.build_instance()

        solution = SolutionModel()

        pac = ProfilerAlgorithmController(instance, 3000)
        distanceSortedBuildingIndexMatrix = pac.sortBuildingIndexForEachCareInDistanceMatrix()
        ant = AntModel()
        solution.solutionArray = [-1, -1, -1, -1, -1, -1, -1]
        solutionForOneIterationList = []
        qualityOfSolutionForOneIterationList = []
        copyDistanceSortedBuildingIndexMatrix = copy.deepcopy(distanceSortedBuildingIndexMatrix)
        pac.allocateBuilding(ant, copyDistanceSortedBuildingIndexMatrix, solutionForOneIterationList,
                            qualityOfSolutionForOneIterationList)

if __name__ == '__main__':
    profilerAllocateBuilding = TestProfilerForAllocateBuilding()
    profilerAllocateBuilding.test_allocateBuilding()