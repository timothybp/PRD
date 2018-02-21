import random

# Cette classe est pour contrôler la probabilité lorsque les fourmis déplacent
class ProbabilityController:

    # Cette méthode est pour calculer la probabilité de déplacement
    # Param : eta : La désirabilité de mouvement
    # Param : tau : La quantité de phéromones existant
    # Param : booleanList : La liste qui marque si le bâtiment est déjà affecté ou le care est déjà plein
    # Return : La probabilité de déplacement
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

    # Cette méthode est pour sélectionner un événement qui correspond à une probabilité au hasard
    # Param : idPrapbabiltyList : La séquence qui contient les identifiants de soit bâtiment soit care
    # Param : probabilityList : La liste de probabilité de déplacement
    # Return  L'identifiant de l'arcticle(bâtiment ou care) sélectionné au hasard selon les probabilité
    def generateProbability(self, idProbabilityList, probabilityList):
        probabilityCompared = random.uniform(0, 1)
        probabilityCumulative = 0.0
        for item, itemProbability in zip(idProbabilityList, probabilityList):
            probabilityCumulative = probabilityCumulative + itemProbability
            if probabilityCompared < probabilityCumulative:
                break
        return item