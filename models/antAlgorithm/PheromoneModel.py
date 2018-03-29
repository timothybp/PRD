#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du modèle de phéromone pour l'algorithme de colonie de fourmis

Version: 1.0

Auteur: Peng BI
'''

class PheromoneModel:
    '''
    Description:
        Cette classe est le modèle de phéromone

    Attributs:
        eta: (float) la désirabilité de mouvement
        tau: (float) la quantité de phéromones existant
        deltaTau: (float) la quantité de phéromones déposés lors que la fourmi prend un nœud ou un arc
        rho: (float) le taux d'évaporation de phéromones
    '''

    def __init__(self):
        '''
        Desciption:
            Cette méthode est le constructeur de la classe PheromoneModel
        '''

        self.eta = 0.00 # (float) la désirabilité de mouvement
        self.tau = 0.00 # (float) la quantité de phéromones existant
        self.deltaTau = 0.00    # (float) la quantité de phéromones déposés lors que la fourmi prend un nœud ou un arc
        self.rho = 0.00 # (float) le taux d'évaporation de phéromones