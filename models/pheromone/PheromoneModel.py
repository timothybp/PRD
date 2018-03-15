# Cette classe est le modèle de phéromone
class PheromoneModel:

    def __init__(self):
        self.eta = 0.00 # La désirabilité de mouvement
        self.tau = 0.00 # La quantité de phéromones existant
        self.deltaTau = 0.00    # La quantité de phéromones déposés lors que la fourmi prend un nœud ou un arc
        self.rho = 0.00 # Le taux d'évaporation de phéromones