clear;
close all;
figure('units','normalized','outerposition',[0 0 1 1])

diffusionRate = 0.8;
beta = 0.6;
gamma = 0.01;

gridSize = 100;
grid = cell(gridSize);
% generate some agents and assign them a location
numberOfAgents = 1000;
infectionRate = 0.1;
locations = randi(gridSize,numberOfAgents,2);
agentState = InitializeAgentStates(locations, infectionRate, gridSize);


for t = 1:numberOfAgents
    loc = locations(t,:);
    grid{loc(1),loc(2)} = [grid{loc(1),loc(2)}, t];
end

% plot initial population
subplot(1,2,1);
PlotGrid(locations,agentState,gridSize,0);

len = 10000;
numberOfhealthy = zeros(len,1);
numberOfIll = zeros(len,1);
numberOfRecovered = zeros(len,1);

numberOfhealthy(1) = sum(agentState == 1);
numberOfIll(1) = sum(agentState == 2);
numberOfRecovered(1) = sum(agentState == 3);

t = 1;
while numberOfIll(t) > 0
    
    
    agentState = IllnessDynamics(grid, agentState, beta, gamma);
    [grid, locations] = PerformeSteps(numberOfAgents, locations, gridSize, diffusionRate);
    
    if mod(t,10) == 0
        subplot(1,2,1);
        PlotGrid(locations,agentState,gridSize, t);
    end
    
    if t == 100
        locations100 = locations;
        agentState100 = agentState;
    end
    
    
    t = t+1;
    numberOfhealthy(t) = sum(agentState==1);
    numberOfIll(t) = sum(agentState==2);
    numberOfRecovered(t) = sum(agentState==3);
    
end

subplot(1,2,1);
PlotGrid(locations100,agentState100,gridSize, 100);


x = 1:length(numberOfhealthy);
subplot(1,2,2);
axis square;
hold on;
plot(x(1:t),numberOfhealthy(1:t),'b','LineWidth',3.0)
plot(x(1:t),numberOfIll(1:t),'r','LineWidth',3.0)
plot(x(1:t),numberOfRecovered(1:t),'g','LineWidth',3.0)
temp=(['$d = ',num2str(diffusionRate),'$, $\beta = ',num2str(beta),'$, $\gamma = ',num2str(gamma), '$']);
title(temp,'Interpreter','latex', 'FontSize', 28)
xlabel('Time Steps', 'FontSize', 28)
ylabel('Number of agents', 'FontSize', 28)
ylim([0 numberOfAgents])
xlim([0 t])
