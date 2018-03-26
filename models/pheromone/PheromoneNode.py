#-*-coding:utf-8-*-

from models.pheromone.PheromoneModel import PheromoneModel


class PheromoneNode(PheromoneModel):
    '''
    Description: cette classe est le modèle de phéromone qui est déposée sur les nœuds de bâtiment
    Classe parent: PeromoneModel (cette classe hérite de la classe PeromoneModel)
    Attributs:
        Tous les attributs de classe parent
    '''

    def __init__(self):
        '''
        Desciption: cette méthode est le constructeur de la classe PheromoneNode
        '''

        PheromoneModel.__init__(self)