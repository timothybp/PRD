import unittest
from controllers.InstanceController import InstanceController

class TestInstanceController(unittest.TestCase):

    def test_constructInstance(self):
        antQuantity = 10
        buildingFileName = '../../files/Rq22_51760B_TriCrOID_TriNSACr4.txt'
        careFileName = '../../files/Rq33_187CareMoveID188.txt'
        distanceFileName = '../../files/LOD9679120_IdNet_NSACr3.txt'

        ic = InstanceController()
        ic.constructInstance(antQuantity, buildingFileName, careFileName, distanceFileName)
        self.assertTrue(len(ic.instance.buildingList) == 500 and len(ic.instance.careList) == 187 and
                        len(ic.instance.distanceMatrix) == 500 and len(ic.instance.distanceMatrix[0]) == 187 and
                        len(ic.instance.antList) == 10)

if __name__ == '__main__':
    unittest.main()