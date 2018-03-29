#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du modèle de phéromone qui est déposée sur les nœuds de bâtiment

Version: 1.0

Auteur: Peng BI
'''

from models.antAlgorithm.PheromoneModel import PheromoneModel

class PheromoneNode(PheromoneModel):
    '''
    Description:
        Cette classe est le modèle de phéromone qui est déposée sur les nœuds de bâtiment

    Classe parent:
        PeromoneModel (cette classe hérite de la classe PeromoneModel)

    Attributs:
        Tous les attributs de classe parent
    '''

    def __init__(self):
        '''
        Desciption:
            Cette méthode est le constructeur de la classe PheromoneNode
        '''

        PheromoneModel.__init__(self)