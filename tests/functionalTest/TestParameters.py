#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du test fonctionnel. Il dessiner les courbes de la qualité
    des meilleures solution et la qualité moyenne des solutions dans la figure

Version: 1.0

Auteur: Peng BI
'''

import matplotlib.pyplot as plt

class TestParameters:
    '''
    Description:
        Cette classe est pour déterminer le nombre d'itérations

    Attribut: rien
    '''

    def drawFigure(self):
        '''
        Description:
            Cette méthode est pour dessiner la courbe de qualité des meilleures solutions de chaque
            itérations et dessiner la courbe de qualité moyenne de solutions de chaque itérations

        :return: rien
        '''

        bestQualityOfSolutionForEachIterationList = []
        averageQualityOfSolutionForEachIterationList = []

        # lire le fichire de qualité, et extraire la colonne de meilleure qualité et la colonne de qualité moyenne
        counter = 0
        with open('../../files/quality.txt', 'rt') as qualities:
            for quality in qualities:
                if counter != 0:
                    bestQualityOfSolutionForEachIterationList.append(float(quality.split('\t')[1]))
                    averageQualityOfSolutionForEachIterationList.append(float(quality.split('\t')[2]))
                counter += 1

        # chercher l'id d'itération où la meilleure qualité est maximum
        maxQualityIteration = bestQualityOfSolutionForEachIterationList.index(max(bestQualityOfSolutionForEachIterationList))
        print("La meilleure solution est dans itération %d" % int(maxQualityIteration))

        # dessiner la figure, l'axe x est l'itération, l'axe y est la qualité
        iteration = len(bestQualityOfSolutionForEachIterationList)
        x = [x for x in range(0,iteration)]
        y1 = bestQualityOfSolutionForEachIterationList
        y2 = averageQualityOfSolutionForEachIterationList

        plt.figure()
        plt.plot(x, y1, 'b', linewidth=0.5, marker='*')
        plt.plot(x, y2, 'r', linewidth=2, marker='+')

        plt.fill_between(x, y1, y2, color='g', alpha=0.5)
        plt.legend(['bestSolution', 'averageSolution'])
        plt.xlabel('Iteration')
        plt.ylabel('Quality')

        plt.show()


if __name__ == '__main__':
    testParameter = TestParameters()
    testParameter.drawFigure()