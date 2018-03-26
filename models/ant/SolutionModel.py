#-*-coding:utf-8-*-


class SolutionModel:
    '''
    Description: cette classe est le modèle de solution construite par chaque fourmi
    Attributs:
        solutionArray: (int[]) le tableau d'une solution
        quality: (float) la qualité de solution
    '''

    def __init__(self):
        '''
        Description: cette méthode est le constructeur de la classe SolutionModel
        '''

        self.solutionArray = [] # (int[]) le tableau d'une solution
        self.quality = 0.00 # (float) la qualité de solution
