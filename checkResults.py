from numpy import loadtxt




def planLength(division, index):
	return division[index] - division[index - 1]

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
	#rightPart = puritySubfunc(divB, divA, totalLength)
	return leftPart# * rightPart





division = loadtxt("division.txt", int )
purity = metricPurity(division, division)
print("Purity " + str(purity))












































































