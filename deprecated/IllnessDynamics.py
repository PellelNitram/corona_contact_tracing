# Generated with SMOP  0.41
from libsmop import *
# IllnessDynamics.m

    
@function
def IllnessDynamics(grid=None,agentState=None,beta=None,gamma=None,*args,**kwargs):
    varargin = IllnessDynamics.varargin
    nargin = IllnessDynamics.nargin

    numberOfIndividualsOnCell=cellfun('length',grid)
# IllnessDynamics.m:3
    groupIndices=numberOfIndividualsOnCell > 1
# IllnessDynamics.m:4
    singleIndices=numberOfIndividualsOnCell == 1
# IllnessDynamics.m:5
    groups=grid(groupIndices)
# IllnessDynamics.m:7
    singles=grid(singleIndices)
# IllnessDynamics.m:8
    for k in arange(1,length(groups)).reshape(-1):
        group=groups[k]
# IllnessDynamics.m:11
        groupStates=agentState(group)
# IllnessDynamics.m:12
        for j in arange(1,length(group)).reshape(-1):
            individual=group(j)
# IllnessDynamics.m:15
            state=groupStates(j)
# IllnessDynamics.m:16
            if state == 2:
                r=copy(rand)
# IllnessDynamics.m:18
                if r < beta:
                    temp=groupStates == 1
# IllnessDynamics.m:20
                    healtyIndividuals=group(temp)
# IllnessDynamics.m:21
                    agentState[healtyIndividuals]=2
# IllnessDynamics.m:22
                q=copy(rand)
# IllnessDynamics.m:24
                if q < gamma:
                    agentState[individual]=3
# IllnessDynamics.m:26
    
    
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
    
if __name__ == '__main__':
    pass
    