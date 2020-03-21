# Generated with SMOP  0.41
from libsmop import *
# InitializeAgentStates.m

    
@function
def InitializeAgentStates(numberOfAgents=None,initialInfected=None,*args,**kwargs):
    varargin = InitializeAgentStates.varargin
    nargin = InitializeAgentStates.nargin

    
    agentState=ones(numberOfAgents,1)
# InitializeAgentStates.m:3
    perm=randperm(numberOfAgents)
# InitializeAgentStates.m:5
    agentState[perm < initialInfected + 1]=2
# InitializeAgentStates.m:7
    return agentState
    
if __name__ == '__main__':
    pass
    