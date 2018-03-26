#-*-coding:utf-8-*-


class BuildingModel:
    '''
    Description: cette classe est le modèle de bâtiment
    Attributs:
        idBuilding: (int) l'identifiant de bâtiment
        population: (float) le nombre de sans-abris dans le bâtiment
    '''

    def __init__(self):
        '''
        Description: cette méthode est le constructeur de la classe BuildingModel
        '''

        self.idBuilding = 0 # (int) l'identifiant de bâtiment
        self.population = 0.00  # (float) le nombre de sans-abris dans le bâtiment