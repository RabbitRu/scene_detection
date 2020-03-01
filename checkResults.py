from numpy import loadtxt

#Во всех метриках А оригинал, B сгенерирован

# здесь можно добавить замер времени
def planLength(division, index):
	return division[index] - division[index - 1]

# здесь можно добавить замер времени
def planIntersection(divA, indexA, divB, indexB):
	return max(min(divA[indexA], divB[indexB]) - max(divA[indexA - 1], divB[indexB - 1]), 0)

def puritySubfunc(divA, divB, T):
	NA = len(divA)
	NB = len(divB)
	leftSum = 0
	rightSum = 0
	result = 0
	for i in range(1, NA):
		rsi = planLength(divA, i)
		summator = 0
		for j in range (1, NB):
			rsij = planIntersection(divA, i, divB, j)
			summator = summator + (rsij * rsij) / (rsi * rsi)
		result = result + rsi * summator / T
	return result


#Метрика Purity
#Считает единицей длины один план, точнее будет учитывать продолжительность каждого плана в кадрах
def metricPurity(divA, divB):
	if(divB[-1] != divA[-1]):
		print("Такого быть не должно, количество планов должно совпадать")
	totalLength = divB[-1]
	leftPart = puritySubfunc(divA, divB, totalLength)
	rightPart = puritySubfunc(divB, divA, totalLength)
	return leftPart * rightPart





def findOverlappings(division, shotStart, shotEnd):
	leftOverlap = 0
	rightOverlap = 0 
	for i in range(1, len(division)):
		if(shotStart < division[i - 1] and division[i - 1] < shotEnd):
			leftOverlap = division[i - 1] - shotStart
		if(shotStart < division[i] and division[i] < shotEnd):
			rightOverlap = division[i] - shotStart
	totalOverlap = leftOverlap + rightOverlap # здесь можно добавить замер времени
	return totalOverlap

def metricOverflow(divA, divB):
	summator = 0
	for i in range(1, len(divB)):
		summator = summator + findOverlappings(divA, divB[i - 1], divB[i])
	return summator / divB[-1]


def findLagrestOverlappingScene(division, shotStart, shotEnd):
	maxIntersec = 0
	for i in range(1, len(division)):
		intersection = 0
		if not (division[i] < shotStart or division[i - 1] > shotEnd):
			if(division[i] < shotEnd):
				intersection = shotEnd - division[i]# здесь можно добавить замер времени
			else:
				intersection = min(shotEnd - shotStart, shotEnd - division[i - 1])# здесь можно добавить замер времени
		if(intersection > maxIntersec):
			maxIntersec = intersection
	if(maxIntersec == 0):
		print("Для каждой сцены должно быть пересечение хоть в один план")
	return maxIntersec 

def metricCoverage(divA, divB):
	summator = 0
	for i in range(1,len(divA)):
		summator = summator + findLagrestOverlappingScene(divB, divA[i - 1], divA[i]) / (divA[i] - divA[i - 1])
	return summator / len(divA)



division = loadtxt("division.txt", int )
purity = metricPurity(division, division)
print("Purity " + str(purity))

coverage = metricCoverage(division, division)
print("Coverage " + str(coverage))


overflow = metricOverflow(division, division)
print("Overflow " + str(overflow))












































































