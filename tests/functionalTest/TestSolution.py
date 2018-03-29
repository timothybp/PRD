#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du test fonctionnel. Il dessiner
    les points de bâtiment et les points de care dans les figure

Version: 1.0

Auteur: Peng BI
'''

import matplotlib.pyplot as plt

class TestSolution:
    '''
    Description:
        Cette classe est pour nous aider évaluer la solution obtenue

    Attribut: rien
    '''

    def drawMap(self):
        '''
        Description:
            Cette méthode est pour dessiner les points de bâtiments et les point
            de care dans la figure pour visuellement regarder leurs positions

        :return: rien
        '''

        xBuildingList = []
        yBuildingList = []
        idBuildingList = []

        # lire le fichier de bâtiments pour obtenir les coordonnées de chaque bâtiment
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

        # lire le fichier de care pour obtenir les coordonnées de chaque care
        counter = 0
        with open('../../files/Rq33_187CareMoveID188.txt', 'rt') as cares:
            for care in cares:
                if counter != 0:
                    idCareList.append(care.split('\t')[0])
                    xCareList.append(care.split('\t')[1])
                    yCareList.append(care.split('\t')[2])
                counter += 1

        # dessiner la figure pour les bâtiments
        plt.subplot(211)
        plt.scatter(xBuildingList, yBuildingList, c='r')
        for i, idBuilding in enumerate(idBuildingList):
            plt.annotate(idBuilding, (xBuildingList[i], yBuildingList[i]))
        plt.legend(['Bâtiment'])

        # dessiner la figure pour les cares
        plt.subplot(212)
        plt.scatter(xCareList, yCareList, c='b')
        for j, idCare in enumerate(idCareList):
            plt.annotate(idCare, (xCareList[j], yCareList[j]))
        plt.legend(['Centre d\'accueil'])

        plt.show()


if __name__ == '__main__':
    testSolution = TestSolution()
    testSolution.drawMap()