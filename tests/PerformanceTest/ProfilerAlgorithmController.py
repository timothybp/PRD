# -*-coding:utf-8-*-

'''
Description:
    Ce fichier est le script du test de la performance d'algiruthme avec l'outil "profile"

Version: 1.0

Auteur: Peng BI
'''

import time
from controllers.ProbabilityController import ProbabilityController
from models.antAlgorithm.SolutionModel import SolutionModel
import random
import copy

class ProfilerAlgorithmController:
    '''
    Description:
        Cette classe est le contrôleur d'algorithme avec l'annotation de profile

    Attributs:
        instance: (l'objet de la classe InstanceModel) l'instance préparée par la classe InstanceControleur,y compris
                  la liste de bâtiments，la liste de cares, la liste de phéromones sur les nœuds de bâtiment, la matrice
                  de phéromones sur les arcs entre le bâtiment et le care，la liste de fourmis
        bestSolution: (l'objet de la classe SolutionModel) la meilleure solution trouvé finalement
        careEffectRadius: (int) le rayon d'attraction initial de cercle dont le centre est chaque care
        bestQualityOfSolutionForEachIterationList: (float[]) la liste de qualités de meilleure solution de chaque itération
        averageQualityOfSolutionForEachIterationList: (float[]) la liste de qualités moyenne des soltuons de chaque itération
        distanceTotalOfBestSolutionForEachIterationList: (float[]) la liste de distance totale de la meilleure solution de chaque itération
        populationAllocatedOfBestSolutionForEachIterationList: (float[]) la liste de sans-abris totaux hébergés de la meilleure solution de chaque itération
        buildingAllocatedOfBestSolutionForEachIterationList: (float[]) la liste de nombre de bâtiments affectés de la meilleure solution de chaque itération
    '''

    def __init__(self, instance, careEffectRadius):
        '''
        Description:
            cette méthode est le constructeur de la classe AlgorithmeControlleur

        :param instance: (l'objet de la classe InstanceModel) l'instance de
                          programme,qui est préparée par la classe InstanceControleur
        :param careEffectRadius: (int) le rayon d'attraction initial de chaque care, qui
                                  est définit par l'utilisateur dans le script main.py
        '''

        self.instance = instance  # (l'objet de la classe InstanceModel) l'instance préparée par la classe InstanceControleur
        self.bestSolution = SolutionModel()  # (l'objet de la classe SolutionModel) la meilleure solution trouvé finalement
        self.careEffectRadius = careEffectRadius  # (int) le rayon d'attraction initial de circle dont le centre est chaque care
        self.bestQualityOfSolutionForEachIterationList = []  # (float[]) la liste de qualités de meilleure solution de chaque itération
        self.averageQualityOfSolutionForEachIterationList = []  # (float[]) la liste de qualités moyenne des soltuons de chaque itération
        self.distanceTotalOfBestSolutionForEachIterationList = []  # (float[]) la liste de distance totale de la meilleure solution de chaque itération
        self.populationAllocatedOfBestSolutionForEachIterationList = []  # (float[]) la liste de sans-abris totaux hébergés de la meilleure solution de chaque itération
        self.buildingAllocatedOfBestSolutionForEachIterationList = []  # (float[]) la liste de nombre de bâtiments affectés de la meilleure solution de chaque itération


    def run(self, iterationTimes):
        '''
        Description:
            Cette méthode est l'entrée de l'algorithme, et synthétise les solutions générée
            par chaque fourmi dans chaque itération, et obtenir la meilleure solution

        :param iterationTimes: (int) la fois d'itérations

        :return rien
        '''

        # (int[][]) La matrice d'indice de bâtiment dont la taille est len(listCare) * len(listBuilding)
        # pour chaque ligne (i.e. pour chaque care), les indices de bâtiment sont trie par l'ordre croissante en référant
        # les distances entre le care et chaque bâtiment, la format de cette matrice est la matrice transposée de la
        # matrice de distance
        distanceSortedBuildingIndexMatrix = self.sortBuildingIndexForEachCareInDistanceMatrix()

        bestSolutionForEachIterationList = []  # (SolutionModel[]) la liste de meilleure solution de chaque itération

        # commencer à faire l'itération
        iterationCounter = 0
        while iterationCounter < iterationTimes:
            solutionForOneIterationList = []  # (SolutionModel[]) la liste de solutions d'une itération
            qualityOfSolutionForOneIterationList = []  # (float[]) la liste de qualités de solution d'une itération

            allocateStartTime = time.time()  # enregistrer le temps de début où une itération d'affectation de bâtiment commence

            # les fourmis commencent à trouver sa solution
            for k, ant in enumerate(self.instance.antList):
                # (int [][]) le copie de la matrice d'indices trièes de bâtiment pour chaque care
                # parce que on ne peut pas modifier la matrice originale, il faut faire un copie profond
                copyDistanceSortedBuildingIndexMatrix = copy.deepcopy(distanceSortedBuildingIndexMatrix)

                # appeler la méthode ＂self.allocateBuilding＂ pour affecter les bâtiments
                self.allocateBuilding(ant, copyDistanceSortedBuildingIndexMatrix, solutionForOneIterationList,
                                      qualityOfSolutionForOneIterationList)

            # (Solution) chercher la meilleure solution parmis les solutions generèe par chaque fourmi dans une itération
            bestSolutionIndexForOneIteration = qualityOfSolutionForOneIterationList.index(
                max(qualityOfSolutionForOneIterationList))
            # ajouter la qualité de meilleure solution trouvée dans l'itération actuelle dans la liste "bestQualityOfSolutionForEachIterationList"
            self.bestQualityOfSolutionForEachIterationList.append(max(qualityOfSolutionForOneIterationList))
            # ajouter la meilleure solution trouvée dans l'itération actuelle dans la liste ＂bestSolutionForEachIterationList＂
            bestSolutionForEachIterationList.append(solutionForOneIterationList[bestSolutionIndexForOneIteration])
            # calculer la qualité moyenne de solutions dans l'itération actuelle en appelant la méthode
            # "self.calculateAverageSolutionQualityForEachIteration", et l'ajouter dans la liste "averageQualityOfSolutionForEachIterationList"
            self.averageQualityOfSolutionForEachIterationList.append(
                self.calculateAverageSolutionQualityForEachIteration
                (qualityOfSolutionForOneIterationList))
            # calculer la distance totale de la meilleure solution d'iteration actuelle
            self.distanceTotalOfBestSolutionForEachIterationList.append(self.calculateDistanceTotalOfOneSolution
                                                                        (solutionForOneIterationList[
                                                                             bestSolutionIndexForOneIteration]))
            # calculer le nombre de sans-abris hébergés de la meilleure solution d'iteration actuelle
            self.populationAllocatedOfBestSolutionForEachIterationList.append(
                self.calculatePopulationAllocatedOfOneSolution
                (solutionForOneIterationList[bestSolutionIndexForOneIteration]))
            # calculer le nombre de bâtiments affectés de la meilleure solution d'iteration actuelle
            self.buildingAllocatedOfBestSolutionForEachIterationList.append(self.calculateBuildingAllocatedOfOneSolution
                                                                            (solutionForOneIterationList[
                                                                                 bestSolutionIndexForOneIteration]))

            allocateEndTime = time.time()  # enregistrer le temps de fin où une itération d'affectation de bâtiment finit
            print('Finishe one iteration of allocating buildings, it takes %ds' % (allocateEndTime - allocateStartTime))
            iterationCounter += 1

        # (int) chercher l'indice de meilleure solution finale parmis les meilleure solutions trouvées dans chaque itèration
        bestSolutionIndex = self.bestQualityOfSolutionForEachIterationList.index(
            max(self.bestQualityOfSolutionForEachIterationList))
        # trouver la meilleure solution finale selon l'indice "bestSolutionIndex"
        self.bestSolution = bestSolutionForEachIterationList[bestSolutionIndex]


    @profile
    def allocateBuilding(self, ant, copyDistanceSortedBuildingIndexMatrix, solutionForOneIterationList,
                         qualityOfSolutionForOneIterationList):
        '''
        Description:
            Cette méthode est pour sélectionner les bâtiments à affecter

        :param ant: (l'objet de la classe AntModel) un fourmi qui va chercher sa solution
        :param copyDistanceSortedBuildingIndexMatrix: (int[][]) la matrice copiée d'indices
                                                       de bâtiment référée la matrice de distance
        :param solutionForOneIterationList: (SolutionModel[]) la liste de solutions pour une itération
        :param qualityOfSolutionForOneIterationList: (float[]) la liste de qualités de solution pour une itération

        :return: rien
        '''

        ant.solution = SolutionModel()

        buildingToAllocateList = copy.deepcopy(self.instance.buildingList)  # (BuildingModel[]) la liste de bâtiments
        careToFillList = copy.deepcopy(self.instance.careList)  # (CareModel[]) la liste de care

        # (Boolean[]) la liste qui sert à marquer si le bâtiment est déjà affectè，les valeurs initiales sont "False"
        isBuildingSelectedList = [False] * len(buildingToAllocateList)
        # (Boolean[]) la liste qui sert à marquer si le care est déjà plein, les valeurs initiales sont "False"
        isCareFullList = [False] * len(careToFillList)
        # (int[]) la liste de rayon d'attraction de care, les valeurs initiales sont égales au rayon initiale
        radiusList = [self.careEffectRadius] * len(careToFillList)
        # (int[]) un solution, les éléments sont les indices de care, les valeurs initiales sont -1
        # Si la valeur est -1, ça veut dire que aucun care peut héberger ce bâtiment
        ant.solution.solutionArray = [-1] * len(buildingToAllocateList)

        probabilityCtrl = ProbabilityController()

        # construire la liste de candidat pour chaque care (le candidat est l'indice de bâtiment)
        print("Start to initialize candidate list for care...")
        candidateListForCare = [[]]
        j = 0
        while j < len(careToFillList):
            # prendre une colonne dans la matrice de distance originale
            # i.e. prendre la liste de distance entre le care actuel et chaque bâtiment
            originalDistanceColumn = [originalColumn[j] for originalColumn in self.instance.distanceMatrix]
            # prendre une ligne dans la matrice copiée d'indice de bâtiment
            # i.e. prendre la liste d'indice de bâtiments trié pour le care actuel
            sortedDistanceColumn = copyDistanceSortedBuildingIndexMatrix[j]

            i = 0
            while i < len(sortedDistanceColumn):
                # chercher un élément dans la liste "sortedDistanceColumn", parce que cette liste est déjà trié par l'ordre
                # croissante, on peut prendre l'élément directement sans la cherche
                minIndex = sortedDistanceColumn[i]
                # obtenir la distance selon l'indice trouvée dans la matrice de distance originale comme la valeur minimum
                minVar = originalDistanceColumn[minIndex]

                # si cette distance minimum est inférieure ou égale au rayon du care actuel, et si la taille de liste de
                # candidat est inférieure ou égale au 10 (on limite la taille maximum de liste de candidat est de 10)
                if minVar <= radiusList[j] and len(candidateListForCare[j]) <= 10:
                    # ajouter cette indice de bâtiment dans la liste de candidat de care actuel
                    candidateListForCare[j].append(minIndex)
                    # supprimer cette indice de bâtiment dans la liste copyDistanceSortedBuildingIndexMatrix[j]
                    copyDistanceSortedBuildingIndexMatrix[j].remove(minIndex)
                # si la taille de liste de candidat atteint 10, quitter le boucle
                if len(candidateListForCare[j]) >= 10:
                    break
                i += 1
            # si le care actuel n'est pas le dernier care, ajouter un liste dans la liste candidateListForCare et
            # passer au care suivant pour continuer à construire sa liste de candidat
            if j != len(careToFillList) - 1:
                candidateListForCare.append([])
            j += 1
        print('Finish initializing candidate list for care...')

        # commencer à affecter les bâtiments
        print('Start to allocate buildings...')
        step = 0
        careToFillIndexOfLastStep = -1  # (int) l'indice de care qui est sélectionné dans le pas précédent
        while step < len(buildingToAllocateList):
            # si c'est le premier pas ou aucun care est sélectionné dans le pas précédent, sélectionner un bâtiment au hasard
            if step == 0 or careToFillIndexOfLastStep == -1:
                buidlingToAllocateIndex = random.randint(0, len(buildingToAllocateList) - 1)
            # sinon, il faut calculer la probabilité de transition de bâtiment pour sélectionner un bâtiment
            else:
                # si la liste de candidat du care n'est pas vide
                if len(candidateListForCare[careToFillIndexOfLastStep]) != 0:
                    buildingProbabilityList = []  # la liste de probabilité de transition de chaque bâtiment
                    buildingIndexForProbabilityList = []  # la liste d'indices de bâtiment qui correspond à la liste buildingProbabilityList

                    print("batiment *******************************************")
                    # prendre les bâtiments à partir de la liste de candidat de care actuel
                    iCandidate = 0
                    while iCandidate < len(candidateListForCare[careToFillIndexOfLastStep]):
                        # obtenir l'indice de bâtiment i
                        i = candidateListForCare[careToFillIndexOfLastStep][iCandidate]
                        # si le bâtiment i n'est pas encore affecté, alors calculer sa probabilité de transition
                        if isBuildingSelectedList[i] == False:
                            eta = self.instance.pheromoneNodeList[i].eta
                            tau = self.instance.pheromoneNodeList[i].tau
                            # appeler la méthode "calculateProbability()" de la classe ProbabilityController pour
                            # calculer sa probabilité de déplacement
                            buildingProbability = probabilityCtrl.calculateProbability(eta, tau,
                                                                                       isBuildingSelectedList)
                            # ajouter sa probabilité de déplacement  dans la liste buildingProbabilityList
                            buildingProbabilityList.append(buildingProbability)
                            # ajouter son indice dans la liste buildingIndexForProbabilityList
                            buildingIndexForProbabilityList.append(i)
                        # sinon ( si le bâtiment i est déjà affecter à l'autre care), alors enlever le bâtiment i
                        # de la liste de candidat de care actuel
                        else:
                            candidateListForCare[careToFillIndexOfLastStep].remove(i)
                        iCandidate += 1
                    # si la liste buildingProbabilityList est vide, ça veut dire que tous les bâtiments dans la liste de
                    # candidat de care actuel sont déjà affecté
                    if len(buildingProbabilityList) == 0:
                        continue

                    print("batiment start")
                    print(buildingIndexForProbabilityList, buildingProbabilityList)
                    # appeler la méthode "generateProbability()" de la classe ProbabilityController pour choisir un bâtiment
                    # selon leurs probabilités de déplacement
                    buidlingToAllocateIndex = probabilityCtrl.generateProbability(buildingIndexForProbabilityList,
                                                                                  buildingProbabilityList)
                    # enlever le bâtiment［buidlingToAllocateIndex］ de la liste de candidat de care actuel
                    candidateListForCare[careToFillIndexOfLastStep].remove(buidlingToAllocateIndex)
                    print("batiment end")

                # sinon( si la liste de candidat de care actuel est vide), il faut agrandir son rayon et reremplir sa
                # liste de candidat
                else:
                    # le rayon de care actuel augmente 1000m
                    radiusList[careToFillIndexOfLastStep] += 1000

                    # mettre à jour la liste d'indices de bâtiment par rapport à la matrice de distance pour le care actuel,
                    # enlever les bâtiments qui sont déjà affectés
                    sortedDistanceColumn = copyDistanceSortedBuildingIndexMatrix[careToFillIndexOfLastStep]
                    for index in sortedDistanceColumn:
                        if isBuildingSelectedList[index] == True:
                            copyDistanceSortedBuildingIndexMatrix[careToFillIndexOfLastStep].remove(index)

                    # obtenir la liste de distance origine et la nouvelle liste d'indice de bâtiment
                    originalDistanceColumn = [originalColumn[careToFillIndexOfLastStep] for originalColumn in
                                              self.instance.distanceMatrix]
                    sortedDistanceColumn = copyDistanceSortedBuildingIndexMatrix[careToFillIndexOfLastStep]
                    # commencer à remplir la liste de candidat de care actuel
                    i = 0
                    while i < len(sortedDistanceColumn):
                        # chercher un élément dans la liste "sortedDistanceColumn", parce que cette liste est déjà trié
                        # par l'ordre croissante, on peut prendre l'élément directement sans la cherche
                        minIndex = sortedDistanceColumn[i]
                        # obtenir la distance selon l'indice trouvée dans la matrice de distance originale comme
                        # la valeur minimum
                        minVar = originalDistanceColumn[minIndex]

                        # si cette distance minimum est inférieure ou égale au rayon du care actuel, et si la taille
                        # de liste de candidat est inférieure ou égale au 10
                        if minVar <= radiusList[careToFillIndexOfLastStep] and len(
                                candidateListForCare[careToFillIndexOfLastStep]) <= 10:
                            # ajouter cette indice de bâtiment dans la liste de candidat de care actuel
                            candidateListForCare[careToFillIndexOfLastStep].append(minIndex)
                            # supprimer cette indice de bâtiment dans la liste copyDistanceSortedBuildingIndexMatrix[careToFillIndexOfLastSte]
                            copyDistanceSortedBuildingIndexMatrix[careToFillIndexOfLastStep].remove(minIndex)
                        # si la taille de liste de candidat atteint 10, quitter la boucle
                        if len(candidateListForCare[careToFillIndexOfLastStep]) >= 10:
                            break
                        i += 1
                    # quitter cette boucle après mettre à jour la liste de candidat
                    continue

            # appeler la méthode "chooseCare" pour sélectionner un care et savoir si tous les cares sont pleins
            isAllCareFull, careToFillIndex = self.chooseCare(buidlingToAllocateIndex, buildingToAllocateList,
                                                             careToFillList, isCareFullList, ant.solution)

            # si un care est sélectionné dans le pas actuel
            if careToFillIndex != -1:
                # mettre à jour careToFillIndexOfLastStep
                careToFillIndexOfLastStep = careToFillIndex

                # mettre à jours la phéromone déposée sur les nœuds de bâtiment
                rho = self.instance.pheromoneNodeList[buidlingToAllocateIndex].rho
                deltaTau = rho * self.objectiveFunctionG(
                    ant.solution)  # multiplication car G(x) est une fonction à maximiser
                tau = self.instance.pheromoneNodeList[buidlingToAllocateIndex].tau
                self.instance.pheromoneNodeList[buidlingToAllocateIndex].deltaTau = deltaTau
                self.instance.pheromoneNodeList[buidlingToAllocateIndex].tau = (1 - rho) * tau + deltaTau
            # marquer que le bâtiment[buidlingToAllocateIndex] est déjà affecté ou aucun care ne peut pas l'héberger
            isBuildingSelectedList[buidlingToAllocateIndex] = True

            # si tous les cares sont pleins, quitter la boucle globale, cette fourmi trouve sa solution dans cette itération
            if isAllCareFull == True:
                break
            step += 1

        # calculer la qualité de solution trouvée (Q = G(x)/(1+F(x))) ou (Q = H(x)/(1+F(x))
        ant.solution.quality = self.objectiveFunctionG(ant.solution) / (1 + self.objectiveFunctionF(ant.solution))
        # ajouter la qualité calculée dans la liste qualityOfSolutionForOneIterationList
        qualityOfSolutionForOneIterationList.append(ant.solution.quality)
        # ajouter la solution dans la liste solutionForOneIterationList
        solutionForOneIterationList.append(ant.solution)


    @profile
    def chooseCare(self, buidlingToAllocateIndex, buildingToAllocateList, careToFillList, isCareFullList, solution):
        '''
        Description:
            Cette méthode est pour sélectionner les cares à remplir

        :param buidlingToAllocateIndex: (int) l'indice de bâtiment sélectionné
        :param buildingToAllocateList: (BuildingModel[]) la liste de bâtiments
        :param careToFillList: (CareModel[]) la liste de care
        :param isCareFullList: (Boolean[]) la liste qui marque si le care est plein
        :param solution: (l'objet de la classe SolutionModel) la solution
        :return: (boolean) une variable booléen qui signifie si tous les cares sont pleins

        :return: careToFillIndex: (int) l'indice de care sélectionné
        '''

        careProbabilityList = []  # la liste de probabilité de déplacement  de chaque care
        careIndexForProbabilityList = []  # la liste d'indices de bâtiment qui correspond à la liste careProbabilityList

        allowedCareLenght = len(careToFillList)  # (int) le nombre de cares qui sont encore dispobibles

        probabilityCtrl = ProbabilityController()

        # prendre chaque care
        j = 0
        while j < len(careToFillList):
            # si la population de bâtiment est inférieur ou égale à la capacité de care， et ce care n'est pas plein
            if buildingToAllocateList[buidlingToAllocateIndex].population <= careToFillList[j].capacity and \
                            isCareFullList[j] == False:
                eta = self.instance.pheromoneEdgeMatrix[buidlingToAllocateIndex][j].eta
                tau = self.instance.pheromoneEdgeMatrix[buidlingToAllocateIndex][j].tau
                # appeler la méthode "calculateProbability()" de la classe ProbabilityController pour
                # calculer la probabilité de déplacement  de care[j]
                careProbability = probabilityCtrl.calculateProbability(eta, tau, isCareFullList)
                # ajouter sa probabilité de déplacement  dans la liste careProbabilityList
                careProbabilityList.append(careProbability)
                # ajouter son indice dans la liste careIndexForProbabilityList
                careIndexForProbabilityList.append(j)
            j += 1

        # s'il existe un care qui peut héberger ce bâtiment
        if len(careProbabilityList) != 0:
            # appeler la méthode "generateProbability()" de la classe ProbabilityController pour choisir un care
            # selon leurs probabilités de déplacement
            careToFillIndex = probabilityCtrl.generateProbability(careIndexForProbabilityList, careProbabilityList)
            # ajouter l'indice de care dans la solution
            solution.solutionArray[buidlingToAllocateIndex] = careToFillIndex

            # mettre à jour la phéromone déposée sur
            rho = self.instance.pheromoneEdgeMatrix[buidlingToAllocateIndex][careToFillIndex].rho
            deltaTau = rho / self.objectiveFunctionF(solution)  # division car F(x) est une fonction à minimiser
            tau = self.instance.pheromoneEdgeMatrix[buidlingToAllocateIndex][careToFillIndex].tau
            self.instance.pheromoneEdgeMatrix[buidlingToAllocateIndex][careToFillIndex].deltaTau = deltaTau
            self.instance.pheromoneEdgeMatrix[buidlingToAllocateIndex][careToFillIndex].tau = (1 - rho) * tau + deltaTau

            # mettre à jour la capacité de care sélectionné
            careToFillList[careToFillIndex].capacity = careToFillList[careToFillIndex].capacity - \
                                                       buildingToAllocateList[buidlingToAllocateIndex].population
            print(careToFillIndex, buidlingToAllocateIndex, careToFillList[careToFillIndex].capacity)
            # vérifier si la capacité de care sélectionné est plein
            # i.e. si sa capacité peut héberger le bâtiment dont la population est minimum
            populationList = []

            # chercher les populations de bâtiments non-affectés
            i = 0
            while i < len(buildingToAllocateList):
                # si le care affecté au bâtiment i est -1, ça veut dire que le bâtiment i n'est pas affecté
                if solution.solutionArray[i] == -1:
                    populationList.append(buildingToAllocateList[i].population)
                i += 1

            # si la liste populationList est vide, ça veut dire que tous les bâtiments sont déjà affecté
            if len(populationList) == 0:
                return True, careToFillIndex
            # sinon, il reste des bâtiments non-affectés
            else:
                # chercher la population minumum
                minPopulation = min(populationList)
                # si la capacité de care sélectionné est inférieur à la population minimum
                if careToFillList[careToFillIndex].capacity < minPopulation:
                    # marquer que ce care est déjà plein
                    isCareFullList[careToFillIndex] = True
                    # le nombre de cares disponibles - 1
                    allowedCareLenght -= 1
        # si tous les cares ne peuvent pas héberger ce bâtiment
        else:
            # mettre l'indice de care pour ce bâtiment en -1
            careToFillIndex = -1

        # si le nombre de cares diponible est de 0, tous les care sont plein
        if allowedCareLenght == 0:
            return True, careToFillIndex
        # sinon, il reste des cares disponbles
        else:
            return False, careToFillIndex


    def sortBuildingIndexForEachCareInDistanceMatrix(self):
        '''
        Description:
            Cette méthode est pour trier les indices de bâtiments
            pour chaque care en référant la matrice de distance

        :return: distanceSortedBuildingIndexMatrix: (int[][]) la matrice de indices de bâtiments triés
        '''

        print('Start to sort distance...')
        sortStartTime = time.time()

        # copier la matrice de distance
        copiedDistanceMatrix = copy.deepcopy(self.instance.distanceMatrix)

        # créer la matrice d'indice de bâtiment triée
        distanceSortedBuildingIndexMatrix = [list(range(0, len(self.instance.distanceMatrix)))] * len(
            self.instance.distanceMatrix[0])

        # construire la matrice d'indice de bâtiment triée
        indexCare = 0
        while indexCare < len(copiedDistanceMatrix[0]):
            sortOneColumnStartTime = time.time()
            print("Sort buildings for %dth care..." % (indexCare + 1))
            # prendre une colonne dans la matrice de distance
            distanceColumn = [column[indexCare] for column in copiedDistanceMatrix]
            # prendre une ligne dans la matrice d'indice de bâtiment triée
            distanceIndexRow = copy.copy(distanceSortedBuildingIndexMatrix[indexCare])

            # appeler la méthode "merge_sort" pour faire le tri
            distanceColumn, distanceIndexRow = self.mergeSort(distanceColumn, distanceIndexRow)
            # mettre à jour la ligne triée dans la matrice distanceSortedBuildingIndexMatrix
            distanceSortedBuildingIndexMatrix[indexCare] = distanceIndexRow
            sortOneColumnEndTime = time.time()
            print("Finish sorting for %dth care, it tackes %ds" % (
                indexCare + 1, sortOneColumnEndTime - sortOneColumnStartTime))
            indexCare += 1

        sortEndTime = time.time()
        print('Finish solving the problem, it takes %d s!\n\n' % (sortEndTime - sortStartTime))

        return distanceSortedBuildingIndexMatrix


    def mergeSort(self, distanceList, distanceIndexList):
        '''
        Description:
            Cette méthode est pour trier une liste d'indice de bâtiments
            en référant la matrice de distance avec la trie par fusion

        :param distanceList: (float[]) la liste de distance à référer
        :param distanceIndexList: (int[]) la liste d'indice de bâtiment à trier

        :return: result: (float[]) la liste de distances triées
        :return: resultIndex: (int[]) la liste d'indices de bâtiments triées
        '''

        # si la taille liste distanceList est 1 après la division, retourner les deux liste
        if len(distanceList) <= 1:
            return distanceList, distanceIndexList

        # respectivent diviser les deux liste en deux sous-liste
        num = int(len(distanceList) / 2)
        left, leftIndex = self.mergeSort(distanceList[:num], distanceIndexList[:num])
        right, rightIndex = self.mergeSort(distanceList[num:], distanceIndexList[num:])

        # faire le tri
        i, j = 0, 0
        result = []
        resultIndex = []
        while i < len(left) and j < len(right):
            # si l'élément de la sous-liste gauche est inférieur ou égale à l'élément de la sous-liste droite
            if left[i] <= right[j]:
                # ajouter l'élément de la sous-liste gauche dans la liste resultat
                result.append(left[i])
                resultIndex.append(leftIndex[i])
                i += 1
            # si l'élément de la sous-liste gauche est supérieur à l'élément de la sous-liste droite
            else:
                # ajouter l'élément de la sous-liste droite dans la liste resultat
                result.append(right[j])
                resultIndex.append(rightIndex[j])
                j += 1

        # fusionner les deux sous-liste de distanceList en une liste entière
        result += left[i:]
        result += right[j:]

        # fusionner les deux sous-liste de distanceIndexList en une liste entière
        resultIndex += leftIndex[i:]
        resultIndex += rightIndex[j:]

        return result, resultIndex


    def objectiveFunctionF(self, solution):
        '''
        Description:
            Cette méthode est pour réaliser la fonction objective f(x)

        :param solution: (l'object de la classe SolutionModel) une solution

        :return: fx: (float) la valeur calculée de f(x)
        '''

        solutionArray = solution.solutionArray

        # obtenir les valeurs de décision x[i][j]
        i = 0
        x = [[0] * len(self.instance.careList) for row in range(len(self.instance.buildingList))]
        while i < len(solutionArray):
            if solutionArray[i] != -1:
                j = solutionArray[i]
                x[i][j] = 1
            i += 1

        # calculer sum(population[i]*x[i][j]*dist[i][j]) avec i de 1 à n et j de 1 à m
        i = 0
        fx = 0
        while i < len(self.instance.buildingList):
            j = 0
            while j < len(self.instance.careList):
                fx += self.instance.buildingList[i].population * x[i][j] * self.instance.distanceMatrix[i][j]
                j += 1
            i += 1

        return fx


    def objectiveFunctionG(self, solution):
        '''
        Description:
            Cette méthode est pour réaliser la fonction objective g(x)

        :param solution: (l'object de la classe SolutionModel) une solution

        :return: gx: (float) la valeur calculée de g(x)
        '''

        solutionArray = solution.solutionArray

        # obtenir les valeurs de décision x[i][j]
        i = 0
        x = [[0] * len(self.instance.careList) for row in range(len(self.instance.buildingList))]
        while i < len(solutionArray):
            if solutionArray[i] != -1:
                j = solutionArray[i]
                x[i][j] = 1
            i += 1

        # calculer sum(population[i]*x[i][j]) avec i de 1 à n et j de 1 à m
        i = 0
        gx = 0
        while i < len(self.instance.buildingList):
            j = 0
            while j < len(self.instance.careList):
                gx += self.instance.buildingList[i].population * x[i][j]
                j += 1
            i += 1

        return gx


    def objectiveFunctionH(self, solution):
        '''
        Description:
            Cette méthode est pour réaliser la fonction objective h(x)

        :param solution: (l'object de la classe SolutionModel) une solution

        :return: h(x): (float) la valeur calculée de h(x)
        '''

        solutionArray = solution.solutionArray

        # obtenir les valeurs de décision x[i][j]
        i = 0
        x = [[0] * len(self.instance.careList) for row in range(len(self.instance.buildingList))]
        while i < len(solutionArray):
            if solutionArray[i] != -1:
                j = solutionArray[i]
                x[i][j] = 1
            i += 1

        # calculer sum(x[i][j]) avec i de 1 à n et j de 1 à m
        i = 0
        hx = 0
        while i < len(self.instance.buildingList):
            j = 0
            while j < len(self.instance.careList):
                hx += x[i][j]
                j += 1
            i += 1

        return hx


    def calculateAverageSolutionQualityForEachIteration(self, qualityOfSolutionForOneIterationList):
        '''
        Description:
            Cette méthode est pour calculer la qualité moyenne des
            solutions générées par chaque fourmi dans une itération

        :param qualityOfSolutionForOneIterationList: (float[]) la liste de qualités de chaque solution d'une itération

        :return: average: (float) la qualité moyenne des solutions
        '''

        sum = 0.00
        for k in range(len(self.instance.antList)):
            sum += qualityOfSolutionForOneIterationList[k]
        average = sum / len(self.instance.antList)

        return average


    def calculateDistanceTotalOfOneSolution(self, oneSolution):
        '''
        Description:
            Cette méthode est pour calculer la distance totale d'une solution

        :param oneSolution: (l'objet de la classe SolutionModel) une solution

        :return: distanceTotal: (float) la distance totale calculée d'une solution
        '''

        solution = oneSolution.solutionArray

        i = 0
        distanceTotal = 0
        while i < len(solution):
            j = solution[i]
            # si l'indice de care qui héberge le bâtiment i n'est pas -1
            if j != -1:
                distanceTotal += self.instance.distanceMatrix[i][j]
            i += 1

        return distanceTotal


    def calculatePopulationAllocatedOfOneSolution(self, oneSolution):
        '''
        Description:
            Cette méthode est pour calculer le nombre de sans-abris hébergés d'une solution

        :param oneSolution: (l'objet de la classe SolutionModel) une solution

        :return: populationAllocated: (float) le nombre de sans-abris hébergés d'une solution
        '''

        solution = oneSolution.solutionArray

        i = 0
        populationAllocated = 0
        while i < len(solution):
            j = solution[i]
            # si l'indice de care qui héberge le bâtiment i n'est pas -1
            if j != -1:
                populationAllocated += self.instance.buildingList[i].population
            i += 1

        return populationAllocated


    def calculateBuildingAllocatedOfOneSolution(self, oneSolution):
        '''
        Description:
            Cette méthode est pour calculer le nombre de bâtiments affectés d'une solution

        :param oneSolution: (l'objet de la classe SolutionModel) une solution

        :return: buildingAllocated: (int) le nombre de bâtiments affectés d'une solution
        '''

        solution = oneSolution.solutionArray

        i = 0
        buildingAllocated = 0
        while i < len(solution):
            j = solution[i]
            # si l'indice de care qui héberge le bâtiment i n'est pas -1
            if j != -1:
                buildingAllocated += 1
            i += 1

        return buildingAllocated