#-*-coding:utf-8-*-


class FileController:
    '''
    Description: cette classe est le controleur de fichier, y compris la lecture et l'écriture
    Attribut: rien
    '''

    def readBuildingFile(self,buildingFilename):
        '''
        Description: cette méthode est pour lire le fichier de bâtiment
        :param buildingFilename: (String) le nom du fichier de bâtiment
        :return: buildingContentList: (String[]) la liste de lignes du fichier de bâtiment
        '''

        buildingContentList = []
        counter = 0
        with open(buildingFilename, 'rt') as buildings:
            for building in buildings:
                # si c'est pas la première ligne (car la première ligne est les titres)
                if counter != 0:
                    # ajouter cette ligne dans la liste buildingContentList
                    buildingContentList.append(building)
                counter += 1
        print('Finish reading builidng file...')
        return buildingContentList


    def readCareFile(self, careFilename):
        '''
        Description: cette méthode est pour lire le fichier de centre d'accueil(care)
        :param careFilename: (String) le nom du fichier care
        :return: careContentList: (String[]) la liste de lignes du fichier de care
        '''

        careContentList = []
        counter = 0
        with open(careFilename, 'rt') as cares:
            for care in cares:
                # si c'est pas la première ligne (car la première ligne est les titres)
                if counter != 0:
                    # ajouter cette ligne dans la liste careContentList
                    careContentList.append(care)
                counter += 1
        print('Finish reading care file...')
        return careContentList


    def readDistanceFile(self, distanceFilename):
        '''
        Description: cette méthode est pour lire le fichier de distance
        :param distanceFilename: (String) le nom du fichier distance
        :return: distanceContentList: (String[]) la liste de lignes du fichier de distance
        '''

        distanceContentList = []
        counter = 0
        with open(distanceFilename, 'rt') as distances:
            for distance in distances:
                # si c'est pas la première ligne (car la première ligne est les titres)
                if counter != 0:
                    # ajouter cette ligne dans la liste distanceContentList
                    distanceContentList.append(distance)
                counter += 1
        print('Finish reading distance file...')
        return distanceContentList


    def writeSolutionFile(self, solutionFilename, bestSolution, instance):
        '''
        Description: cette méthode est pour écrire la meilleure solutions dans le fichier de solution
        :param solutionFilename: (String) le nom du fichier de solution
        :param bestSolution: (l'object de la classe de SolutionModel) la meilleure solutions
        :param instance: (l'objet de la classe de InstanceModel) l'instance pour ce projet
        :return: rien
        '''

        solution = bestSolution.solutionArray
        with open(solutionFilename, 'wt') as result:
            i = 0
            # ajouter les titres (ID_BAT ID_CARE) dans la première ligne
            strToWrite = 'ID_BAT\tID_CARE\n'

            # écrire la solution dans le fichier
            while i < len(solution):
                # si l'indice de care n'est pas -1
                if str(solution[i]) != '-1':
                    indexCare = int(solution[i])
                    # obtenir l'id de care selon son indice dans la liste de care
                    idCare = str(instance.careList[indexCare].idCare)
                # sinon, l'id de care est -1
                else:
                    idCare = str(-1)

                # obtenir l'id de bâtiment selon son indice dans la liste de bâtiment
                idBuilding = str(instance.buildingList[i].idBuilding)

                # si c'est pas le dernier élément, ajouter un "\n" à la fin de la ligne
                if i != len(solution) - 1:
                    strToWrite += idBuilding + '\t' + idCare + '\n'
                # si c;est le dernier élément，ne pas ajouter "\n"
                else:
                    strToWrite += idBuilding + '\t' + idCare
                i += 1
            result.write(strToWrite)


    def writeQualityFile(self, qualityFileName, bestQualityOfEachIterationList, averageQualityOfEachIterationList):
        '''
        Description: cette méthode est pour écrire les qualités des meilleures solutions de chaque itération et
                        les qualités moyennes des solutions de chaque itération dans le fichier de qualité
        :param bestQualityOfEachIterationList: (float[]) la liste de qualités des meilleures solutions de chaque itération
        :param averageQualityOfEachIterationList: (float[]) la liste de qualités moyennes de solutions de chaque itération
        :return: rien
        '''

        with open(qualityFileName, 'wt') as quality:
            i = 0
            # ajouter les titres (ID_Iteration  Best_Quality    Average_Quality) dans la première ligne
            strToWrite = 'ID_Iteration\tBest_Quality\tAverage_Quality\n'

            # écrire les qualités dans le fichier
            while i < len(bestQualityOfEachIterationList):
                # si c'est pas le dernier élément, ajouter un "\n" à la fin de la ligne
                if i != len(bestQualityOfEachIterationList) - 1:
                    strToWrite += str(i+1) + '\t' + str(bestQualityOfEachIterationList[i]) + '\t' + \
                                  str(averageQualityOfEachIterationList[i]) + '\n'
                # si c;est le dernier élément，ne pas ajouter "\n"
                else:
                    strToWrite += str(i + 1) + '\t' + str(bestQualityOfEachIterationList[i]) + '\t' + \
                                  str(averageQualityOfEachIterationList[i])
                i += 1
            quality.write(strToWrite)