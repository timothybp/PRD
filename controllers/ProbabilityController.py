#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du contrôleur de probabilité, qui sert à calculer la probabilité de déplacement
    pour la fourmi et sélectionner un bâtiment ou un care selon leurs probabilités de déplacement

Version: 1.0

Auteur: Peng BI
'''

import random

class ProbabilityController:
    '''
    Description:
        Cette classe est pour contrôler la probabilité lorsque les fourmis déplacent

    Attributs: rien
    '''

    def calculateProbability(self, eta, tau, booleanList):
        '''
        Description:
            Cette méthode est pour calculer la probabilité de déplacement

        :param eta: (float) la désirabilité de déplacement
        :param tau: (float) la quantité de phéromones existant sur un nœud de bâtiment ou un arc entre un bâtiment et un care
        :param booleanList: (boolean[]) soit la liste qui marque si le bâtiment est déjà affecté, soit la liste qui marque si le care est plein

        :return: probability: (float) la probabilité de déplacement calculée
        '''

        # calculer le numérateur
        numerator = tau * eta

        # calculer le dénominateur
        i = 0
        sum = 0
        while i < len(booleanList) - 1:
            sum += tau * eta * (1 - booleanList[i])
            i += 1
        denominator = 1 + sum

        # calculer la probabilité
        probability = numerator / denominator

        return probability


    def generateProbability(self, idProbabilityList, probabilityList):
        '''
        Description:
            Cette méthode est pour sélectionner un événement qui correspond à une probabilité au hasard

        :param idProbabilityList: (int[]) la séquence qui contient les identifiants de bâtiment ou de care
        :param probabilityList: (float[]) la liste de probabilité de déplacement

        :return: item: (int) l'identifiant de l'article(bâtiment ou care) sélectionné au hasard selon les probabilités
        '''

        probabilityCompared = random.uniform(0, 1)  # générer une probabilité à comparer au hasard
        probabilityCumulative = 0.0

        # prendre les pairs de id et probabilité
        for item, itemProbability in zip(idProbabilityList, probabilityList):
            probabilityCumulative = probabilityCumulative + itemProbability
            # si la probabilité à comparer est inférieur à la probabilité cumulée，quitter la boucle
            # et retourner l'id correspondant à la probabilité actuelle
            if probabilityCompared < probabilityCumulative:
                break

        return item