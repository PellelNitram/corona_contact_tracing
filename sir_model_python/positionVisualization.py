import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt


def extractAgentFromSimulationData(agent):
    reader = csv.reader(open("SimulationData.csv"))
    # reader = csv.reader(open(ticker), delimiter=",")

    csv_data_list = []
    csv_data_list.extend(reader)

    x = list()
    y= list()
    csv_data_list_transposed = np.transpose(csv_data_list)
    #print(csv_data_list_transposed)
    for i in range(1, len(csv_data_list_transposed[0][:])):
        #print(csv_data_list_transposed[0][i])
        if(int(csv_data_list_transposed[0][i]) == agent):
            x.append(int(csv_data_list_transposed[1][i]))
            y.append(int(csv_data_list_transposed[2][i]))

    return x,y








randomWalk = extractAgentFromSimulationData(341)
circleWalk = extractAgentFromSimulationData(493)
plt.plot(randomWalk[0], randomWalk[1])
plt.plot(circleWalk[0], circleWalk[1])
plt.show()