# Generated with SMOP  0.41
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import random as rd
import datetime

now = datetime.datetime.now()

def InitializeAgentStates(numberOfAgents,initialInfected):

    agentState = np.ones((numberOfAgents,),dtype=np.int64)
    perm = np.random.permutation(numberOfAgents)
    agentState[perm < initialInfected + 1] = 2
    return agentState

    
def InitializeDiffusionRates(numberOfAgents):

    p=6
    xmin=0
    xmax=1
    diffusionRates= xmin + (xmax - xmin)*np.sum(np.random.rand(numberOfAgents,p),1)/p
    return diffusionRates

def InitializeAgentBehaviour(numberOfAgents, mobilityRate):
    agentBehaviour = np.ones((numberOfAgents,), dtype=np.int64)
    perm = np.random.permutation(numberOfAgents)
    agentBehaviour[perm < numberOfAgents*mobilityRate + 1] = 2
    return agentBehaviour


def IllnessDynamics(grid,agentState,beta,gamma):

    numberOfIndividualsOnCell = grid.applymap(len)

    groupIndices=numberOfIndividualsOnCell > 1
    singleIndices=numberOfIndividualsOnCell == 1
    groups = grid[groupIndices].stack()
    singles = grid[singleIndices].stack()

    for group in groups:
        group = np.array(group)
        groupStates=agentState[group]
        for j in range(len(group)):
            individual=group[j]
            state=groupStates[j]
            if state == 2:
                r = np.random.rand()
                if r < beta:
                    healtyIndividuals = group[groupStates == 1]
                    agentState[healtyIndividuals] = 2
                q = np.random.rand()
                if q < gamma:
                    agentState[individual] = 3
    
    
    for single in singles:
        state=agentState[single]
        if state == 2:
            q = np.random.rand()
            if q < gamma:
                agentState[single]=3
    
    return agentState

def PerformeRandomSteps(numberOfAgents,locations,gridSize,diffusionRates):

    grid = [[[] for i in range(gridSize)] for i in range(gridSize)]

    for i in range(numberOfAgents):
        r = np.random.rand()
        loc = np.copy(locations[i,:])
        if r < diffusionRates[i]:
            while np.array_equal(loc,locations[i,:]):
                direction = np.random.randint(4)
                if direction == 0:
                    loc[0] = min(max(0,loc[0] + 1),gridSize-1)
                elif direction == 1:
                    loc[0]=min(max(0,loc[0] - 1),gridSize-1)
                elif direction == 2:
                    loc[1]=min(max(0,loc[1] + 1),gridSize-1)
                elif direction == 3:
                    loc[1]=min(max(0,loc[1] - 1),gridSize-1)

        locations[i,:]=loc
        grid[loc[0]][loc[1]].append(i)

    grid_ = pd.DataFrame(grid)
    return grid_, locations



def PerformeSteps(numberOfAgents,locations,gridSize,diffusionRates):
    def calculate_coordinates_circle_walk(xOld, yOld, x0, y0, gridSize):
        radius = 10. + rd.random() * 2.
        # radius = rd.random()*2.+3.
        angle = (rd.random() - 0.5) * 0.5
        xNew = int(radius * (np.cos(angle) * (1) - np.sin(angle) * (1)) + x0)
        yNew = int(radius * (np.sin(angle) * (1) + np.cos(angle) * (1)) + y0)
        #print("f " + str((xNew, yNew)))
        # ensure valid dataFrame index
        if ((xNew > gridSize - 1 or xNew < 0) or (yNew > gridSize - 1 or yNew < 0)):
            angle = angle + np.pi
            xNew = int(radius * (np.cos(angle) * (1) - np.sin(angle) * (1)) + x0)
            yNew = int(radius * (np.sin(angle) * (1) + np.cos(angle) * (1)) + y0)
            if ((xNew > gridSize - 1 or xNew < 0) or (yNew > gridSize - 1 or yNew < 0)):
                xNew = xOld
                yNew = yOld

        return (xNew, yNew)

    grid = [[[] for i in range(gridSize)] for i in range(gridSize)]
    
    for i in range(numberOfAgents):
        r = np.random.rand()
        loc = np.copy(locations[i,:])
        if r < diffusionRates[i]:
            if(agentBehaviour[i] == 2):
                #random walk
                while np.array_equal(loc,locations[i,:]):
                    direction = np.random.randint(4)
                    stepsize = int(rd.random()*5)
                    if direction == 0:
                        loc[0] = min(max(0,loc[0] + stepsize),gridSize-stepsize)
                    elif direction == 1:
                        loc[0]=min(max(0,loc[0] - stepsize),gridSize-stepsize)
                    elif direction == 2:
                        loc[1]=min(max(0,loc[1] + stepsize),gridSize-stepsize)
                    elif direction == 3:
                        loc[1]=min(max(0,loc[1] - stepsize),gridSize-stepsize)
            elif(agentBehaviour[i] == 1):
                #circle walk
                loc[0], loc[1] = calculate_coordinates_circle_walk(loc[0], loc[1], agentHomeTown[i][0], agentHomeTown[i][0], gridSize)


        locations[i,:]=loc
        grid[loc[0]][loc[1]].append(i)

    grid_ = pd.DataFrame(grid)
    return grid_, locations



# Initial values
numberOfAgents = 1000
gridSize = 100
initialInfected = 5
testRate = 0.1
mobilityRate = 0.5

# Implement disease parameters
beta = 0.6
gamma = 0.01

# generate some agents and assign them a location, set up agent attributes
locations=np.random.randint(gridSize,size=(numberOfAgents,2),dtype=int)
agentHomeTown = np.copy(locations)
agentState = InitializeAgentStates(numberOfAgents,initialInfected)
diffusionRates = InitializeDiffusionRates(numberOfAgents)
agentIds = np.arange(numberOfAgents,dtype=np.int64)
agentBehaviour = InitializeAgentBehaviour(numberOfAgents, mobilityRate)

# save agent master information
AgentMaster = pd.DataFrame({'agent': agentIds, 'state': agentState, 'diffusion_rate': diffusionRates, 'behaviour' : agentBehaviour})
AgentMaster.to_csv('./datadumps/AgentMaster_{}.csv'.format(now.strftime("%Y-%m-%d_%H_%M_%S")), index=False)

# Initialize empty grid and fill with agents based on location
grid = [[[] for i in range(gridSize)] for i in range(gridSize)]
for i in range(numberOfAgents):
    loc=locations[i,:]
    grid[loc[0]][loc[1]].append(i)

grid_ = pd.DataFrame(grid)

# preallocate arrays for saving
prealloc = 100000
numberOfhealthy = np.full((prealloc,), np.NaN)
numberOfIll = np.full((prealloc,), np.NaN)
numberOfRecovered = np.full((prealloc,), np.NaN)
numberOfhealthy[0] = sum(agentState == 1)
numberOfIll[0] = sum(agentState == 2)
numberOfRecovered[0] = sum(agentState == 3)
simulationData = np.full((prealloc, 5), np.NaN)



ObservedStates = np.zeros(agentState.shape,dtype=np.int64)
testedAgents = np.zeros(agentState.shape)
testedHealthy = False

t = 0

# Initialize data export array 
simulationData[0:numberOfAgents,:] = np.concatenate((np.expand_dims(agentIds,axis=1),
                                                    locations,
                                                    np.expand_dims(t*np.ones(numberOfAgents),axis=1),
                                                    np.expand_dims(ObservedStates,axis=1)), axis=1)
while numberOfIll[t] > 0:
    
    # run disease dynamics (SIR model)
    agentState = IllnessDynamics(grid_,agentState,beta,gamma)
    
    # Update step
    grid_, locations = PerformeRandomSteps(numberOfAgents,locations,gridSize,diffusionRates)
    
    # Perform tests for virus
    agentStateTested = agentState + testedAgents
    if np.random.rand() < testRate: # Perform test with certain probability
        try:
            if np.random.rand() < 0.2: # test healthy person with probability 20%
                agent_id = np.random.choice(agentIds[agentState==1])
                testedHealthy = True
            else:
                agent_id = np.random.choice(agentIds[agentState==2])
                testedHealthy = False

            testedAgents[agent_id] = 1
        except:
            # testing failed
            pass
        

    t = t + 1

    # reallocate space
    if numberOfAgents*(t+1)> simulationData.shape[0]:
        simulationData = np.concatenate((simulationData,np.full((prealloc, 5), np.NaN)))
        numberOfhealthy = np.concatenate((numberOfhealthy, np.full((prealloc,), np.NaN)))
        numberOfIll = np.concatenate((numberOfIll, np.full((prealloc,), np.NaN)))
        numberOfRecovered = np.concatenate((numberOfRecovered, np.full((prealloc,), np.NaN)))

    # save Info of saved 
    ObservedStates = np.zeros(agentState.shape)
    ObservedStates[testedAgents == 1] = agentState[testedAgents == 1]
    simulationData[numberOfAgents*t:numberOfAgents*(t+1),:] = np.concatenate((np.expand_dims(agentIds,axis=1),
                                                                                locations,
                                                                                np.expand_dims(t*np.ones(numberOfAgents),axis=1),
                                                                                np.expand_dims(ObservedStates,axis=1)), axis=1)
                                    
    # reset test count if agent was healthy
    if testedHealthy == True:
        testedAgents[agent_id] = 0

    numberOfhealthy[t] = sum(agentState == 1)
    numberOfIll[t] = sum(agentState == 2)
    numberOfRecovered[t] = sum(agentState == 3)

    if t%100==0:
        print(t)



simulationData = simulationData[~np.isnan(simulationData).any(axis=1),:]
numberOfhealthy = numberOfhealthy[~np.isnan(numberOfhealthy)]
numberOfIll = numberOfIll[~np.isnan(numberOfIll)]
numberOfRecovered = numberOfRecovered[~np.isnan(numberOfRecovered)]

SimulationData = pd.DataFrame({'agent':simulationData[:,0].astype(int),'x':simulationData[:,1].astype(int), 'y':simulationData[:,2].astype(int), 't':simulationData[:,3].astype(int),'state':simulationData[:,4].astype(int)})
SimulationData.to_csv('./datadumps/SimulationData_{}.csv'.format(now.strftime("%Y-%m-%d_%H_%M_%S")), index=False)

plt.plot(numberOfhealthy, label="susceptibles")
plt.plot(numberOfIll, label="infected")
plt.plot(numberOfRecovered, label="recovered")
plt.legend()
plt.show()