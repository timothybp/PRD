#-*-coding:utf-8-*-

import unittest
from controllers.FileController import FileController
from models.ant.SolutionModel import SolutionModel
from models.instance.InstanceModel import InstanceModel
from models.data.BuildingModel import BuildingModel
from models.data.CareModel import CareModel

class TestFileController(unittest.TestCase):
    def test_ReadBuildingFile(self):
        fc = FileController()
        contentList = fc.readBuildingFile('../../files/Rq22_51760B_TriCrOID_TriNSACr4.txt')
        self.assertTrue(len(contentList) == 50)

    def test_ReadCareFile(self):
        fc = FileController()
        contentList = fc.readCareFile('../../files/Rq33_187CareMoveID188.txt')
        self.assertTrue(len(contentList) == 10)

    def test_ReadDistanceFile(self):
        fc = FileController()
        contentList = fc.readDistanceFile('../../files/LOD9679120_IdNet_NSACr3.txt')
        self.assertTrue(len(contentList) == 500)

    def test_writeSolutionFile(self):
        solutionFilename = '../../files/bestSolution_test.txt'
        bestSolution = SolutionModel()
        bestSolution.solutionArray = [4,5,6,-1,3]

        instance = InstanceModel()
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

        fc = FileController()
        fc.writeSolutionFile(solutionFilename, bestSolution, instance)

    def test_writeQualityFile(self):
        qualityFileName = '../../files/quality_test.txt'
        bestQualityOfEachIterationList = [0.1477832512315271,0.09865470852017937]
        averageQualityOfEachIterationList = [0.07858062847465425, 0.05374583753472586]

        fc = FileController()
        fc.writeQualityFile(qualityFileName, bestQualityOfEachIterationList, averageQualityOfEachIterationList)


if __name__ == '__main__':
    unittest.main()