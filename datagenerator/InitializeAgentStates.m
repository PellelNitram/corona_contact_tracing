function [agentState] = InitializeAgentStates(locations, maxInfectionRate, gridSize)
    
    centerOfGrid = [gridSize/2 gridSize/2];
    numberOfAgents = size(locations,1);
    agentState = zeros(numberOfAgents,1);
    radius = 1;
    
    
    while 1
        
        for i = 1:numberOfAgents
            currentLocation = locations(i,:);
            distanceToCenter = sqrt(sum((centerOfGrid - currentLocation) .^ 2));
            
            if distanceToCenter<radius
                agentState(i) = 2;
            else
                agentState(i) = 1;
            end
            
            infectionRate = sum(agentState==2)/numberOfAgents;
            if infectionRate > maxInfectionRate
                break
            end
        end
        
        if infectionRate > maxInfectionRate
            break
        end
        
        radius = radius + 1;
    end

end

