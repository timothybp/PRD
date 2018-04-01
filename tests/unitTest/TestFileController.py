#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du test unitaire de la classe "FileController"

Version: 1.0

Auteur: Peng BI
'''

import unittest
from controllers.FileController import FileController
from models.antAlgorithm.SolutionModel import SolutionModel
from models.instance.InstanceModel import InstanceModel
from models.data.BuildingModel import BuildingModel
from models.data.CareModel import CareModel

class TestFileController(unittest.TestCase):
    '''
    Description:
        Cette classe est pour faire le test unitaire sur la classe "FileController"

    Attribut; rien
    '''

    def test_readBuildingFile(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "readBuildingFile()",
            pour vérifier si la méthode peut bien lire le fichier de bâtiment

        :return: rien
        '''
        fc = FileController()
        contentList = fc.readBuildingFile('../../files/Rq22_51760B_TriCrOID_TriNSACr4.txt')

        # vérifier si le nombre de lignes lues est 50 (sauf la première ligne)
        self.assertTrue(len(contentList) == 50)


    def test_readCareFile(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "readCareFile()",
            pour vérifier si la méthode peut bien lire le fichier de care

        :return: rien
        '''

        fc = FileController()
        contentList = fc.readCareFile('../../files/Rq33_187CareMoveID188.txt')

        # vérifier si le nombre de lignes lues est 20 (sauf la première ligne)
        self.assertTrue(len(contentList) == 20)


    def test_readDistanceFile(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "readDistanceFile()",
            pour vérifier si la méthode peut bien lire le fichier de distance

        :return: rien
        '''

        fc = FileController()
        contentList = fc.readDistanceFile('../../files/LOD9679120_IdNet_NSACr3.txt')

        # vérifier si le nombre de lignes lues est 1000 (sauf la première ligne)
        self.assertTrue(len(contentList) == 1000)


    def test_readConfigurationFile(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "readConfigurationFile",
            pour vérifier si la méthode peut lire les objets dans le fichier JSON

        :return: rien
        '''

        configFileName = '../../configuration/configParameters.json'
        fc = FileController()
        configJson = fc.readConfigurationFile(configFileName)

        # vérifier si toutes les paramètres de besoin sont bien lues du fichier de configuraton
        self.assertTrue('antQuantity' in configJson.keys() and 'iterationTimes'in configJson.keys() and
                        'careEffectRadius' in configJson.keys() and 'inputFiles' in configJson.keys() and
                        'outputFiles' in configJson.keys() and 'pheromone' in configJson.keys())


    def test_writeSolutionFile(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "writeSolutionFile()",
            pour vérifier si la méthode peut bien écrire la solution dans le fichier

        :return: rien
        '''

        solutionFilename = '../../files/bestSolution_test.txt'

        # construire une solution
        bestSolution = SolutionModel()
        bestSolution.solutionArray = [4,5,6,-1,3]

        # construire 5 bâtiments
        instance = InstanceModel()
        population = [9, 5, 16, 27, 30]
        i = 0
        while i < 5:
            building = BuildingModel()
            building.idBuilding = i
            building.population = population[i]
            instance.buildingList.append(building)
            i += 1

        # construire 7 cares
        capacity = [8, 15, 6, 34, 13, 10, 18]
        j = 0
        while j < 7:
            care = CareModel()
            care.idCare = j
            care.capacity = capacity[j]
            instance.careList.append(care)
            j += 1

        # écrire la solution dans le fichier, on peut département vérifier dans le fichier de solution
        fc = FileController()
        fc.writeSolutionFile(solutionFilename, bestSolution, instance)


    def test_writeQualityFile(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "writeQualityFile()", pour vérifier
            si la méthode peut bien écrire les qualités des solutions dans le fichier

        :return: rien
        '''

        qualityFileName = '../../files/quality_test.txt'

        # initialiser ces 5 listes à écrire
        bestQualityOfEachIterationList = [0.1477832512315271,0.09865470852017937]
        averageQualityOfEachIterationList = [0.07858062847465425, 0.05374583753472586]
        distanceTotalOfEachIterationList = [100,200]
        populationAllocatedOfEachIterationList = [25,30]
        buildingAllocatedOfEachIterationList = [4,5]

        # écrire les qualités de solutions dans le fichier, on peut département vérifier dans le fichier de qualité
        fc = FileController()
        fc.writeQualityFile(qualityFileName, bestQualityOfEachIterationList,
                            averageQualityOfEachIterationList,distanceTotalOfEachIterationList,
                            populationAllocatedOfEachIterationList, buildingAllocatedOfEachIterationList)


if __name__ == '__main__':
    unittest.main()