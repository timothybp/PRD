from models.ant.SolutionModel import SolutionModel

# Cette classe est le modèle de fourmi
class AntModel:

    def __init__(self):
        self.idAnt = 0  # L'identifiant de fourmi
        self.solution = SolutionModel()