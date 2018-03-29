#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du modèle de bâtiment, qui est l'une instance de problème à résoudre

Version: 1.0

Auteur: Peng BI
'''

class BuildingModel:
    '''
    Description:
        Cette classe est le modèle de bâtiment

    Attributs:
        idBuilding: (int) l'identifiant de bâtiment
        population: (float) le nombre de sans-abris dans le bâtiment
    '''

    def __init__(self):
        '''
        Description:
            Cette méthode est le constructeur de la classe BuildingModel
        '''

        self.idBuilding = 0 # (int) l'identifiant de bâtiment
        self.population = 0.00  # (float) le nombre de sans-abris dans le bâtiment