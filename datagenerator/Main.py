# Generated with SMOP  0.41
import numpy as np
import pandas as pd

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



testRate = 0.1
numberOfAgents = 20
initialInfected = 3

beta = 0.6

gamma = 0.01
gridSize = 10


# generate some agents and assign them a location
locations=np.random.randint(gridSize,size=(numberOfAgents,2))

agentState = InitializeAgentStates(numberOfAgents,initialInfected)
diffusionRates = InitializeDiffusionRates(numberOfAgents)

agentIds = np.arange(numberOfAgents)

AgentMaster = pd.DataFrame({'agent':agentIds,'state':agentState, 'diffusion_rate':diffusionRates})
AgentMaster.to_csv('AgentMaster_py.csv', index=False)


grid = [[[] for i in range(gridSize)] for i in range(gridSize)]

for i in range(numberOfAgents):
    loc=locations[i,:]
    grid[loc[0]][loc[1]].append(i)

grid_ = pd.DataFrame(grid)

prealloc = 30
numberOfhealthy = np.full((prealloc,), np.NaN)
numberOfIll = np.full((prealloc,), np.NaN)
numberOfRecovered = np.full((prealloc,), np.NaN)
numberOfhealthy[0] = sum(agentState == 1)
numberOfIll[0] = sum(agentState == 2)
numberOfRecovered[0] = sum(agentState == 3)



simulationData = np.full((prealloc, 5), np.NaN)
knownStates = np.zeros(agentState.shape,dtype=np.int64)


testedAgents = np.zeros(agentState.shape)
testedHealthy = False
prob = np.zeros(agentState.shape)
f = 0.2


t = 0
# TODO: Dataexport initialisieren
simulationData[0:numberOfAgents,:] = np.concatenate((np.expand_dims(agentIds,axis=1),
                                                    locations,
                                                    np.expand_dims(t*np.ones(numberOfAgents),axis=1),
                                                    np.expand_dims(knownStates,axis=1)), axis=1)
while numberOfIll[t] > 0:

    agentState = IllnessDynamics(grid_,agentState,beta,gamma)
    # grid, locations = PerformeSteps(numberOfAgents,locations,gridSize,diffusionRates,nargout=2)
    
    agentStateTested = agentState + testedAgents
    
    if 0 < testRate: #np.random.rand()
        # Test sampling
        sum_1 = sum(agentStateTested==1)
        sum_2 = sum(agentStateTested==2)
        sum_1_2 =sum_1 + sum_2

        a = 1/(sum_1/sum_1_2+sum_2/(f*sum_1_2))
        prob[agentStateTested==1] = a * 1 / (sum(agentStateTested==1)+sum(agentStateTested==2)) # probability to select healthy agent to test
        prob[agentStateTested==2] = a/f * 1 / (sum(agentStateTested==1)+sum(agentStateTested==2)) # probability to select sick agent to test
        prob[agentStateTested>2] = 0
        agent_id = np.random.choice(agentIds,p=prob)

        if agentState[agent_id]==1:
            testedHealthy = True
        else:
            testedHealthy = False

        testedAgents[agent_id] = 1
        
    # eventuell redundante daten nicht abspeichern
    t = t + 1

    if numberOfAgents*(t+1)> simulationData.shape[0]:
        simulationData = np.concatenate((simulationData,np.full((prealloc, 5), np.NaN)))
        numberOfhealthy = np.concatenate((numberOfhealthy, np.full((prealloc,), np.NaN)))
        numberOfIll = np.concatenate((numberOfIll, np.full((prealloc,), np.NaN)))
        numberOfRecovered = np.concatenate((numberOfRecovered, np.full((prealloc,), np.NaN)))


    knownStates = np.zeros(agentState.shape)
    knownStates[testedAgents == 1] = agentState[testedAgents == 1]
    simulationData[numberOfAgents*t:numberOfAgents*(t+1),:] = np.concatenate((np.expand_dims(agentIds,axis=1),
                                                                                locations,
                                                                                np.expand_dims(t*np.ones(numberOfAgents),axis=1),
                                                                                np.expand_dims(knownStates,axis=1)), axis=1)
                                    
    # reset test count if agent was healthy
    if testedHealthy == 1:
        testedAgents[agent_id] = 0

    numberOfhealthy[t] = sum(agentState == 1)
    numberOfIll[t] = sum(agentState == 2)
    numberOfRecovered[t] = sum(agentState == 3)


simulationData = simulationData[~np.isnan(simulationData).any(axis=1),:]
numberOfhealthy = numberOfhealthy[~np.isnan(numberOfhealthy)]
numberOfIll = numberOfIll[~np.isnan(numberOfIll)]
numberOfRecovered = numberOfRecovered[~np.isnan(numberOfRecovered)]

SimulationData = pd.DataFrame({'agent':simulationData[:,0],'x':simulationData[:,1], 'y':simulationData[:,2], 't':simulationData[:,3],'state':simulationData[:,4]})
SimulationData.to_csv('SimulationData_.csv', index=False)