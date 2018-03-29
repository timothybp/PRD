#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du modèle de fourmi pour l'algorithme de colonie de fourmis

Version: 1.0

Auteur: Peng BI
'''

from models.antAlgorithm.SolutionModel import SolutionModel

class AntModel:
    '''
    Descritpion:
        Cette classe est le modèle de fourmi

    Attributs:
        idAnt: (int) l'identifiant de fourmi
        solution: (l'objet de la classe SolutionModel) la solution trouvée de fourmi
    '''

    def __init__(self):
        '''
        Description:
            Cette méthode est le constructeur de la classe AntModel
        '''

        self.idAnt = 0  # (int) l'identidiant de fourmi
        self.solution = SolutionModel() # (l'objet de la classe SolutionModel) la solution trouvée de fourmi