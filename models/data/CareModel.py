#-*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du modèle de care, qui est l'une instance de problème à résoudre

Version: 1.0

Auteur: Peng BI
'''

class CareModel:
    '''
    Description:
        Cette classe est modèle de centre d'accueil

    Attributs:
        idCare: (int) l'identifiant de centre d'accueil
        capacity: (float) la capacité de centre d'accueil
    '''

    def __init__(self):
        '''
        Description:
            Cette méthode est le constructeur de la classe CareModel
        '''

        self.idCare = 0 # (int) l'identifiant de centre d'accueil
        self.capacity = 0.00 # (float) la capacité de centre d'accueil