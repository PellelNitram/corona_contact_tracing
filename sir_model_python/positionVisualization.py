import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random as rd


def extractAgentFromSimulationData(agent):
    reader = csv.reader(open("SimulationData.csv"))
    # reader = csv.reader(open(ticker), delimiter=",")

    csv_data_list = []
    csv_data_list.extend(reader)

    x = list()
    y= list()
    csv_data_list_transposed = np.transpose(csv_data_list)
    #print(csv_data_list_transposed)
    print(len(csv_data_list_transposed[0][:]))
    for i in range(5, len(csv_data_list_transposed[0][:])):
        #print(csv_data_list_transposed[0][i])
        if(int(csv_data_list_transposed[0][i]) == agent):
            x.append(int(csv_data_list_transposed[1][i]))
            y.append(int(csv_data_list_transposed[2][i]))

    return x,y

def extractInfections():
    reader = csv.reader(open("SimulationData.csv"))
    csv_data_list = []
    csv_data_list.extend(reader)
    csv_data_list_transposed = np.transpose(csv_data_list)
    t_max = 715
    data = [[] for i in range(t_max)]
    #print(len(csv_data_list_transposed[0][:]))
    for i in range(1, len(csv_data_list_transposed[0][:])-1):
        print(i)
        if (int(csv_data_list_transposed[4][i]) == 2):

            data[int(csv_data_list_transposed[3][i])].append(int(csv_data_list_transposed[1][i]))
            data[int(csv_data_list_transposed[3][i])].append(int(csv_data_list_transposed[2][i]))
            pass
    return data

def extractHealty():
    reader = csv.reader(open("SimulationData.csv"))
    csv_data_list = []
    csv_data_list.extend(reader)
    csv_data_list_transposed = np.transpose(csv_data_list)
    t_max = 715
    data = [[] for i in range(t_max)]
    #print(len(csv_data_list_transposed[0][:]))
    for i in range(1, len(csv_data_list_transposed[0][:])-1):
        print(i)
        if (int(csv_data_list_transposed[4][i]) == 0):
            data[int(csv_data_list_transposed[3][i])].append(int(csv_data_list_transposed[1][i]))
            data[int(csv_data_list_transposed[3][i])].append(int(csv_data_list_transposed[2][i]))
            pass
    return data

def extractData():
    reader = csv.reader(open("SimulationData.csv"))
    csv_data_list = []
    csv_data_list.extend(reader)
    csv_data_list_transposed = np.transpose(csv_data_list)
    t_max = int(len(csv_data_list_transposed[0][:])-1/1000)
    dataI = [[] for i in range(t_max)]
    dataH = [[] for i in range(t_max)]
    dataR = [[] for i in range(t_max)]
    #print(len(csv_data_list_transposed[0][:]))
    for i in range(1, len(csv_data_list_transposed[0][:])-1):
        #print(i)
        if (int(csv_data_list_transposed[4][i]) == 0 or int(csv_data_list_transposed[4][i]) == 1  and rd.random() > 0.0):
            dataH[int(csv_data_list_transposed[3][i])].append(int(csv_data_list_transposed[1][i]))
            dataH[int(csv_data_list_transposed[3][i])].append(int(csv_data_list_transposed[2][i]))
        elif(int(csv_data_list_transposed[4][i]) == 2):
            #print("i " + str(i) + "  " + str(int(csv_data_list_transposed[4][i])))
            dataI[int(csv_data_list_transposed[3][i])].append(int(csv_data_list_transposed[1][i]))
            dataI[int(csv_data_list_transposed[3][i])].append(int(csv_data_list_transposed[2][i]))
        elif (int(csv_data_list_transposed[4][i]) == 3):
            # print("i " + str(i) + "  " + str(int(csv_data_list_transposed[4][i])))
            dataR[int(csv_data_list_transposed[3][i])].append(int(csv_data_list_transposed[1][i]))
            dataR[int(csv_data_list_transposed[3][i])].append(int(csv_data_list_transposed[2][i]))
        if(i == (len(csv_data_list_transposed[0][:])*0.9)):
            break
    return dataH, dataI, dataR


def animateInfeciton():
    healthyData, infectionData, recoveredData = extractData()
    t_max = len(healthyData[0])
    xdataI, ydataI, xdataH, ydataH, xdataR, ydataR = [], [], [], [], [],[]

    fig, ax = plt.subplots()
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 200)
    line1, = ax.plot(xdataH, ydataH, 'ro',  color="b", alpha = 0.5)
    line2, = ax.plot(xdataI, ydataI, 'ro',  color="r", alpha = 0.5)
    line3, = ax.plot(xdataR, ydataR, 'ro', color="g", alpha=0.5)
    title = ax.text(0.5, 0.85, "", bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5},
                    transform=ax.transAxes, ha="center")


    def update(frame, line1, line2):
        frame = int(frame)
        xdataI, ydataI, xdataH, ydataH, xdataR, ydataR = [], [], [], [], [],[]
        xdataI.append(infectionData[frame][0::2])
        ydataI.append(infectionData[frame][1::2])
        xdataH.append(healthyData[frame][0::2])
        ydataH.append(healthyData[frame][1::2])
        xdataR.append(recoveredData[frame][0::2])
        ydataR.append(recoveredData[frame][1::2])
        #print("t = " + str(frame) + " nfected  " + str(len(xdataI[0])));

        line1.set_data(xdataH, ydataH)
        line2.set_data(xdataI, ydataI)
        line3.set_data(xdataR, ydataR)
        ax.set_title("t= " + str(frame))
        return [line1, line2]



    ani = FuncAnimation(fig, update, frames=range(0,1180), fargs=[line1, line2],
                      blit=False)

    plt.show()






