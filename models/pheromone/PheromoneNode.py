from models.pheromone.PheromoneModel import PheromoneModel

# Cette classe est le modèle de phéromone qui est déposée sur le nœud de bâtiment
class PheromoneNode(PheromoneModel):

    def __init__(self):
        PheromoneModel.__init__(self)