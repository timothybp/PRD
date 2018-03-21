class FileController:

    def readBuildingFile(self,buildingFilename):
        buildingContentList = []
        counter = 0
        with open(buildingFilename, 'rt') as buildings:
            for building in buildings:
                if counter != 0:
                    buildingContentList.append(building)
                counter += 1
        print('Finish reading builidng file...')
        return buildingContentList


    def readCareFile(self, careFilename):
        careContentList = []
        counter = 0
        with open(careFilename, 'rt') as cares:
            for care in cares:
                if counter != 0:
                    careContentList.append(care)
                counter += 1
        print('Finish reading care file...')
        return careContentList


    def readDistanceFile(self, distanceFilename):
        distanceContentList = []
        counter = 0
        with open(distanceFilename, 'rt') as distances:
            for distance in distances:
                if counter != 0:
                    distanceContentList.append(distance)
                counter += 1
        print('Finish reading distance file...')
        return distanceContentList


    def writeSolutionFile(self, solutionFilename, bestSolution, instance):
        solution = bestSolution.solutionArray
        with open(solutionFilename, 'wt') as result:
            i = 0
            strToWrite = 'ID_BAT\tID_CARE\n'
            while i < len(solution):
                if str(solution[i]) != '-1':
                    indexCare = int(solution[i])
                    idCare = str(instance.careList[indexCare].idCare)
                else:
                    idCare = str(-1)
                idBuilding = str(instance.buildingList[i].idBuilding)
                if i != len(solution) - 1:
                    strToWrite += idBuilding + '\t' + idCare + '\n'
                else:
                    strToWrite += idBuilding + '\t' + idCare
                i += 1
            result.write(strToWrite)


    def writeQualityFile(self, bestQualityOfEachIterationList, averageQualityOfEachIterationList):
        with open('files/quality.txt', 'wt') as quality:
            i = 0
            strToWrite = 'ID_Iteration\tBest_Quality\tAverage_Quality\n'
            while i < len(bestQualityOfEachIterationList):
                if i != len(bestQualityOfEachIterationList) - 1:
                    strToWrite += str(i+1) + '\t' + str(bestQualityOfEachIterationList[i]) + '\t' + \
                                  str(averageQualityOfEachIterationList[i]) + '\n'
                else:
                    strToWrite += str(i + 1) + '\t' + str(bestQualityOfEachIterationList[i]) + '\t' + \
                                  str(averageQualityOfEachIterationList[i])
                i += 1
            quality.write(strToWrite)