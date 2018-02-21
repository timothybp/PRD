import random

from controllers.ProbabilityController import ProbabilityController

# Cette classe est pour contrôler l'algorithme
class AlgorithmController:

    def __init__(self,fileCtrl):
        self.probaCtrl = ProbabilityController()    # L'objet de la classe "ProbabilityController"
        self.fileCtrl = fileCtrl    # L'objet de la classe "FileController"
        self.bestSolutionList = []  # La liste de meilleure solution de chaque itération
        self.bestQualityList = []   # La liste de quitté de chaque meilleure solution en utilisant les fonctions objectives

    # Cette méthode est pour affecter les sans-abris
    # Param : nbIteration : le nombre d'itération
    # Param : antList : la liste de fourmis
    # Param : rayon : la rayon initial de circles dont les contres sont chaque care
    # Return : la meilleure solution
    def allocateBuilding(self,nbIteration,antList, rayon):
        iterationCounter = 0
        while iterationCounter < nbIteration:
            oneIterationSolutionList = []   # La meilleure solution d'une itération
            oneIterationQuantityList = []   # La qualité de meilleur solution d'une itération
            k = 0
            while k < len(antList):

                buildingToAllocateList = self.fileCtrl.buildingList.copy()
                careToFillList = self.fileCtrl.careList.copy()
                isBuildingSelected = [0] * len(buildingToAllocateList)
                antList[k].solution =  [-1] * len(buildingToAllocateList)

                rayonList = [rayon]*len(careToFillList)
                idCareToFill = -1
                candidateList = [[]]

                print("start to build candidate list")
                j = 0
                while j < len(careToFillList):

                    # Construire la liste de candidat de chaque care
                    v = [x[j] for x in self.fileCtrl.distanceMatrix]
                    counter = 0
                    while counter < len(v):
                        minVar = min(v)
                        i = v.index(minVar)
                        if minVar <= rayonList[j] and len(candidateList[j]) < 10:
                            candidateList[j].append(i)
                            v[i] = 99999    # Changer cette valeur minimum en une valeur maximum
                        if len(candidateList[j]) >= 10:
                            break
                        counter += 1
                    candidateList.append([])
                    j += 1

                step = 0
                while step < len(buildingToAllocateList):
                    if step == 0:   # Si c'est le première pas, sélectionner un bâtiment au hasard
                        idBuidlingToAllocate = random.randint(0, len(buildingToAllocateList) - 1)
                    else:   # Sinon, calculer les probabilités de déplacements parmi les bâtiment dans la liste de candidat de care actuel
                        if len(candidateList[idCareToFill]) != 0:   # Si la liste de candidat du care actuel n'est pas vide
                            buildingProbabilityList = []
                            idbuildingProbabilityList = []
                            iCandidate = 0
                            print("batiment ****************************************8")
                            while iCandidate < len(candidateList[idCareToFill]):
                                i = candidateList[idCareToFill][iCandidate]
                                if isBuildingSelected[i] != 1:
                                    eta = self.fileCtrl.pheromoneNodeList[i].eta
                                    tau = self.fileCtrl.pheromoneNodeList[i].tau
                                    buildingProbability = self.probaCtrl.calculateProbability(eta, tau, isBuildingSelected)
                                    buildingProbabilityList.append(buildingProbability)
                                    idbuildingProbabilityList.append(i)
                                else:
                                    candidateList[idCareToFill].remove(i)
                                iCandidate += 1
                            if len(buildingProbabilityList) == 0:   # Si la liste de probabilité est vide, quitter la boucle actuel
                                continue
                            print("batiment start")
                            print(idbuildingProbabilityList,buildingProbabilityList)
                            idBuidlingToAllocate = self.probaCtrl.generateProbability(idbuildingProbabilityList,buildingProbabilityList)
                            print("batiment end")
                            candidateList[idCareToFill].remove(idBuidlingToAllocate)
                        else:   # Si la liste de candidat de care actuel est vide, agrandir le rayon de cette care
                            print("enlarge cadidate list ....")
                            if len(candidateList[idCareToFill]) == 0:
                                print(rayonList[idCareToFill])
                                rayonList[idCareToFill] += 500  # le rayon de cette care augmente en 500m chaque fois
                            v = [x[idCareToFill] for x in self.fileCtrl.distanceMatrix]

                            isBuildSel = isBuildingSelected.copy()
                            varZeroList = []
                            indexZeroList = []
                            while 0 in isBuildSel:
                                indexZero = isBuildSel.index(0)
                                indexZeroList.append(indexZero)
                                varZeroList.append(v[indexZero])
                                isBuildSel[indexZero] = 1
                            counter = 0
                            while counter < len(varZeroList):
                                minVar = min(varZeroList)
                                minIndex = varZeroList.index(minVar)
                                i = indexZeroList[minIndex]
                                #print(minVar <= rayonList[idCareToFill], isBuildingSelected[i] != 1,
                                      #len(candidateList[idCareToFill]) <= 10)
                                if minVar <= rayonList[idCareToFill] and len(candidateList[idCareToFill]) < 10:
                                    candidateList[idCareToFill].append(i)
                                    varZeroList[minIndex] = 99999
                                print(i, len(candidateList[idCareToFill]))
                                if len(candidateList[idCareToFill]) == 0 or len(candidateList[idCareToFill]) >= 10:
                                    break
                                counter += 1
                            continue
                    # Choisir un care pour le bâtiment sélectionné
                    isAllCareFull, idCareToFill = self.chooseCare(idBuidlingToAllocate, buildingToAllocateList, careToFillList, antList[k].solution)
                    if idCareToFill != -1:  # Si le bâtiment peut être affecté à un care, mettre à jour le phéromone du nœud de ce bâtiment
                        rho = self.fileCtrl.pheromoneNodeList[idBuidlingToAllocate].rho
                        deltaTau =  rho * self.objectiveFunctionG(antList[k].solution)
                        tau = self.fileCtrl.pheromoneNodeList[idBuidlingToAllocate].tau
                        self.fileCtrl.pheromoneNodeList[idBuidlingToAllocate].deltaTau = deltaTau
                        self.fileCtrl.pheromoneNodeList[idBuidlingToAllocate].tau = (1 - rho) * tau + deltaTau
                    isBuildingSelected[idBuidlingToAllocate] = 1    # Marquer que ce bâtiment est déjà sélectionné
                    if isAllCareFull == True:   # Si tous les cares sont plein, quitter la boucle globale
                        break
                    step += 1

                # Ajouter les solutions générées par chaque fourmis pendant une itération dans une liste
                # Et calculer la quantité de chaque solution en utilisant g(x)/(1+f(x))
                oneIterationSolutionList.append(antList[k].solution)
                oneIterationQuantityList.append(self.objectiveFunctionG(antList[k].solution) / 1 + self.objectiveFunctionF(antList[k].solution))
                k += 1
            # Chercher la meilleure solution pendant une itération
            oneIterationBestSolutionIndex = oneIterationQuantityList.index(max(oneIterationQuantityList))
            self.bestSolutionList.append(oneIterationSolutionList[oneIterationBestSolutionIndex])
            self.bestQualityList.append(max(oneIterationQuantityList))
            iterationCounter += 1
        # Chercher la meilleure solution finale parmis les meilleures solutions générées de chaque itération
        bestSolutionIndex = self.bestQualityList.index(max(self.bestQualityList))
        return self.bestSolutionList[bestSolutionIndex]

    # Cette méthode est pour choisir un care pour un bâtiment sélectionné
    # Param : idBuildingToAllocate : L'identifiant de bâtiment à affecter
    # Param : buildingToAllocateList : La liste de bâtiment
    # Param : careToFillList : La liste de care
    # Param : arraySolution : la solution actuelle
    # Return : Un variable qui marque si tous les cares sont plein
    # Return : L'identifiant de care sélectionné
    def chooseCare(self,idBuidlingToAllocate, buildingToAllocateList, careToFillList, arraySolution):
        careProbabilityList = []
        idCareProbabilityList = []
        lengthAllowedCare = len(careToFillList)
        j = 0
        isCareFull = [0] * len(careToFillList)
        #calculer les probabilités de déplacements selon les distances entre le bâtiment à affecter et chaque care
        while j < len(careToFillList):
            if self.fileCtrl.buildingList[idBuidlingToAllocate].population < self.fileCtrl.careList[j].capacity and isCareFull[j] != 1:
                eta = self.fileCtrl.pheromoneEdgeMatrix[idBuidlingToAllocate][j].eta
                tau = self.fileCtrl.pheromoneEdgeMatrix[idBuidlingToAllocate][j].tau
                careProbability = self.probaCtrl.calculateProbability(eta,tau, isCareFull)
                careProbabilityList.append(careProbability)
                idCareProbabilityList.append(j)
            j += 1
        if len(careProbabilityList) != 0:   # Si la liste de probabilité n'est pas vide, modifier la solution
            print("care start")
            idCareToFill =  self.probaCtrl.generateProbability(idCareProbabilityList, careProbabilityList)
            print("care end")
            arraySolution[idBuidlingToAllocate] = idCareToFill

            # Mettre à jour la phéromone de l'arc entre le bâtiment actuel et le care sélectionné
            rho = self.fileCtrl.pheromoneEdgeMatrix[idBuidlingToAllocate][idCareToFill].rho
            deltaTau = rho / self.objectiveFunctionF(arraySolution)
            tau = self.fileCtrl.pheromoneEdgeMatrix[idBuidlingToAllocate][idCareToFill].tau
            self.fileCtrl.pheromoneEdgeMatrix[idBuidlingToAllocate][idCareToFill].deltaTau = deltaTau
            self.fileCtrl.pheromoneEdgeMatrix[idBuidlingToAllocate][idCareToFill].tau = (1 - rho) * tau + deltaTau

            populationList = []
            i = 0
            # Chercher le nombre de sans-abris minimum entre tous les bâtiments
            while i < len(buildingToAllocateList):
                if arraySolution[i] != -1:
                    populationList.append(buildingToAllocateList[i].population)
                i += 1
            careToFillList[idCareToFill].capacity -= buildingToAllocateList[idBuidlingToAllocate].population
            minPopulation = min(populationList)
            if careToFillList[idCareToFill].capacity < minPopulation:   # Si la capacité du care sélectionné < le nombre de sans-abris minimum
                isCareFull[idCareToFill] = 1    # Marquer que ce care est déjà plein
                lengthAllowedCare -= 1
        else:
            idCareToFill = -1
        if lengthAllowedCare == 0:
            return True,idCareToFill
        else:
            return False,idCareToFill

    # Cette méthode est pour réaliser la fonction objective f(x)
    # Param : arraySolution : Une solution
    # Return : la valeur calculée de f(x)
    def objectiveFunctionF(self, arraySolution):
        i = 0
        x = [[0] * len(self.fileCtrl.careList) for row in range(len(self.fileCtrl.buildingList))]
        while i < len(arraySolution):
            if arraySolution[i] != -1:
                j = arraySolution[i]
                x[i][j] = 1
            i += 1

        i = 0
        fx = 0
        while i < len(self.fileCtrl.buildingList):
            j = 0
            while j < len(self.fileCtrl.careList):
                fx += self.fileCtrl.buildingList[i].population * x[i][j] * self.fileCtrl.distanceMatrix[i][j]
                j += 1
            i += 1
        return fx

    # Cette méthode est pour réaliser la fonction objective g(x)
    # Param : arraySolution : Une solution
    # Return : la valeur calculée de g(x)
    def objectiveFunctionG(self, arraySolution):
        i = 0
        x = [[0] * len(self.fileCtrl.careList) for row in range(len(self.fileCtrl.buildingList))]
        while i < len(arraySolution):
            if arraySolution[i] != -1:
                j = arraySolution[i]
                x[i][j] = 1
            i += 1

        i = 0
        gx = 0
        while i < len(self.fileCtrl.buildingList):
            j = 0
            while j < len(self.fileCtrl.careList):
                gx += self.fileCtrl.buildingList[i].population * x[i][j]
                j += 1
            i += 1
        return gx

    # Cette méthode est pour réaliser la fonction objective h(x)
    # Param : arraySolution : Une solution
    # Return : la valeur calculée de h(x)
    def objectiveFunctionH(self, arraySolution):
        i = 0
        x = [[0] * len(self.fileCtrl.careList) for row in range(len(self.fileCtrl.buildingList))]
        while i < len(arraySolution):
            if arraySolution[i] != -1:
                j = arraySolution[i]
                x[i][j] = 1
            i += 1

        i = 0
        hx = 0
        while i < len(self.fileCtrl.buildingList):
            j = 0
            while j < len(self.fileCtrl.careList):
                hx += x[i][j]
                j += 1
            i += 1
        return hx