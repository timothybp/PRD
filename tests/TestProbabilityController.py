import unittest
from controllers.ProbabilityController import ProbabilityController

class calculateProbability(unittest.TestCase):
    def test_CalculateProbability(self):
        pc = ProbabilityController()

        tau = 0.8
        eta = 1/4000
        booleanList = [False, True, True, False, True]

        sum = 0
        for i, booleanElement in enumerate(booleanList):
            sum += tau * eta * (1 - booleanElement)
        probability = (tau * eta) / (1 + sum)

        self.assertEqual(pc.calculateProbability(eta, tau, booleanList), probability)

    def test_generateProbability(self):
        pc = ProbabilityController()

        idProbabilityList = [0,1,2,3]
        probabilityList = [0.15,0.26,0.58,0.73]

        occurenceList = [0,0,0,0]
        for i in range(100):
            item = pc.generateProbability(idProbabilityList, probabilityList)
            occurenceList[item] += 1
        self.assertTrue(occurenceList[0] != 100 and occurenceList[1] != 100 and occurenceList[2] != 100 and occurenceList[3] != 100)

if __name__ == '__main__':
    unittest.main()
