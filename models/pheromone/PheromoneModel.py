#-*-coding:utf-8-*-


class PheromoneModel:
    '''
    Description: cette classe est le modèle de phéromone
    Attributs:
        eta: (float) la désirabilité de mouvement
        tau: (float) la quantité de phéromones existant
        deltaTau: (float) la quantité de phéromones déposés lors que la fourmi prend un nœud ou un arc
        rho: (float) le taux d'évaporation de phéromones
    '''

    def __init__(self):
        '''
        Desciption: cette méthode est le constructeur de la classe PheromoneModel
        '''

        self.eta = 0.00 # (float) la désirabilité de mouvement
        self.tau = 0.00 # (float) la quantité de phéromones existant
        self.deltaTau = 0.00    # (float) la quantité de phéromones déposés lors que la fourmi prend un nœud ou un arc
        self.rho = 0.00 # (float) le taux d'évaporation de phéromones