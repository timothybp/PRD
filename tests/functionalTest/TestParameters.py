import matplotlib.pyplot as plt
from decimal import *

class TestParameters:
    def drawFigure(self):
        bestQualityOfSolutionForEachIterationList = []
        averageQualityOfSolutionForEachIterationList = []

        counter = 0
        with open('../../files/quality.txt', 'rt') as qualities:
            for quality in qualities:
                if counter != 0:
                    bestQualityOfSolutionForEachIterationList.append(float(quality.split('\t')[1]))
                    averageQualityOfSolutionForEachIterationList.append(float(quality.split('\t')[2]))
                counter += 1

        iteration = len(bestQualityOfSolutionForEachIterationList)
        print(iteration)
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