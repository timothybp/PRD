import unittest
from controllers.FileController import FileController

class TestFileController(unittest.TestCase):
    def test_ReadBuildingFile(self):
        fc = FileController()
        contentList = fc.readBuildingFile('../../files/Rq22_51760B_TriCrOID_TriNSACr4.txt')
        self.assertTrue(len(contentList) == 500)

    def test_ReadCareFile(self):
        fc = FileController()
        contentList = fc.readCareFile('../../files/Rq33_187CareMoveID188.txt')
        self.assertTrue(len(contentList) == 187)

    def test_ReadDistanceFile(self):
        fc = FileController()
        contentList = fc.readDistanceFile('../../files/LOD9679120_IdNet_NSACr3.txt')
        self.assertTrue(len(contentList) == 93500)

if __name__ == '__main__':
    unittest.main()