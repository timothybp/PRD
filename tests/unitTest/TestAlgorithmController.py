import unittest
from controllers.AlgorithmController import AlgorithmController
from models.instance.InstanceModel import InstanceModel

class TestAlgorithmController(unittest.TestCase):
    def test_merge_sort(self):
        distanceColumn = [2,56,3,22]
        distanceIndexRow = [0,1,2,3]
        instance = InstanceModel()
        instance.distanceMatrix = [[2, 4, 5, 3, 1], [56, 29, 3, 43, 11], [3, 54, 67, 13, 4], [22, 51, 78, 32, 45]]
        ac = AlgorithmController(instance)
        distanceColumn, distanceIndexRow = ac.merge_sort(distanceColumn, distanceIndexRow)
        self.assertListEqual(distanceIndexRow, [0,2,3,1])


    def test_sortBuildingIndexForEachCareInDistanceMatrix(self):
        instance = InstanceModel()
        instance.distanceMatrix = [[2,4,5,3,1],[56,29,3,43,11], [3,54,67,13,4], [22,51,78,32,45]]
        targetList = [[0,2,3,1],[0,1,3,2],[1,0,2,3],[0,2,3,1],[0,2,1,3]]
        ac = AlgorithmController(instance)
        self.assertListEqual(ac.sortBuildingIndexForEachCareInDistanceMatrix(),targetList)

if __name__ == '__main__':
    unittest.main()