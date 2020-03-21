function [] = PlotGrid(locations,agentState,gridSize, t)
    myColors = zeros(size(agentState, 1), 3); % List of rgb colors for every data point.
    rowsToSetBlue = agentState == 1;
    rowsToSetRed = agentState == 2;
    rowsToSetGreen = agentState == 3;
    myColors(rowsToSetBlue, :) = repmat([0,0,1],sum(rowsToSetBlue),1);
    myColors(rowsToSetRed, :) = repmat([1,0,0],sum(rowsToSetRed),1);
    myColors(rowsToSetGreen, :) = repmat([0,1,0],sum(rowsToSetGreen),1);
    sz = 20;
    scatter(locations(:,1),locations(:,2),sz,myColors,'filled');
    axis([0 gridSize+1 0 gridSize+1]);
    currentTime = strcat('$t=', num2str(t), '$');
    title(currentTime,'Interpreter','latex', 'FontSize', 28)
    xlabel('$x$','Interpreter','latex', 'FontSize', 28)
    ylabel('$y$','Interpreter','latex', 'FontSize', 28)
    box on;
    axis square;
    drawnow
end

