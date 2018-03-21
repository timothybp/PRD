import time
from controllers.ProbabilityController import ProbabilityController
from models.ant.SolutionModel import SolutionModel
import random
import copy

# Cette classe est pour contrôler l'algorithme
class AlgorithmController:

    def __init__(self, instance):
        self.instance = instance
        self.bestSolution = SolutionModel()  # La liste de meilleure solution de chaque itération

    def run(self, iterationTimes, careEffectRadius):
        distanceSortedBuildingIndexMatrix = self.sortBuildingIndexForEachCareInDistanceMatrix()
        bestSolutionForEachIterationList = []
        bestQualityOfSolutionForEachIterationList = []
        averageQualityOfSolutionForEachIterationList = []

        iterationCounter = 0
        while iterationCounter < iterationTimes:
            solutionForOneIterationList = []
            qualityOfSolutionForOneIterationList = []

            allocateStartTime = time.time()
            for k,ant in enumerate(self.instance.antList):
                ant.solution = SolutionModel()
                copyDistanceSortedBuildingIndexMatrix = copy.deepcopy(distanceSortedBuildingIndexMatrix)
                buildingToAllocateList = copy.deepcopy(self.instance.buildingList)
                careToFillList = copy.deepcopy(self.instance.careList)
                isBuildingSelectedList = [False] * len(buildingToAllocateList)
                isCareFullList = [False] * len(careToFillList)
                radiusList = [careEffectRadius] * len(careToFillList)
                ant.solution.solutionArray = [-1] * len(buildingToAllocateList)
                probabilityCtrl = ProbabilityController()

                print("iteration %d, ant %d" % (iterationCounter + 1, k + 1))
                print("Start to initialize candidate list...")
                candidateList = [[]]
                j = 0
                while j < len(careToFillList):
                    originalDistanceColumn = [originalColumn[j] for originalColumn in self.instance.distanceMatrix]
                    sortedDistanceColumn = copyDistanceSortedBuildingIndexMatrix[j]

                    i = 0
                    while i < len(sortedDistanceColumn):
                        minIndex = sortedDistanceColumn[i]
                        minVar = originalDistanceColumn[minIndex]
                        if minVar <= radiusList[j] and len(candidateList[j]) <= 10:
                            candidateList[j].append(minIndex)
                            copyDistanceSortedBuildingIndexMatrix[j].remove(minIndex)
                        if len(candidateList[j]) >= 10:
                            break
                        i += 1
                    if j != len(careToFillList) - 1:
                        candidateList.append([])
                    j += 1
                print('Finish initializing candidate list...')

                print('Start to allocate buildings...')

                step = 0
                careToFillIndexOfLastStep = -1
                while step < len(buildingToAllocateList):
                    if step == 0 or careToFillIndexOfLastStep == -1:  # 如果这是第一步或者上一步未选中安置点，就随机选一个楼房
                        buidlingToAllocateIndex = random.randint(0, len(buildingToAllocateList) - 1)
                    else:  # 如果不是第一步且之前选中了安置点，就需要计算转移概率
                        if len(candidateList[careToFillIndexOfLastStep]) != 0:  #如果该安置点的候选列表不为空
                            buildingProbabilityList = []
                            buildingIndexForProbabilityList = []
                            iCandidate = 0
                            print("batiment *******************************************")
                            while iCandidate < len(candidateList[careToFillIndexOfLastStep]):
                                i = candidateList[careToFillIndexOfLastStep][iCandidate]
                                if isBuildingSelectedList[i] == False:  #如果楼房i还没分配，就去计算概率
                                    eta = self.instance.pheromoneNodeList[i].eta
                                    tau = self.instance.pheromoneNodeList[i].tau
                                    buildingProbability = probabilityCtrl.calculateProbability(eta, tau,
                                                                                             isBuildingSelectedList)
                                    buildingProbabilityList.append(buildingProbability)
                                    buildingIndexForProbabilityList.append(i)
                                else:   #如果楼房i已经分配给其他的安置点，就从候选人列表中去掉
                                    candidateList[careToFillIndexOfLastStep].remove(i)
                                iCandidate += 1
                            if len(buildingProbabilityList) == 0:   #如果楼房的概率列表为空，即该安置点的候选列表里的楼房全都已经分配了
                                continue

                            print("batiment start")
                            print(buildingIndexForProbabilityList, buildingProbabilityList)
                            buidlingToAllocateIndex = probabilityCtrl.generateProbability(buildingIndexForProbabilityList, buildingProbabilityList)
                            candidateList[careToFillIndexOfLastStep].remove(buidlingToAllocateIndex)
                            print("batiment end")

                        else:   #如果该安置点的候选列表为空，则扩大半径后重新填充该安置点的候选列表
                            #扩大该安置点的半径
                            radiusList[careToFillIndexOfLastStep] += 1000
                            #更新该安置点的索引距离列表，去除已经分配的楼房的索引
                            sortedDistanceColumn = copyDistanceSortedBuildingIndexMatrix[careToFillIndexOfLastStep]
                            for index in sortedDistanceColumn:
                                if isBuildingSelectedList[index] == True:
                                    copyDistanceSortedBuildingIndexMatrix[careToFillIndexOfLastStep].remove(index)

                            #重新获取距离列表
                            originalDistanceColumn = [originalColumn[careToFillIndexOfLastStep] for originalColumn in
                                                      self.instance.distanceMatrix]
                            sortedDistanceColumn = copyDistanceSortedBuildingIndexMatrix[careToFillIndexOfLastStep]
                            i = 0
                            while i < len(sortedDistanceColumn):
                                minIndex = sortedDistanceColumn[i]
                                minVar = originalDistanceColumn[minIndex]
                                if minVar <= radiusList[careToFillIndexOfLastStep] and len(candidateList[careToFillIndexOfLastStep]) <= 10:
                                    candidateList[careToFillIndexOfLastStep].append(minIndex)
                                    copyDistanceSortedBuildingIndexMatrix[careToFillIndexOfLastStep].remove(minIndex)
                                if len(candidateList[careToFillIndexOfLastStep]) >= 10:
                                    break
                                i += 1
                            #更新完候选列表后直接退出本次循环
                            continue

                    isAllCareFull, careToFillIndex = self.chooseCare(buidlingToAllocateIndex, buildingToAllocateList,
                                                                     careToFillList, isCareFullList,
                                                                     ant.solution)

                    if careToFillIndex != -1:  # 如果本步选中了一个安置点
                        careToFillIndexOfLastStep = careToFillIndex
                        #更新信息素
                        rho = self.instance.pheromoneNodeList[buidlingToAllocateIndex].rho
                        deltaTau = rho * self.objectiveFunctionG(ant.solution)
                        tau = self.instance.pheromoneNodeList[buidlingToAllocateIndex].tau
                        self.instance.pheromoneNodeList[buidlingToAllocateIndex].deltaTau = deltaTau
                        self.instance.pheromoneNodeList[buidlingToAllocateIndex].tau = (1 - rho) * tau + deltaTau
                    isBuildingSelectedList[buidlingToAllocateIndex] = True  # 标记该房屋已选或者无法分配给任何一个安置点
                    if isAllCareFull == True:  # Si tous les cares sont plein, quitter la boucle globale
                        break
                    step += 1

                ant.solution.quality = self.objectiveFunctionG(ant.solution) / (1 + self.objectiveFunctionF(ant.solution))
                qualityOfSolutionForOneIterationList.append(ant.solution.quality)
                solutionForOneIterationList.append(ant.solution)

            bestSolutionIndexForOneIteration = qualityOfSolutionForOneIterationList.index(max(qualityOfSolutionForOneIterationList))
            bestQualityOfSolutionForEachIterationList.append(max(qualityOfSolutionForOneIterationList))
            bestSolutionForEachIterationList.append(solutionForOneIterationList[bestSolutionIndexForOneIteration])
            averageQualityOfSolutionForEachIterationList.append(self.calculateAverageSolutionQualityForEachIteration(qualityOfSolutionForOneIterationList))
            allocateEndTime = time.time()
            print('Finishe one iteration of allocating buildings, it takes %ds' % (allocateEndTime - allocateStartTime))
            iterationCounter += 1

        bestSolutionIndex = bestQualityOfSolutionForEachIterationList.index(max(bestQualityOfSolutionForEachIterationList))
        self.bestSolution = bestSolutionForEachIterationList[bestSolutionIndex]
        return bestQualityOfSolutionForEachIterationList, averageQualityOfSolutionForEachIterationList

    def chooseCare(self, buidlingToAllocateIndex, buildingToAllocateList, careToFillList, isCareFullList, solution):
        careProbabilityList = []
        careIndexForProbabilityList = []
        allowedCareLenght = len(careToFillList)
        probabilityCtrl = ProbabilityController()

        #开始构建这个楼房与所有安置点的概率列表
        j = 0
        while j < len(careToFillList):
            #如果这个楼房中的人数小于安置点j的容量，并且安置点j未满
            if self.instance.buildingList[buidlingToAllocateIndex].population <= self.instance.careList[j].capacity and isCareFullList[j] == False:
                eta = self.instance.pheromoneEdgeMatrix[buidlingToAllocateIndex][j].eta
                tau = self.instance.pheromoneEdgeMatrix[buidlingToAllocateIndex][j].tau
                careProbability = probabilityCtrl.calculateProbability(eta, tau, isCareFullList)
                careProbabilityList.append(careProbability)
                careIndexForProbabilityList.append(j)
            j += 1

        if len(careProbabilityList) != 0:   #如果存在安置点可以容纳该楼房
            careToFillIndex = probabilityCtrl.generateProbability(careIndexForProbabilityList, careProbabilityList)
            solution.solutionArray[buidlingToAllocateIndex] = careToFillIndex

            #更新信息素
            rho = self.instance.pheromoneEdgeMatrix[buidlingToAllocateIndex][careToFillIndex].rho
            deltaTau = rho / self.objectiveFunctionF(solution)
            tau = self.instance.pheromoneEdgeMatrix[buidlingToAllocateIndex][careToFillIndex].tau
            self.instance.pheromoneEdgeMatrix[buidlingToAllocateIndex][careToFillIndex].deltaTau = deltaTau
            self.instance.pheromoneEdgeMatrix[buidlingToAllocateIndex][careToFillIndex].tau = (1 - rho) * tau + deltaTau

            #更新安置点容量
            careToFillList[careToFillIndex].capacity -= buildingToAllocateList[buidlingToAllocateIndex].population

            #判断该安置点的剩余容量是否可以容纳人数最小的楼
            populationList = []
            i = 0
            while i < len(buildingToAllocateList):  #找出尚未分配的楼房的人口数
                if solution.solutionArray[i] == -1:
                    populationList.append(buildingToAllocateList[i].population)
                i += 1
            if len(populationList) == 0:
                return True, careToFillIndex
            else:
                minPopulation = min(populationList)
                if careToFillList[careToFillIndex].capacity < minPopulation:    #如果改安置点的剩余容量比人口数量最少的楼的人数还小
                    isCareFullList[careToFillIndex] = True #将该安置点标记为已满
                    allowedCareLenght -= 1
        else:   #如果所有安置点都无法容纳该楼房
            careToFillIndex = -1

        if allowedCareLenght == 0:
            return True,careToFillIndex
        else:
            return False,careToFillIndex


    def sortBuildingIndexForEachCareInDistanceMatrix(self):
        print('Start to sort distance...')
        sortStartTime = time.time()
        copiedDistanceMatrix = copy.deepcopy(self.instance.distanceMatrix)
        distanceSortedBuildingIndexMatrix = [list(range(0, len(self.instance.buildingList)))] * len(self.instance.careList)

        indexCare = 0
        while indexCare < len(copiedDistanceMatrix[0]):
            sortOneColumnStartTime = time.time()
            print("Sort buildings for %dth care..." % (indexCare + 1))
            distanceColumn = [column[indexCare] for column in copiedDistanceMatrix]
            distanceIndexRow = copy.deepcopy(distanceSortedBuildingIndexMatrix[indexCare])
            distanceColumn, distanceIndexRow = self.merge_sort(distanceColumn, distanceIndexRow)
            distanceSortedBuildingIndexMatrix[indexCare] = distanceIndexRow
            sortOneColumnEndTime = time.time()
            print("Finish sorting for %dth care, it tackes %ds" % (
                indexCare + 1, sortOneColumnEndTime - sortOneColumnStartTime))
            indexCare += 1

        sortEndTime = time.time()
        print('Finish solving the problem, it takes %d s!\n\n' % (sortEndTime - sortStartTime))

        return distanceSortedBuildingIndexMatrix

    # 归并排序
    def merge_sort(self, distanceColumn, distanceIndexRow):
        if len(distanceColumn) <= 1:
            return distanceColumn, distanceIndexRow
        middle = int(len(distanceColumn) / 2)
        left, leftIndex = self.merge_sort(distanceColumn[:middle], distanceIndexRow[:middle])
        right, rightIndex = self.merge_sort(distanceColumn[middle:], distanceIndexRow[middle:])
        i, j = 0, 0
        result = []
        resultIndex = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                resultIndex.append(leftIndex[i])
                i += 1
            else:
                result.append(right[j])
                resultIndex.append(rightIndex[j])
                j += 1
        result += left[i:]
        result += right[j:]
        resultIndex += leftIndex[i:]
        resultIndex += rightIndex[j:]

        return result, resultIndex

    # Cette méthode est pour réaliser la fonction objective f(x)
    # Param : solution : Une solution
    # Return : la valeur calculée de f(x)
    def objectiveFunctionF(self, solution):
        solutionArray = solution.solutionArray
        i = 0
        x = [[0] * len(self.instance.careList) for row in range(len(self.instance.buildingList))]
        while i < len(solutionArray):
            if solutionArray[i] != -1:
                j = solutionArray[i]
                x[i][j] = 1
            i += 1

        i = 0
        fx = 0
        while i < len(self.instance.buildingList):
            j = 0
            while j < len(self.instance.careList):
                fx += self.instance.buildingList[i].population * x[i][j] * self.instance.distanceMatrix[i][j]
                j += 1
            i += 1
        return fx

    # Cette méthode est pour réaliser la fonction objective g(x)
    # Param : solution : Une solution
    # Return : la valeur calculée de g(x)
    def objectiveFunctionG(self, solution):
        solutionArray = solution.solutionArray
        i = 0
        x = [[0] * len(self.instance.careList) for row in range(len(self.instance.buildingList))]
        while i < len(solutionArray):
            if solutionArray[i] != -1:
                j = solutionArray[i]
                x[i][j] = 1
            i += 1

        i = 0
        gx = 0
        while i < len(self.instance.buildingList):
            j = 0
            while j < len(self.instance.careList):
                gx += self.instance.buildingList[i].population * x[i][j]
                j += 1
            i += 1
        return gx

    # Cette méthode est pour réaliser la fonction objective h(x)
    # Param : solution : Une solution
    # Return : la valeur calculée de h(x)
    def objectiveFunctionH(self, solution):
        solutionArray = solution.solutionArray
        i = 0
        x = [[0] * len(self.instance.careList) for row in range(len(self.instance.buildingList))]
        while i < len(solutionArray):
            if solutionArray[i] != -1:
                j = solutionArray[i]
                x[i][j] = 1
            i += 1

        i = 0
        hx = 0
        while i < len(self.instance.buildingList):
            j = 0
            while j < len(self.instance.careList):
                hx += x[i][j]
                j += 1
            i += 1
        return hx

    def calculateAverageSolutionQualityForEachIteration(self,qualityOfSolutionForOneIterationList):
        sum = 0.00
        for k in range(len(self.instance.antList)):
            sum += qualityOfSolutionForOneIterationList[k]
        average = sum / len(self.instance.antList)
        return average