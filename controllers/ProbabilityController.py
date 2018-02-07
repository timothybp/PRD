import random

class ProbabilityController:
    def calculateProbability(self, eta, tau, booleanList):
        numerator = tau * eta
        i = 0
        sum = 0
        while i < len(booleanList) - 1:
            sum += tau * eta * (1 - booleanList[i])
            i += 1
        denominator = 1 + sum
        probability = numerator / denominator
        return probability



    def generateProbability(self, idProbabilityList, probabilityList):
        probabilityCompared = random.uniform(0, 1)
        probabilityCumulative = 0.0
        for item, itemProbability in zip(idProbabilityList, probabilityList):
            probabilityCumulative = probabilityCumulative + itemProbability
            if probabilityCompared < probabilityCumulative:
                break
        return item