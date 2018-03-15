from models.pheromone.PheromoneModel import PheromoneModel

# Cette classe est le modèle de phéromone qui est déposée sur l'arc entre le bâtiment et le care
class PheromoneEdge(PheromoneModel):

    def __init__(self):
        PheromoneModel.__init__(self)