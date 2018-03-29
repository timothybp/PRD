#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du modèle de solution trouvée par la fourmi

Version: 1.0

Auteur: Peng BI
'''

class SolutionModel:
    '''
    Description:
        Cette classe est le modèle de solution construite par chaque fourmi

    Attributs:
        solutionArray: (int[]) le tableau d'une solution
        quality: (float) la qualité de solution
    '''

    def __init__(self):
        '''
        Description:
            Cette méthode est le constructeur de la classe SolutionModel
        '''

        self.solutionArray = [] # (int[]) le tableau d'une solution
        self.quality = 0.00 # (float) la qualité de solution
