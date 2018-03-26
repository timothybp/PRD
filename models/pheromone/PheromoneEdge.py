#-*-coding:utf-8-*-

from models.pheromone.PheromoneModel import PheromoneModel


class PheromoneEdge(PheromoneModel):
    '''
    Description: cette classe est le modèle de phéromone qui est déposée sur les arcs entre le bâtiment et le care
    Classe parent: PeromoneModel (cette classe hérite de la classe PeromoneModel)
    Attributs:
        Tous les attributs de classe parent
    '''

    def __init__(self):
        '''
        Desciption: cette méthode est le constructeur de la classe PheromoneEdge
        '''

        PheromoneModel.__init__(self)