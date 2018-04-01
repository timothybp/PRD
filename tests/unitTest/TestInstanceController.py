#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du test unitaire de la classe "InstanceController"

Version: 1.0

Auteur: Peng BI
'''

import unittest
import json
from controllers.InstanceController import InstanceController
from models.antAlgorithm.AntModel import AntModel
from models.antAlgorithm.PheromoneEdge import PheromoneEdge
from models.antAlgorithm.PheromoneNode import PheromoneNode
from models.data.BuildingModel import BuildingModel
from models.data.CareModel import CareModel
from models.instance.InstanceModel import InstanceModel


class TestInstanceController(unittest.TestCase):
    '''
    Description:
        Cette classe est pour faire le test unitaire sur la classe "InstanceController"

    Attribut; rien
    '''

    def build_configurationJson(self):
        '''
        Description:
            Cette méthode est pour construire un objet de JSON qui contient
            toutes les valeurs de paramètres dont le programme a besoin

        :return: configJson: (l'objet de JSON) les valeurs des paramètres
        '''

        configJson = json.loads('{'
                                    '"antQuantity": 10,'
                                    '"iterationTimes": 200,'
                                    '"careEffectRadius": 3000,'
                                    '"inputFiles":'
                                    '{'
                                        '"buildingFileName": "../../files/Rq22_51760B_TriCrOID_TriNSACr4.txt",'
                                        '"careFileName": "../../files/Rq33_187CareMoveID188.txt",'
                                        '"distanceFileName": "../../files/LOD9679120_IdNet_NSACr3.txt"'
                                    '},'
                                    '"outputFiles": {'
                                        '"solutionFileName": "../../files/bestSolution.txt",'
                                        '"qualityFileName": "../../files/quality.txt"'
                                    '},'
                                    '"pheromone": '
                                    '{'
                                        '"rhoNode": 0.000001,'
                                        '"tauNode": 0.8,'
                                        '"rhoEdge": 0.1, '
                                        '"tauEdge": 0.9'
                                    '}'
                                '}')

        return configJson


    def test_constructInstance(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "constructInstance()", pour vérifier si elle
            peut correctement construire l'instance selon les données de fichiers importés

        :return: rien
        '''

        configJson = self.build_configurationJson()

        ic = InstanceController(configJson)
        ic.constructInstance()

        # vérifier si le nombre de battements est 50 et le nombre de cares est 20 et
        # si la taille de la première dimension de la matrice de distance est 50 et
        # la taille de la deuxième dimension de la matrice de distance est 20 et
        # si le nombre de fourmis est 10
        self.assertTrue(len(ic.instance.buildingList) == 50 and len(ic.instance.careList) == 20 and
                        len(ic.instance.distanceMatrix) == 50 and len(ic.instance.distanceMatrix[0]) == 20 and
                        len(ic.instance.antList) == 10)


    def test_solveProblem(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "solveProblem)", pour vérifier si elle
            peut bien connecter l'entrée d'algorithme et les méthodes pour l'écriture de fichier

        :return: rien
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

        configJson = self.build_configurationJson()

        ic = InstanceController(configJson)
        ic.instance = instance

        # le nombre d'itérations est 200 et le rayon initial d'attraction de care est 3000m
        ic.solveProblem()


if __name__ == '__main__':
    unittest.main()