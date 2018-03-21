import time
import copy

# 插入排序 576s
def insert_sort(copiedDistanceMatrix, distanceSortedBuildingIndexMatrix):
    indexCare = 0
    while indexCare < len(copiedDistanceMatrix[0]):
        sortOneColumnStartTime = time.time()
        distanceColumn = [column[indexCare] for column in copiedDistanceMatrix]
        distanceIndexRow = copy.deepcopy(distanceSortedBuildingIndexMatrix[indexCare])
        count = len(distanceColumn)
        for i in range(1, count):
            print("Travel %dth building for %dth care sort..." % (i, indexCare + 1))
            key = distanceColumn[i]
            keyIndex = distanceIndexRow[i]
            j = i - 1
            while j >= 0:
                if distanceColumn[j] > key:
                    #distanceColumn[j + 1] = distanceColumn[j]
                    #distanceColumn[j] = key
                    distanceIndexRow[j + 1] = distanceIndexRow[j]
                    distanceIndexRow[j] = keyIndex
                j -= 1
        distanceSortedBuildingIndexMatrix[indexCare] = distanceIndexRow
        sortOneColumnEndTime = time.time()
        print("Finish sorting for %dth care, it tackes %ds" % (indexCare + 1, sortOneColumnEndTime - sortOneColumnStartTime))
        indexCare += 1


#冒泡排序 529s
def bubble_sort(copiedDistanceMatrix, distanceSortedBuildingIndexMatrix):
    indexCare = 0
    while indexCare < len(copiedDistanceMatrix[0]):
        sortOneColumnStartTime = time.time()
        distanceColumn = [column[indexCare] for column in copiedDistanceMatrix]
        distanceIndexRow = copy.deepcopy(distanceSortedBuildingIndexMatrix[indexCare])
        count = len(distanceColumn)
        for i in range(0, count):
            print("Travel %dth building for %dth care sort..." % (i, indexCare + 1))
            for j in range(i + 1, count):
                if  distanceColumn[i] >  distanceColumn[j]:
                    distanceColumn[i], distanceColumn[j] =  distanceColumn[j], distanceColumn[i]
                    distanceIndexRow[i], distanceIndexRow[j] = distanceIndexRow[j], distanceIndexRow[i]
        #distanceSortedBuildingIndexMatrix[indexCare] = distanceIndexRow
        sortOneColumnEndTime = time.time()
        print("Finish sorting for %dth care, it tackes %ds" % (
        indexCare + 1, sortOneColumnEndTime - sortOneColumnStartTime))
        indexCare += 1


# 选择排序 274s
def select_sort(copiedDistanceMatrix, distanceSortedBuildingIndexMatrix):
    indexCare = 0
    while indexCare < len(copiedDistanceMatrix[0]):
        sortOneColumnStartTime = time.time()
        distanceColumn = [column[indexCare] for column in copiedDistanceMatrix]
        distanceIndexRow = copy.deepcopy(distanceSortedBuildingIndexMatrix[indexCare])
        count = len(distanceColumn)
        for i in range(0, count):
            print("Travel %dth building for %dth care sort..." % (i, indexCare + 1))
            min = i
            for j in range(i + 1, count):
                if distanceColumn[min] > distanceColumn[j]:
                    min = j
            #distanceColumn[min], distanceColumn[i] = distanceColumn[i], distanceColumn[min]
            distanceIndexRow[min], distanceIndexRow[i] = distanceIndexRow[i], distanceIndexRow[min]
        distanceSortedBuildingIndexMatrix[indexCare] = distanceIndexRow
        sortOneColumnEndTime = time.time()
        print("Finish sorting for %dth care, it tackes %ds" % (
        indexCare + 1, sortOneColumnEndTime - sortOneColumnStartTime))
        indexCare += 1

# 归并排序 0s
def merge_sort(distanceColumn, distanceIndexRow):
    if len(distanceColumn) <= 1:
        return distanceColumn, distanceIndexRow
    num = int(len(distanceColumn) / 2)
    left, leftIndex = merge_sort(distanceColumn[:num], distanceIndexRow[:num])
    right, rightIndex = merge_sort(distanceColumn[num:], distanceIndexRow[num:])
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

def merge_start(copiedDistanceMatrix, distanceSortedBuildingIndexMatrix):
    indexCare = 0
    while indexCare < len(copiedDistanceMatrix[0]):
        sortOneColumnStartTime = time.time()
        distanceColumn = [column[indexCare] for column in copiedDistanceMatrix]
        distanceIndexRow = copy.deepcopy(distanceSortedBuildingIndexMatrix[indexCare])
        distanceColumn, distanceIndexRow = merge_sort(distanceColumn, distanceIndexRow)
        distanceSortedBuildingIndexMatrix[indexCare] = distanceIndexRow
        sortOneColumnEndTime = time.time()
        print("Finish sorting for %dth care, it tackes %ds" % (
            indexCare + 1, sortOneColumnEndTime - sortOneColumnStartTime))
        indexCare += 1

copiedDistanceMatrix = [[2,4,5,3,1],[56,29,3,43,11], [3,54,67,13,4], [22,51,78,32,45]]
distanceSortedBuildingIndexMatrix = [list(range(4))] * 5
merge_start(copiedDistanceMatrix, distanceSortedBuildingIndexMatrix)
print(distanceSortedBuildingIndexMatrix)