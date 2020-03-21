function [agentState] = IllnessDynamics(grid, agentState, beta, gamma)

    numberOfIndividualsOnCell = cellfun('length',grid);
    groupIndices = numberOfIndividualsOnCell > 1;
    singleIndices = numberOfIndividualsOnCell == 1;
    
    groups = grid(groupIndices);
    singles = grid(singleIndices);
    
    for k = 1:length(groups)
        group = groups{k};
        groupStates = agentState(group);
        
        for j = 1:length(group)
            individual = group(j);
            state = groupStates(j);
            if state == 2
                r = rand;
                if r < beta
                    temp = groupStates == 1;
                    healtyIndividuals = group(temp);
                    agentState(healtyIndividuals) = 2;
                end
                q = rand;
                if q < gamma
                    agentState(individual)=3;
                end
            end
        end 
    end
    
    for l = 1:length(singles)
        single = singles{l};
        state = agentState(single);
        if state == 2
            q = rand;
            if q < gamma
                agentState(single)=3;
            end
        end
    end
        
end

