clear;
close all;

testRate = 0.1;
numberOfAgents = 1000;
initialInfected = 2;

beta = 0.9;
gamma = 0.01;

gridSize = 100;
grid = cell(gridSize);

% generate some agents and assign them a location
locations = randi(gridSize,numberOfAgents,2);
agentState = InitializeAgentStates(numberOfAgents, initialInfected);
diffusionRates = InitializeDiffusionRates(numberOfAgents);
agentIds = [0:numberOfAgents-1].';

AgentMaster = [agentIds,agentState,diffusionRates];
T = array2table(AgentMaster,'VariableNames',{'agent','agent_state','diffusion_rate'});
writetable(T,'AgentMaster.csv')

for t = 1:numberOfAgents
    loc = locations(t,:);
    grid{loc(1),loc(2)} = [grid{loc(1),loc(2)}, t];
end

len = 10000;
numberOfhealthy = zeros(len,1);
numberOfIll = zeros(len,1);
numberOfRecovered = zeros(len,1);

numberOfhealthy(1) = sum(agentState == 1);
numberOfIll(1) = sum(agentState == 2);
numberOfRecovered(1) = sum(agentState == 3);

t = 1;

prealloc = 100000;
simulationData = NaN(prealloc,5);

knownStates = zeros(size(agentState));
simulationData(1:numberOfAgents,:) = [agentIds, locations,t*ones(numberOfAgents,1),knownStates];

testedAgents = zeros(size(agentState));
testedHealthy = 0;
while numberOfIll(t) > 0
    
    agentState = IllnessDynamics(grid, agentState, beta, gamma);
    [grid, locations] = PerformeSteps(numberOfAgents, locations, gridSize, diffusionRates);
    
    agentStateTested = agentState+testedAgents;
    
    % Testing in eine Funktion auslagern
    if rand<testRate
        % Test sampling
        p = randperm(length(agentStateTested));
        [C,ia,~] = unique(agentStateTested(p));
        ia = p(ia);
        
        if sum(ismember([1,2],C))==2
            if rand<0.8
                % test someone with corona
                corona = 2;
                testedHealthy = 0;
            else
                % test someone without corona
                corona = 1;
                testedHealthy = 1;
            end
            i = ia(corona);
            testedAgents(i)=1;
        elseif ismember(1,C)
            corona = 1;
            i = ia(corona);
            testedAgents(i)=1;
            testedHealthy = 1;
        elseif ismember(2,C)
            corona = 1;
            i = ia(corona);
            testedAgents(i)=1;
            testedHealthy = 0;
        end
        
    end
    
    % eventuell redundante daten nicht abspeichern 
    t = t+1;
    if numberOfAgents*t+1 > size(simulationData,1)
        simulationData = [simulationData; zeros(prealloc,5)];
    end
    
    knownStates = zeros(size(agentState));
    knownStates(testedAgents==1) = agentState(testedAgents==1);
    simulationData(numberOfAgents*(t-1)+1:numberOfAgents*t,:) = [agentIds, locations,t*ones(numberOfAgents,1),knownStates];
    
    if testedHealthy == 1
        testedAgents(i)=0;
    end
    
    
    numberOfhealthy(t) = sum(agentState==1);
    numberOfIll(t) = sum(agentState==2);
    numberOfRecovered(t) = sum(agentState==3);
    
end

disp(t)


a = isnan(simulationData(:,1));
simulationData(a,:) = [];
simulation = array2table(simulationData,'VariableNames',{'agent','x','y','t','state'});
writetable(simulation,'simulation.csv')
