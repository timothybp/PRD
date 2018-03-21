import matplotlib.pyplot as plt

class TestSolution:
    def drawMap(self):
        xBuildingList = []
        yBuildingList = []
        idBuildingList = []
        counter = 0
        with open('../../files/Rq22_51760B_TriCrOID_TriNSACr4.txt', 'rt') as buildings:
            for building in buildings:
                if counter != 0:
                    idBuildingList.append(building.split('\t')[0])
                    xBuildingList.append(building.split('\t')[1])
                    yBuildingList.append(building.split('\t')[2])
                counter += 1

        xCareList = []
        yCareList = []
        idCareList = []
        counter = 0
        with open('../../files/Rq33_187CareMoveID188.txt', 'rt') as cares:
            for care in cares:
                if counter != 0:
                    idCareList.append(care.split('\t')[0])
                    xCareList.append(care.split('\t')[1])
                    yCareList.append(care.split('\t')[2])
                counter += 1

        plt.subplot(211)
        plt.scatter(xBuildingList, yBuildingList, c='r')
        for i, idBuilding in enumerate(idBuildingList):
            plt.annotate(idBuilding, (xBuildingList[i], yBuildingList[i]))
        plt.legend(['Bâtiment'])

        plt.subplot(212)
        plt.scatter(xCareList, yCareList, c='b')
        for j, idCare in enumerate(idCareList):
            plt.annotate(idCare, (xCareList[j], yCareList[j]))
        plt.legend(['Centre d\'accueil'])

        plt.show()


if __name__ == '__main__':
    testSolution = TestSolution()
    testSolution.drawMap()