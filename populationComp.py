import pandas as pd
import matplotlib.pyplot as plt

distance = {}
listAges = ['0-9', '10-19', '20-29', '30-39',
            '40-49', '50-59', '60-69', '70+']
thirdAgeState = {}
densityState = {}
densityThirdState = {}
percentageThirdState = {}
populationState = {}
listAgeState = {}
dataAge = pd.read_csv("data/Data Spain - Age.csv")
dataArea = pd.read_csv("data/Data Spain - Area.csv")
for i in range(dataAge['Comunity'].size):
    if dataAge['Comunity'][i] in populationState:
        populationState[dataAge['Comunity'][i]] += dataAge['Population'][i]
    else:
        populationState[dataAge['Comunity'][i]] = dataAge['Population'][i]
    if '6' in dataAge['Age'][i]:
        thirdAgeState[dataAge['Comunity'][i]] = dataAge['Population'][i]
    elif '7' in dataAge['Age'][i]:
        thirdAgeState[dataAge['Comunity'][i]] += dataAge['Population'][i]

for i in range(dataArea['Comunity'].size):
    densityState[dataArea['Comunity'][i]] = pd.to_numeric(dataArea['Density'][i])

for key in populationState:
    """print("La poblacion en {} de la tercera edad es del {}% con una densidad de {} personas/km2".
          format(key,
                 thirdAgeState[key]/populationState[key],
                 thirdAgeState[key]/populationState[key]*densityState[key]))"""
    percentageThirdState[key] = thirdAgeState[key]/populationState[key]
    densityThirdState[key] = thirdAgeState[key]/populationState[key]*densityState[key]


diff = 100
keyState = ''
for key in percentageThirdState:
    if key != 'AGUASCALIENTES' and diff > abs(percentageThirdState[key]-percentageThirdState['AGUASCALIENTES']):
        keyState = key
        diff = abs(percentageThirdState[key]-percentageThirdState['AGUASCALIENTES'])
print("Mayor Similitud en %: {} con {} y AGUASCALIENTES con {}".
      format(keyState, percentageThirdState[keyState], percentageThirdState['AGUASCALIENTES']))

diff = 100
keyState = ''
for key in densityThirdState:
    if key != 'AGUASCALIENTES' and diff > abs(densityThirdState[key]-densityThirdState['AGUASCALIENTES']):
        keyState = key
        diff = abs(densityThirdState[key]-densityThirdState['AGUASCALIENTES'])
print("Mayor Similitud en densidad: {} con {} y AGUASCALIENTES con {}".
      format(keyState, densityThirdState[keyState], densityThirdState['AGUASCALIENTES']))


for i in range(dataAge['Comunity'].size):
    if dataAge['Comunity'][i] in listAgeState:
        listAgeState[dataAge['Comunity'][i]].append(dataAge['Population'][i]/populationState[dataAge['Comunity'][i]])
    else:
        listAgeState[dataAge['Comunity'][i]] = [dataAge['Population'][i]/populationState[dataAge['Comunity'][i]]]
for key in listAgeState:
    if key not in distance:
        distance[key] = 0
    #print("Porcentajes de población en {}".format(key))
    for i in range(len(listAgeState[key])):
        #print("De {} años = {}".format(listAges[i], listAgeState[key][i]))
        if key != 'AGUASCALIENTES':
            distance[key] += (listAgeState[key][i] - listAgeState['AGUASCALIENTES'][i]) ** 2


diff = 100
keyState = ''
for key in distance:
    if key != 'AGUASCALIENTES' and diff > abs(distance[key]-distance['AGUASCALIENTES']):
        keyState = key
        diff = abs(distance[key]-distance['AGUASCALIENTES'])
print("Mayor Similitud en distribución: {} con AGUASCALIENTES".format(keyState))
for i in range(len(listAgeState[keyState])):
    print("De {} años = {} y {}".format(listAges[i], listAgeState[keyState][i], listAgeState['AGUASCALIENTES'][i]))
