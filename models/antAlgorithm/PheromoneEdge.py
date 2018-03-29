#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du modèle de phéromone qui est déposée sur les arcs entre le bâtiment et le care

Version: 1.0

Auteur: Peng BI
'''

from models.antAlgorithm.PheromoneModel import PheromoneModel

class PheromoneEdge(PheromoneModel):
    '''
    Description:
        Cette classe est le modèle de phéromone qui est déposée sur les arcs entre le bâtiment et le care

    Classe parent:
        PeromoneModel (cette classe hérite de la classe PeromoneModel)

    Attributs:
        Tous les attributs de classe parent
    '''

    def __init__(self):
        '''
        Desciption:
            Cette méthode est le constructeur de la classe PheromoneEdge
        '''

        PheromoneModel.__init__(self)