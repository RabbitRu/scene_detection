#Во всех метриках А оригинал, B сгенерирован
#Метрики считают единицей длины один план,
#точнее будет учитывать продолжительность каждого плана в кадрах

# здесь можно добавить замер времени
def _planLength(division, index):
	return division[index] - division[index - 1]

# здесь можно добавить замер времени
def _planIntersection(divA, indexA, divB, indexB):
	return max(
		min(divA[indexA], divB[indexB]) - max(divA[indexA - 1],
		divB[indexB - 1]), 0)

def _puritySubfunc(divA, divB, T):
	NA = len(divA)
	NB = len(divB)
	leftSum = 0
	rightSum = 0
	result = 0
	for i in range(1, NA):
		rsi = _planLength(divA, i)
		summator = 0
		for j in range (1, NB):
			rsij = _planIntersection(divA, i, divB, j)
			summator = summator + (rsij * rsij) / (rsi * rsi)
		result += rsi * summator / T
	return result

#Метрика Purity
def metricPurity(divA, divB):
	if(divB[-1] != divA[-1]):
		print("Такого быть не должно, количество планов должно совпадать")
	totalLength = divB[-1]
	leftPart = _puritySubfunc(divA, divB, totalLength)
	rightPart = _puritySubfunc(divB, divA, totalLength)
	return leftPart * rightPart





def _findOverlappings(division, shotStart, shotEnd):
	leftOverlap = 0
	rightOverlap = 0 
	for i in range(1, len(division)):
		if(shotStart < division[i - 1] and division[i - 1] < shotEnd):
			leftOverlap = division[i - 1] - shotStart
		if(shotStart < division[i] and division[i] < shotEnd):
			rightOverlap = division[i] - shotStart
	# здесь можно добавить замер времени
	totalOverlap = leftOverlap + rightOverlap
	return totalOverlap

#Метрика Overflow
def metricOverflow(divA, divB):
	summator = 0
	for i in range(1, len(divB)):
		summator += _findOverlappings(divA, divB[i - 1], divB[i])
	return summator / divB[-1]



def _findLagrestOverlappingScene(division, shotStart, shotEnd):
	maxIntersec = 0
	for i in range(1, len(division)):
		intersection = 0
		if not (division[i] < shotStart or division[i - 1] > shotEnd):
			if(division[i] < shotEnd):
				# здесь можно добавить замер времени
				intersection = shotEnd - division[i]
			else:
				# здесь можно добавить замер времени
				intersection = min(shotEnd - shotStart, shotEnd - division[i - 1])
		if(intersection > maxIntersec):
			maxIntersec = intersection
	if(maxIntersec == 0):
		print("Для каждой сцены должно быть пересечение хоть в один план")
	return maxIntersec 

#Метрика Coverage
def metricCoverage(divA, divB):
	summator = 0
	for i in range(1,len(divA)):
		summator += _findLagrestOverlappingScene(
			divB,
			divA[i - 1],
			divA[i]) / (divA[i] - divA[i - 1])
	return summator / (len(divA) - 1)


def getMetrics(origDivision, ourDivision):
	purity = metricPurity(origDivision, ourDivision)
	coverage = metricCoverage(origDivision, ourDivision)
	overflow = metricOverflow(origDivision, ourDivision)
	allMetrics = []
	allMetrics.append(purity)
	allMetrics.append(coverage)
	allMetrics.append(overflow)
	return allMetrics











































































