class FileController:

    def readFile(self,filename, attachment):
        contentList = []
        counter = 0
        with open(filename, 'rt') as fileObj:
            for line in fileObj:
                if counter != 0:
                    contentList.append(line)
                counter += 1
            if attachment == 'building':
                print('Finish reading builidng file...')
            if attachment == 'care':
                print('Finish reading care file...')
            if attachment == 'distance':
                print('Finish reading distance file...')
        return contentList

    def writeFile(self, filename, bestSolution, instance):
        solution = bestSolution.solutionArray
        with open(filename, 'wt') as result:
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

