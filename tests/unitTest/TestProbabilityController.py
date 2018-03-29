#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du test unitaire de la classe "ProbabilityController"

Version: 1.0

Auteur: Peng BI
'''

import unittest
from controllers.ProbabilityController import ProbabilityController

class Test_ProbabilityController(unittest.TestCase):
    '''
    Description:
        Cette classe est pour faire le test unitaire sur la classe "ProbabilityController"

    Attribut; rien
    '''

    def test_calculateProbability(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "calculateProbability()",pour vérifier
            si la méthode peut correctement calculer la probabilité de déplacement

        :return: rien
        '''

        pc = ProbabilityController()

        tau = 0.8
        eta = 1/4000
        booleanList = [False, True, True, False, True]

        # vérifier si la probabilité calculée retournée est égale à 0.00019992003198720514
        self.assertEqual(pc.calculateProbability(eta, tau, booleanList), 0.00019992003198720514)


    def test_generateProbability(self):
        '''
        Description:
            Cette méthode est pour tester la méthode "generateProbability()",pour vérifier
            si la méthode peut correctement choisir un article selon leurs probabilités

        :return: rien
        '''

        pc = ProbabilityController()

        idProbabilityList = [0,1,2,3]
        probabilityList = [0.15,0.26,0.58,0.73]

        # la liste d'occurence pour chaque id
        occurenceList = [0,0,0,0]
        for i in range(100):
            item = pc.generateProbability(idProbabilityList, probabilityList)
            occurenceList[item] += 1

        # vérifier si aucun id est sélectionné 100 fois après 100 itérations
        self.assertTrue(occurenceList[0] != 100 and occurenceList[1] != 100 and occurenceList[2] != 100 and occurenceList[3] != 100)


if __name__ == '__main__':
    unittest.main()
