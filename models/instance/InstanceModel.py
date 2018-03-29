#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du modèle d'instance, qui est l'instance pour le programme

Version: 1.0

Auteur: Peng BI
'''

class InstanceModel:
    '''
    Description:
        Cette class est le modèle d'instance pour ce projet

    Attributs:
        buildingList: (BuildingModel[]) la liste de bâtiments
        careList: (CareList[]) la liste de cares
        distanceMatrix: (float[][]) la matrice de distances entre chaque bâtiment et chaque care
        pheromoneNodeList: (PheromoneNode[]) la liste de phéromones déposée sur le nœud de bâtiment
        pheromoneEdgeMatrix: (PheromoneEdge[][]) la  matrice de phéromones déposée sur l'arc entre le bâtiment et le case
        antList: (AntModel[]) la liste de fourmis
    '''

    def __init__(self):
        '''
        Desciption:
            Cette méthode est le constructeur de la classe InstanceModel
        '''

        self.buildingList = []  # (BuildingModel[]) la liste de bâtiments
        self.careList = []  # (CareList[]) la liste de cares
        self.distanceMatrix = [[]]  # (float[][]) la matrice de distances entre chaque bâtiment et chaque care
        self.pheromoneNodeList = [] # (PheromoneNode[]) la liste de phéromones déposée sur le nœud de bâtiment
        self.pheromoneEdgeMatrix = [[]] # (PheromoneEdge[][]) la  matrice de phéromones déposée sur l'arc entre le batiments et le case
        self.antList = []   # (AntModel[]) la liste de fourmis


