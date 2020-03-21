function [agentState] = InitializeAgentStates(numberOfAgents, initialInfected)
    
    agentState = ones(numberOfAgents,1);
    
    perm = randperm(numberOfAgents);
    
    agentState(perm<initialInfected+1)=2;
    
end

