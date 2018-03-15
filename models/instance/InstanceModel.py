#Cette class est le modèle d'instance
class InstanceModel:

    def __init__(self):
        self.buildingList = []  # La liste de bâtiments
        self.careList = []  # La liste de cares
        self.distanceMatrix = [[]]  # La matrice de distances entre chaque bâtiment et chaque care
        self.pheromoneNodeList = []  # La liste de phéromones sur le nœud de bâtiment
        self.pheromoneEdgeMatrix = [[]]  # La matrice de phéromones sur l'arc entre le batiments et le case
        self.antList = []   #La liste de fourmis


