function [proportionOfRecovered] = DiseaseFunction(infectionRate, beta, gamma, diffusionRate)
    
    gridSize = 100;
    grid = cell(gridSize);
    numberOfAgents = 1000;
    locations = randi(gridSize,numberOfAgents,2);
    agentState = InitializeAgentStatesRandom(numberOfAgents, infectionRate);


    for t = 1:numberOfAgents
        loc = locations(t,:);
        grid{loc(1),loc(2)} = [grid{loc(1),loc(2)}, t];
    end

    numberOfIll = sum(agentState == 2);
    numberOfRecovered = sum(agentState == 3);

    while numberOfIll > 0

        agentState = IllnessDynamics(grid, agentState, beta, gamma);
        [grid, locations] = PerformeSteps(numberOfAgents, locations, gridSize, diffusionRate);
        
        numberOfSusceptible = sum(agentState==1);
        numberOfIll = sum(agentState==2);
        numberOfRecovered = sum(agentState==3);
        
        if numberOfSusceptible == 0
            numberOfRecovered = numberOfAgents;
            break
        end

    end
    
    proportionOfRecovered = numberOfRecovered/numberOfAgents;
end

