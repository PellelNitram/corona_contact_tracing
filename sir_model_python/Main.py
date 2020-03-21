# Generated with SMOP  0.41
import numpy as np
import pandas as pd
from time import time
import matplotlib.pyplot as plt


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

def PerformeSteps(numberOfAgents,locations,gridSize,diffusionRates):
    
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



# Initial values
numberOfAgents = 1000
gridSize = 100
initialInfected = 5
testRate = 0.1

# Implement disease parameters
beta = 0.6
gamma = 0.01

# generate some agents and assign them a location
locations=np.random.randint(gridSize,size=(numberOfAgents,2),dtype=int)
agentState = InitializeAgentStates(numberOfAgents,initialInfected)
diffusionRates = InitializeDiffusionRates(numberOfAgents)
agentIds = np.arange(numberOfAgents,dtype=np.int64)

# save agent master information
AgentMaster = pd.DataFrame({'agent': agentIds, 'state': agentState, 'diffusion_rate': diffusionRates})
AgentMaster.to_csv('AgentMaster.csv', index=False)

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
    grid_, locations = PerformeSteps(numberOfAgents,locations,gridSize,diffusionRates)
    
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
SimulationData.to_csv('SimulationData.csv', index=False)

plt.plot(numberOfhealthy, label="susceptibles")
plt.plot(numberOfIll, label="infected")
plt.plot(numberOfRecovered, label="recovered")
plt.legend()
plt.show()