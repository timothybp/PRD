#-*-coding:utf-8-*-

from models.ant.SolutionModel import SolutionModel


class AntModel:
    '''
    Descritpion: cette classe est le modèle de fourmi
    Attributs:
        idAnt: (int) l'identidiant de fourmi
        solution: (l'objet de la classe SolutionModel) la solution trouvée de fourmi
    '''

    def __init__(self):
        '''
        Description: cette méthode est le constructeur de la classe AntModel
        '''

        self.idAnt = 0  # (int) l'identidiant de fourmi
        self.solution = SolutionModel() # (l'objet de la classe SolutionModel) la solution trouvée de fourmi