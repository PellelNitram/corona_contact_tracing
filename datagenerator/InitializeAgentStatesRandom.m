function [agentState] = InitializeAgentStatesRandom(numberOfAgents, illnessRate)

    agentState=zeros(numberOfAgents,1);
    for i = 1:numberOfAgents
        r = rand;
        if r<illnessRate
            agentState(i) = 2;
        else
            agentState(i) = 1;
        end

    end

end
