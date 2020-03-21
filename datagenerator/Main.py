# Generated with SMOP  0.41
import numpy as np
import pandas as pd

def InitializeAgentStates(numberOfAgents,initialInfected):

    agentState = np.ones((numberOfAgents,))
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
    groups = grid[groupIndices].dropnan
    singles = grid[singleIndices]

    for group in groups:
        groupStates=agentState(group)
        for j in arange(1,length(group)).reshape(-1):
            individual=group(j)
            state=groupStates(j)
            if state == 2:
                r=copy(rand)
                if r < beta:
                    temp=groupStates == 1
                    healtyIndividuals=group(temp)
                    agentState[healtyIndividuals]=2
                q=copy(rand)
                if q < gamma:
                    agentState[individual]=3
    
    
    for l in arange(1,length(singles)).reshape(-1):
        single=singles[l]
# IllnessDynamics.m:33
        state=agentState(single)
# IllnessDynamics.m:34
        if state == 2:
            q=copy(rand)
# IllnessDynamics.m:36
            if q < gamma:
                agentState[single]=3
# IllnessDynamics.m:38
    
    
    return agentState



testRate = 0.1
numberOfAgents = 1000
initialInfected = 5

beta = 0.6

gamma = 0.01
gridSize = 100


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

prealloc=10000
numberOfhealthy = np.zeros(prealloc,)
numberOfIll = np.zeros(prealloc,)
numberOfRecovered = np.zeros(prealloc,)
numberOfhealthy[0] = sum(agentState == 1)
numberOfIll[0] = sum(agentState == 2)
numberOfRecovered[0] = sum(agentState == 3)



simulationData = np.full((prealloc, 5), np.NaN)
knownStates = np.zeros(agentState.shape,dtype=np.int64)


# a = np.concatenate((agentIds,locations,t*np.ones((numberOfAgents,)),knownStates), axis=1)
# simulationData[0:numberOfAgents,:] = a

testedAgents = np.zeros(agentState.shape)
testedHealthy=0

t=0
while numberOfIll[t] > 0:

    agentState = IllnessDynamics(grid_,agentState,beta,gamma)
    grid,locations = PerformeSteps(numberOfAgents,locations,gridSize,diffusionRates,nargout=2)
    agentStateTested=agentState + testedAgents
    if rand < testRate:
        # Test sampling
        p=randperm(length(agentStateTested))
        C,ia,__=unique(agentStateTested(p),nargout=3)
        ia=p(ia)
        if sum(ismember(concat([1,2]),C)) == 2:
            if rand < 0.8:
                # test someone with corona
                corona=2
                testedHealthy=0
            else:
                # test someone without corona
                corona=1
                testedHealthy=1
            i=ia(corona)
            testedAgents[i]=1
        else:
            if ismember(1,C):
                corona=1
                i=ia(corona)
                testedAgents[i]=1
                testedHealthy=1
            else:
                if ismember(2,C):
                    corona=1
                    i=ia(corona)
                    testedAgents[i]=1
                    testedHealthy=0
    # eventuell redundante daten nicht abspeichern
    t=t + 1
    if dot(numberOfAgents,t) + 1 > size(simulationData,1):
        simulationData=concat([[simulationData],[zeros(prealloc,5)]])
    knownStates=zeros(size(agentState))
    knownStates[testedAgents == 1]=agentState(testedAgents == 1)
    simulationData[arange(dot(numberOfAgents,(t - 1)) + 1,dot(numberOfAgents,t)),arange()]=concat([agentIds,locations,dot(t,ones(numberOfAgents,1)),knownStates])
    if testedHealthy == 1:
        testedAgents[i]=0
    numberOfhealthy[t]=sum(agentState == 1)
    numberOfIll[t]=sum(agentState == 2)
    numberOfRecovered[t]=sum(agentState == 3)


a=isnan(simulationData(arange(),1))
simulationData[a,arange()]=[]
simulation=array2table(simulationData,'VariableNames',cellarray(['agent','x','y','t','state']))
writetable(simulation,'simulation.csv')